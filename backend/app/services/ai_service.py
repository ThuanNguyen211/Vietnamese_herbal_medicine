"""
AI Service - Tích hợp mô hình DenseNet161 nhận diện 50 cây thuốc nam Việt Nam.
"""

import io
import os
import uuid
import unicodedata
import re
import logging
from typing import Optional, List, Tuple

import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
from sqlalchemy.orm import Session
from app.models import Plant

logger = logging.getLogger(__name__)

# ============================================================
# Danh sách 50 class theo đúng thứ tự index 0-49 của model
# ============================================================
CLASS_NAMES: List[str] = [
    "Rau má",              # 0
    "Diếp cá",             # 1
    "Tía tô",              # 2
    "Sả",                  # 3
    "Gừng",                # 4
    "Nghệ vàng",           # 5
    "Nghệ đen",            # 6
    "Lá lốt",              # 7
    "Kinh giới",           # 8
    "Húng chanh",           # 9
    "Bạc hà",              # 10
    "Ngải cứu",            # 11
    "Cỏ mần trầu",         # 12
    "Chó đẻ răng cưa",     # 13
    "Nhọ nồi",             # 14
    "Trinh nữ",            # 15
    "Dừa cạn",             # 16
    "Hoàn ngọc",           # 17
    "Xạ đen",              # 18
    "Cỏ ngọt",             # 19
    "Kim ngân hoa",         # 20
    "Ké đầu ngựa",         # 21
    "Bồ công anh",          # 22
    "Ích mẫu",             # 23
    "Mã đề",               # 24
    "Cỏ tranh",            # 25
    "Muồng trâu",          # 26
    "Lược vàng",           # 27
    "Thiên lý",            # 28
    "Khổ qua",             # 29
    "Sung",                # 30
    "Vối",                 # 31
    "Sâm đất",             # 32
    "Đinh lăng",           # 33
    "Cúc tần",             # 34
    "Me đất",              # 35
    "Lạc tiên",            # 36
    "Chè xanh",            # 37
    "Dâu tằm",             # 38
    "Sài đất",             # 39
    "Rau sam",             # 40
    "Ngũ gia bì",          # 41
    "Xuyên tâm liên",      # 42
    "Thìa canh",           # 43
    "Bạch hoa xà",         # 44
    "Gấc",                 # 45
    "Mơ lông",             # 46
    "Nhàu",                # 47
    "Cây vằng",            # 48
    "Dấp cá biển",         # 49
]

NUM_CLASSES = len(CLASS_NAMES)  # 50

# ============================================================
# Transform ảnh (giống lúc train: resize 224, normalize ImageNet)
# ============================================================
image_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])

# ============================================================
# Load model DenseNet161 một lần khi khởi động server
# ============================================================
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "densenet_best.pth")

_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_model = None


def _load_model():
    """Load DenseNet201 model với custom classifier (50 classes)."""
    global _model
    if _model is not None:
        return _model

    logger.info("Đang load model DenseNet201 từ %s ...", MODEL_PATH)

    model = models.densenet201(weights=None)
    # Thay classifier cuối cùng cho 50 class
    in_features = model.classifier.in_features  # 1920 cho DenseNet201
    model.classifier = torch.nn.Linear(in_features, NUM_CLASSES)

    state_dict = torch.load(MODEL_PATH, map_location=_device, weights_only=True)
    model.load_state_dict(state_dict)
    model.to(_device)
    model.eval()

    _model = model
    logger.info("Load model thành công! Device: %s", _device)
    return _model


# Load model ngay khi import module
try:
    _load_model()
except Exception as e:
    logger.error("Không thể load model: %s", e)


def normalize_vietnamese(text: str) -> str:
    """Chuẩn hóa text tiếng Việt để so sánh không dấu."""
    if not text:
        return ""

    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.replace("đ", "d")
    text = re.sub(r"\s+", " ", text)
    return text


def classify_image(image_bytes: bytes, top_k: int = 2) -> List[Tuple[str, float]]:
    """
    Nhận diện cây thuốc nam từ ảnh bằng DenseNet201.
    
    Input: image bytes
    Output: List of (plant_name, confidence_score).
    Mặc định trả về tối đa 2 cây, nhưng sẽ chỉ trả về top-1 nếu:
    - top-1 >= 75%, hoặc
    - top-2 <= 25%
    """
    model = _load_model()
    if model is None:
        logger.error("Model chưa được load!")
        return []

    try:
        # Đọc ảnh và chuyển sang RGB
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = image_transform(img).unsqueeze(0).to(_device)

        # Inference
        with torch.no_grad():
            output = model(tensor)
            probabilities = F.softmax(output, dim=1)[0]

        # Lấy top-k kết quả
        top_probs, top_indices = torch.topk(probabilities, k=min(top_k, NUM_CLASSES))
        
        results: List[Tuple[str, float]] = []
        for prob, idx in zip(top_probs, top_indices):
            class_name = CLASS_NAMES[idx.item()]
            confidence = prob.item()
            results.append((class_name, confidence))

        if len(results) >= 2:
            top_1_conf = results[0][1]
            top_2_conf = results[1][1]
            if top_1_conf >= 0.75 or top_2_conf <= 0.25:
                return results[:1]

        return results

    except Exception as e:
        logger.error("Lỗi khi phân loại ảnh: %s", e)
        return []


def match_symptoms_to_plants(symptoms_text: str, db: Session) -> List[Tuple[Plant, float]]:
    """
    Tìm cây thuốc nam phù hợp với nội dung text người dùng nhập.

    Hỗ trợ tìm theo nhiều trường:
    - tên cây, tên khoa học, tên khác
    - mô tả, công dụng, triệu chứng
    - bộ phận dùng, cách dùng, vùng phân bố

    Trả về kết quả theo logic giống ảnh:
    - Mặc định tối đa 2 cây
    - Nếu top-1 >= 75% hoặc top-2 <= 25% thì chỉ trả top-1
    """
    normalized_query = normalize_vietnamese(symptoms_text)
    if not normalized_query:
        return []

    keywords = re.findall(r"[a-z0-9]+", normalized_query)

    searchable_fields = [
        ("name", 6.0),
        ("scientific_name", 5.0),
        ("other_names", 5.0),
        ("symptoms", 4.5),
        ("usage", 4.0),
        ("description", 3.5),
        ("parts_used", 3.0),
        ("family", 2.0),
        ("preparation", 2.0),
        ("distribution", 1.5),
    ]

    plants = db.query(Plant).all()
    scored_results: List[Tuple[Plant, float]] = []

    for plant in plants:
        score = 0.0

        for field_name, field_weight in searchable_fields:
            raw_value = getattr(plant, field_name, None)
            if not raw_value:
                continue

            field_text = normalize_vietnamese(str(raw_value))
            if not field_text:
                continue

            # Tăng điểm mạnh khi cụm truy vấn xuất hiện nguyên cụm trong field.
            if normalized_query in field_text:
                score += field_weight * 2.5

            keyword_hits = 0
            for kw in keywords:
                if kw in field_text:
                    keyword_hits += 1

            # Giới hạn số hit để tránh field dài lấn át hoàn toàn.
            if keyword_hits:
                score += field_weight * min(keyword_hits, 3)

        # Bonus khi query trùng chính xác tên cây.
        if normalized_query == normalize_vietnamese(plant.name or ""):
            score += 20.0

        if score > 0:
            scored_results.append((plant, score))

    if not scored_results:
        return []

    scored_results.sort(key=lambda x: x[1], reverse=True)

    score_tensor = torch.tensor([score for _, score in scored_results], dtype=torch.float32)
    confidence_tensor = F.softmax(score_tensor, dim=0)
    ranked_results: List[Tuple[Plant, float]] = []

    for (plant, _), confidence in zip(scored_results, confidence_tensor):
        ranked_results.append((plant, round(float(confidence.item()), 2)))

    top_results = ranked_results[:2]
    if len(top_results) >= 2:
        top_1_conf = top_results[0][1]
        top_2_conf = top_results[1][1]
        if top_1_conf >= 0.75 or top_2_conf <= 0.25:
            return top_results[:1]

    return top_results


def process_map(
    message: Optional[str],
    image_bytes: Optional[bytes],
    db: Session
) -> dict:
    """
    Xử lý yêu cầu map: text + ảnh.
    Trả về dict với reply, recommended_plants, session_id.
    """
    session_id = str(uuid.uuid4())[:8]
    recommended = []
    reply_parts = []
    lock_to_image_top1 = False

    # 1. Xử lý ảnh (nếu có)
    if image_bytes:
        predictions = classify_image(image_bytes)
        if predictions:
            # Nếu classify_image chỉ trả về 1 kết quả khi top_k=2, coi như ảnh đã đủ chắc chắn.
            lock_to_image_top1 = len(predictions) == 1
            reply_parts.append("📷 **Kết quả nhận diện từ ảnh:**")
            for plant_name, conf in predictions:
                plant = db.query(Plant).filter(Plant.name == plant_name).first()
                if plant:
                    recommended.append({
                        "id": plant.id,
                        "name": plant.name,
                        "scientific_name": plant.scientific_name,
                        "image_url": plant.image_url,
                        "usage": plant.usage,
                        "distribution_coords": plant.distribution_coords,
                        "confidence": round(conf, 2),
                    })
                    reply_parts.append(f"- **{plant.name}** ({plant.scientific_name}) - Độ tin cậy: {conf:.0%}")
                else:
                    reply_parts.append(f"- **{plant_name}** - Độ tin cậy: {conf:.0%} (chưa có trong CSDL)")

    # 2. Xử lý text từ người dùng (nếu có)
    if message and message.strip() and not lock_to_image_top1:
        matches = match_symptoms_to_plants(message, db)
        if matches:
            reply_parts.append(f"\n🌿 **Cây thuốc nam phù hợp với nội dung \"{message}\":**")
            for plant, conf in matches:
                # Tránh trùng lặp
                if not any(r["id"] == plant.id for r in recommended):
                    recommended.append({
                        "id": plant.id,
                        "name": plant.name,
                        "scientific_name": plant.scientific_name,
                        "image_url": plant.image_url,
                        "usage": plant.usage,
                        "distribution_coords": plant.distribution_coords,
                        "confidence": round(conf, 2),
                    })
                reply_parts.append(f"- **{plant.name}**: {plant.usage[:100] if plant.usage else 'N/A'}...")
        else:
            reply_parts.append(
                f"Không tìm thấy cây thuốc nam phù hợp với nội dung \"{message}\". "
                "Bạn có thể thử theo tên cây, mô tả, công dụng, bộ phận dùng hoặc triệu chứng."
            )

    if not reply_parts:
        reply_parts.append(
            "Vui lòng nhập nội dung (tên cây/mô tả/công dụng/triệu chứng/...) "
            "hoặc tải lên ảnh cây thuốc nam để tôi hỗ trợ bạn."
        )

    return {
        "reply": "\n".join(reply_parts),
        "recommended_plants": recommended,
        "session_id": session_id,
    }
