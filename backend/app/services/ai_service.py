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
    """Chuẩn hóa text tiếng Việt để so sánh."""
    text = text.lower().strip()
    return text


def classify_image(image_bytes: bytes, top_k: int = 2) -> List[Tuple[str, float]]:
    """
    Nhận diện cây thuốc nam từ ảnh bằng DenseNet201.
    
    Input: image bytes
    Output: List of (plant_name, confidence_score) — top-k kết quả (mặc định 2)
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

        return results

    except Exception as e:
        logger.error("Lỗi khi phân loại ảnh: %s", e)
        return []


def match_symptoms_to_plants(symptoms_text: str, db: Session) -> List[Tuple[Plant, float]]:
    """
    Placeholder: Tìm cây thuốc nam phù hợp với triệu chứng.
    
    Khi tích hợp model thật (NLP/embedding), thay thế hàm này.
    Hiện tại dùng keyword matching đơn giản.
    """
    keywords = [k.strip().lower() for k in symptoms_text.split(",")]
    if len(keywords) == 1:
        keywords = symptoms_text.lower().split()

    plants = db.query(Plant).all()
    results = []

    for plant in plants:
        if not plant.symptoms:
            continue
        plant_symptoms = plant.symptoms.lower()
        score = 0
        for kw in keywords:
            if kw in plant_symptoms:
                score += 1
        if score > 0:
            confidence = min(score / max(len(keywords), 1), 1.0)
            results.append((plant, confidence))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:5]


def process_chat(
    message: Optional[str],
    image_bytes: Optional[bytes],
    db: Session
) -> dict:
    """
    Xử lý yêu cầu chatbot: text + ảnh.
    Trả về dict với reply, recommended_plants, session_id.
    """
    session_id = str(uuid.uuid4())[:8]
    recommended = []
    reply_parts = []

    # 1. Xử lý ảnh (nếu có)
    if image_bytes:
        predictions = classify_image(image_bytes)
        if predictions:
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

    # 2. Xử lý text triệu chứng (nếu có)
    if message and message.strip():
        matches = match_symptoms_to_plants(message, db)
        if matches:
            reply_parts.append(f"\n🌿 **Cây thuốc nam phù hợp với triệu chứng \"{message}\":**")
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
            reply_parts.append(f"Không tìm thấy cây thuốc nam phù hợp với triệu chứng \"{message}\". Vui lòng thử lại với mô tả khác.")

    if not reply_parts:
        reply_parts.append("Vui lòng nhập triệu chứng hoặc tải lên ảnh cây thuốc nam để tôi hỗ trợ bạn.")

    return {
        "reply": "\n".join(reply_parts),
        "recommended_plants": recommended,
        "session_id": session_id,
    }
