"""
Seed data: Dữ liệu mẫu 50 cây thuốc nam Việt Nam.
Nguồn: Dữ liệu mẫu - Cây thuốc Nam.csv
Chạy file này để tạo database và thêm dữ liệu.
"""

from app.database import engine, SessionLocal, Base
from app.models import Plant


def get_first_letter(name: str) -> str:
    """Lấy chữ cái đầu tiên (viết hoa) của tên cây, hỗ trợ tiếng Việt."""
    name = name.strip()
    if not name:
        return "#"
    first_char = name[0].upper()
    if first_char == "Đ" or first_char == "\u0110":
        return "Đ"
    return first_char


SOUTHERN_LOCATIONS = [
    {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
    {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"},
    {"lat": 10.2433, "lng": 106.3756, "location": "Bến Tre"},
    {"lat": 10.4938, "lng": 105.6882, "location": "Đồng Tháp"},
    {"lat": 10.0125, "lng": 105.0809, "location": "Rạch Giá, Kiên Giang"},
    {"lat": 9.1769, "lng": 105.1524, "location": "Cà Mau"},
    {"lat": 9.6037, "lng": 105.9739, "location": "Sóc Trăng"},
    {"lat": 9.2941, "lng": 105.7278, "location": "Bạc Liêu"},
    {"lat": 10.3600, "lng": 106.3590, "location": "Mỹ Tho, Tiền Giang"},
    {"lat": 10.2534, "lng": 105.9722, "location": "Vĩnh Long"},
    {"lat": 10.6956, "lng": 106.2431, "location": "Long An"},
    {"lat": 11.3254, "lng": 106.4770, "location": "Bình Dương"},
    {"lat": 10.9574, "lng": 106.8426, "location": "Đồng Nai"},
    {"lat": 11.3351, "lng": 106.1099, "location": "Tây Ninh"},
    {"lat": 10.4114, "lng": 107.1362, "location": "Bà Rịa - Vũng Tàu"},
    {"lat": 10.2899, "lng": 103.9840, "location": "Phú Quốc"},
]


def build_southern_distribution_coords(plant_name: str, total_points: int = 3):
    """Sinh tọa độ phân bố chỉ trong miền Nam Việt Nam cho từng cây."""
    if not plant_name:
        plant_name = "cay-thuoc"

    start = sum(ord(ch) for ch in plant_name) % len(SOUTHERN_LOCATIONS)
    step = 5  # Coprime với 16 để đảm bảo lấy điểm không trùng.
    coords = []

    for i in range(total_points):
        idx = (start + i * step) % len(SOUTHERN_LOCATIONS)
        coords.append(dict(SOUTHERN_LOCATIONS[idx]))

    return coords


SAMPLE_PLANTS = [
    # 1. Rau má
    {
        "name": "Rau má",
        "scientific_name": "Centella asiatica",
        "other_names": "Tích tuyết thảo, Liên tiền thảo",
        "family": "Apiaceae (Hoa tán)",
        "description": "Thân bò sát đất, lá tròn hình thận, mép khía, rễ mọc tại đốt",
        "parts_used": "Toàn cây",
        "usage": "Thanh nhiệt, mát gan, giải độc",
        "preparation": "Rau tươi xay sinh tố, sắc nước uống. Dùng 30-40g tươi/ngày.",
        "symptoms": "nóng trong, mụn nhọt, mát gan, giải độc, thanh nhiệt, da xấu",
        "image_url": "/images/thumbnails/01_rau_ma.jpg",
        "distribution": "Mọc hoang và trồng khắp Việt Nam, rất phổ biến.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"}
        ],
    },
    # 2. Diếp cá
    {
        "name": "Diếp cá",
        "scientific_name": "Houttuynia cordata",
        "other_names": "Giấp cá, Rau giấp",
        "family": "Saururaceae (Lá giấp)",
        "description": "Thân thảo, mùi tanh, lá hình tim, hoa nhỏ trắng",
        "parts_used": "Lá, thân",
        "usage": "Trị mụn, trĩ, kháng viêm",
        "preparation": "Lá tươi giã nát đắp ngoài hoặc sắc nước uống, 30-50g/ngày.",
        "symptoms": "mụn nhọt, trĩ, viêm, kháng viêm, nóng trong, giải độc",
        "image_url": "/images/thumbnails/02_diep_ca.jpg",
        "distribution": "Mọc hoang khắp Việt Nam, nhiều ở vùng ẩm mát.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 16.4637, "lng": 107.5909, "location": "Huế"}
        ],
    },
    # 3. Tía tô
    {
        "name": "Tía tô",
        "scientific_name": "Perilla frutescens",
        "other_names": "Tử tô, É tía",
        "family": "Lamiaceae (Hoa môi)",
        "description": "Thân vuông, lá răng cưa, xanh tím",
        "parts_used": "Lá, cành",
        "usage": "Giải cảm, ho",
        "preparation": "Lá tươi ăn sống, nấu cháo giải cảm. Sắc nước uống 10-20g.",
        "symptoms": "cảm lạnh, ho, dị ứng, ngộ độc hải sản, buồn nôn, đầy bụng",
        "image_url": "/images/thumbnails/03_tia_to.jpg",
        "distribution": "Trồng phổ biến khắp Việt Nam, đặc biệt miền Bắc.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 20.8449, "lng": 106.6881, "location": "Hải Phòng"},
            {"lat": 20.4388, "lng": 106.1621, "location": "Nam Định"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"}
        ],
    },
    # 4. Sả
    {
        "name": "Sả",
        "scientific_name": "Cymbopogon citratus",
        "other_names": "Sả chanh, Hương mao",
        "family": "Poaceae (Hòa thảo)",
        "description": "Thân giả củ, lá dài hẹp, mùi thơm",
        "parts_used": "Thân, lá",
        "usage": "Giải cảm, tiêu hóa",
        "preparation": "Thân và lá nấu nước xông, nấu nước uống. Tinh dầu sả dùng ngoài.",
        "symptoms": "cảm cúm, đau đầu, đau bụng, đầy hơi, tiêu hóa kém",
        "image_url": "/images/thumbnails/04_sa.jpg",
        "distribution": "Trồng phổ biến khắp Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 18.6790, "lng": 105.6813, "location": "Nghệ An"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"}
        ],
    },
    # 5. Gừng
    {
        "name": "Gừng",
        "scientific_name": "Zingiber officinale",
        "other_names": "Sinh khương (tươi), Can khương (khô)",
        "family": "Zingiberaceae (Gừng)",
        "description": "Thân rễ phình, màu vàng nhạt",
        "parts_used": "Thân rễ",
        "usage": "Chống lạnh, buồn nôn",
        "preparation": "Củ tươi giã lấy nước, sắc nước uống, pha trà gừng, nấu ăn.",
        "symptoms": "cảm lạnh, buồn nôn, đau bụng, đầy hơi, ho, viêm họng, đau cơ",
        "image_url": "/images/thumbnails/05_gung.jpg",
        "distribution": "Trồng khắp cả nước, nhiều ở các tỉnh miền núi phía Bắc và Tây Nguyên.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 22.3363, "lng": 103.8438, "location": "Sa Pa, Lào Cai"},
            {"lat": 14.0583, "lng": 108.2772, "location": "Gia Lai"}
        ],
    },
    # 6. Nghệ vàng
    {
        "name": "Nghệ vàng",
        "scientific_name": "Curcuma longa",
        "other_names": "Khương hoàng, Uất kim",
        "family": "Zingiberaceae (Gừng)",
        "description": "Thân rễ màu vàng cam",
        "parts_used": "Thân rễ",
        "usage": "Viêm loét dạ dày",
        "preparation": "Củ tươi giã lấy nước, bột nghệ pha uống với mật ong. Tinh bột nghệ.",
        "symptoms": "đau dạ dày, viêm loét, vết thương, da xấu, tiêu hóa kém, viêm khớp",
        "image_url": "/images/thumbnails/06_nghe_vang.jpg",
        "distribution": "Trồng nhiều ở Hưng Yên, Nghệ An, Đắk Lắk.",
        "distribution_coords": [
            {"lat": 20.6527, "lng": 106.0512, "location": "Hưng Yên"},
            {"lat": 18.6790, "lng": 105.6813, "location": "Nghệ An"},
            {"lat": 12.7100, "lng": 108.2378, "location": "Đắk Lắk"}
        ],
    },
    # 7. Nghệ đen
    {
        "name": "Nghệ đen",
        "scientific_name": "Curcuma zedoaria",
        "other_names": "Nga truật, Nghệ tím",
        "family": "Zingiberaceae (Gừng)",
        "description": "Thân rễ tím đen",
        "parts_used": "Thân rễ",
        "usage": "Rối loạn kinh nguyệt",
        "preparation": "Thân rễ phơi khô sắc nước uống hoặc ngâm rượu. Liều 6-12g/ngày.",
        "symptoms": "rối loạn kinh nguyệt, đau bụng kinh, ứ huyết, đầy bụng, khó tiêu",
        "image_url": "/images/thumbnails/07_nghe_den.jpg",
        "distribution": "Trồng nhiều ở miền Trung và Tây Nguyên.",
        "distribution_coords": [
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"},
            {"lat": 14.0583, "lng": 108.2772, "location": "Gia Lai"},
            {"lat": 12.7100, "lng": 108.2378, "location": "Đắk Lắk"}
        ],
    },
    # 8. Lá lốt
    {
        "name": "Lá lốt",
        "scientific_name": "Piper lolot",
        "other_names": "Tất bát",
        "family": "Piperaceae (Hồ tiêu)",
        "description": "Thân bò, lá hình tim, xanh đậm",
        "parts_used": "Lá",
        "usage": "Đau khớp, đau bụng",
        "preparation": "Lá tươi nấu nước uống hoặc cuốn thịt nướng. Sắc 15-30g/ngày.",
        "symptoms": "đau khớp, đau bụng, phong thấp, đau lưng, tay chân lạnh",
        "image_url": "/images/thumbnails/08_la_lot.jpg",
        "distribution": "Trồng phổ biến khắp Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"}
        ],
    },
    # 9. Kinh giới
    {
        "name": "Kinh giới",
        "scientific_name": "Elsholtzia ciliata",
        "other_names": "Khương giới",
        "family": "Lamiaceae (Hoa môi)",
        "description": "Thân vuông, lá răng cưa",
        "parts_used": "Toàn cây",
        "usage": "Cảm cúm",
        "preparation": "Toàn cây sắc nước uống hoặc nấu cháo giải cảm. 8-16g/ngày.",
        "symptoms": "cảm cúm, sốt, đau đầu, phát ban, dị ứng, ngứa",
        "image_url": "/images/thumbnails/09_kinh_gioi.jpg",
        "distribution": "Trồng phổ biến miền Bắc Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 20.8449, "lng": 106.6881, "location": "Hải Phòng"},
            {"lat": 20.4388, "lng": 106.1621, "location": "Nam Định"}
        ],
    },
    # 10. Húng chanh
    {
        "name": "Húng chanh",
        "scientific_name": "Plectranthus amboinicus",
        "other_names": "Tần dày lá, Rau tần",
        "family": "Lamiaceae (Hoa môi)",
        "description": "Lá dày, mọng nước, mép khía",
        "parts_used": "Lá",
        "usage": "Ho, viêm họng",
        "preparation": "Lá tươi hấp đường phèn, giã lấy nước uống.",
        "symptoms": "ho, viêm họng, ho có đờm, cảm cúm, khàn giọng",
        "image_url": "/images/thumbnails/10_hung_chanh.jpg",
        "distribution": "Trồng phổ biến khắp Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"}
        ],
    },
    # 11. Bạc hà
    {
        "name": "Bạc hà",
        "scientific_name": "Mentha arvensis",
        "other_names": "Bạc hà nam, Bạc hà Á",
        "family": "Lamiaceae (Hoa môi)",
        "description": "Thân bò, lá xanh, mùi thơm",
        "parts_used": "Lá",
        "usage": "Giải cảm",
        "preparation": "Lá tươi nấu nước xông. Tinh dầu bạc hà bôi ngoài. Trà bạc hà.",
        "symptoms": "cảm cúm, đau đầu, nghẹt mũi, sốt, đau bụng, buồn nôn",
        "image_url": "/images/thumbnails/11_bac_ha.jpg",
        "distribution": "Trồng phổ biến khắp cả nước, nhiều ở đồng bằng Bắc Bộ.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 20.9373, "lng": 106.3146, "location": "Hải Dương"},
            {"lat": 20.8449, "lng": 106.6881, "location": "Hải Phòng"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"}
        ],
    },
    # 12. Ngải cứu
    {
        "name": "Ngải cứu",
        "scientific_name": "Artemisia vulgaris",
        "other_names": "Thuốc cứu, Ngải diệp",
        "family": "Asteraceae (Cúc)",
        "description": "Lá xẻ lông chim, mặt dưới trắng",
        "parts_used": "Lá",
        "usage": "Đau bụng kinh",
        "preparation": "Lá tươi nấu trứng gà, sắc nước uống. 10-15g/ngày.",
        "symptoms": "đau bụng kinh, kinh nguyệt không đều, đau nhức xương khớp, cầm máu",
        "image_url": "/images/thumbnails/12_ngai_cuu.jpg",
        "distribution": "Mọc hoang và trồng phổ biến khắp Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 20.4388, "lng": 106.1621, "location": "Nam Định"}
        ],
    },
    # 13. Cỏ mần trầu
    {
        "name": "Cỏ mần trầu",
        "scientific_name": "Eleusine indica",
        "other_names": "Cỏ vườn trầu, Ngưu cân thảo",
        "family": "Poaceae (Hòa thảo)",
        "description": "Thân bò, rễ chùm",
        "parts_used": "Toàn cây",
        "usage": "Thanh nhiệt",
        "preparation": "Toàn cây tươi sắc nước uống, 30-60g/ngày.",
        "symptoms": "thanh nhiệt, giải độc, sốt, cao huyết áp, viêm gan",
        "image_url": "/images/thumbnails/13_co_man_trau.jpg",
        "distribution": "Mọc hoang khắp Việt Nam, dễ tìm ở ven đường, bãi cỏ.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"}
        ],
    },
    # 14. Chó đẻ răng cưa
    {
        "name": "Chó đẻ răng cưa",
        "scientific_name": "Phyllanthus urinaria",
        "other_names": "Diệp hạ châu, Cam kiềm",
        "family": "Phyllanthaceae (Diệp hạ châu)",
        "description": "Thân nhỏ, lá kép",
        "parts_used": "Toàn cây",
        "usage": "Viêm gan B",
        "preparation": "Toàn cây tươi hoặc khô sắc nước uống, 30-50g tươi/ngày.",
        "symptoms": "viêm gan, viêm gan B, vàng da, sỏi thận, sỏi mật, tiểu buốt, nóng gan",
        "image_url": "/images/thumbnails/14_cho_de_rang_cua.jpg",
        "distribution": "Mọc hoang khắp Việt Nam, nhiều ở vùng đồng bằng và trung du.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 16.4637, "lng": 107.5909, "location": "Huế"},
            {"lat": 15.9752, "lng": 108.2530, "location": "Đà Nẵng"}
        ],
    },
    # 15. Nhọ nồi
    {
        "name": "Nhọ nồi",
        "scientific_name": "Eclipta prostrata",
        "other_names": "Cỏ mực, Hạn liên thảo",
        "family": "Asteraceae (Cúc)",
        "description": "Thân mềm, hoa trắng",
        "parts_used": "Toàn cây",
        "usage": "Cầm máu",
        "preparation": "Toàn cây tươi giã lấy nước uống hoặc đắp ngoài. 20-40g/ngày.",
        "symptoms": "cầm máu, chảy máu cam, rong kinh, bổ thận, đen tóc",
        "image_url": "/images/thumbnails/15_nho_noi.jpg",
        "distribution": "Mọc hoang khắp Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"}
        ],
    },
    # 16. Trinh nữ (Mắc cỡ)
    {
        "name": "Trinh nữ",
        "scientific_name": "Mimosa pudica",
        "other_names": "Mắc cỡ, Xấu hổ, Hàm tu thảo",
        "family": "Fabaceae (Đậu)",
        "description": "Lá cụp khi chạm, thân gai",
        "parts_used": "Rễ, lá",
        "usage": "An thần",
        "preparation": "Rễ hoặc toàn cây sắc nước uống, 15-30g/ngày.",
        "symptoms": "mất ngủ, an thần, lo âu, đau nhức, suy nhược thần kinh",
        "image_url": "/images/thumbnails/16_trinh_nu_mac_co.jpg",
        "distribution": "Mọc hoang khắp Việt Nam, nhiều ở ven đường, bờ ruộng.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"}
        ],
    },
    # 17. Dừa cạn
    {
        "name": "Dừa cạn",
        "scientific_name": "Catharanthus roseus",
        "other_names": "Hoa trường xuân, Bông dừa",
        "family": "Apocynaceae (Trúc đào)",
        "description": "Hoa hồng/tím, lá xanh bóng",
        "parts_used": "Toàn cây",
        "usage": "Hạ đường huyết",
        "preparation": "Lá và rễ sắc nước uống, 10-20g/ngày.",
        "symptoms": "tiểu đường, đường huyết cao, huyết áp cao",
        "image_url": "/images/thumbnails/17_dua_can.jpg",
        "distribution": "Trồng làm cây cảnh và thuốc khắp Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"}
        ],
    },
    # 18. Hoàn ngọc
    {
        "name": "Hoàn ngọc",
        "scientific_name": "Pseuderanthemum palatiferum",
        "other_names": "Nhật nguyệt, Xuân hoa",
        "family": "Acanthaceae (Ô rô)",
        "description": "Lá thuôn, thân gỗ nhỏ",
        "parts_used": "Lá",
        "usage": "Giải độc",
        "preparation": "Lá tươi giã lấy nước uống hoặc sắc nước, 20-30g/ngày.",
        "symptoms": "giải độc, viêm dạ dày, viêm đại tràng, táo bón, mụn nhọt",
        "image_url": "/images/thumbnails/18_hoan_ngoc.jpg",
        "distribution": "Trồng nhiều ở miền Nam và miền Trung Việt Nam.",
        "distribution_coords": [
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"}
        ],
    },
    # 19. Xạ đen
    {
        "name": "Xạ đen",
        "scientific_name": "Celastrus hindsii",
        "other_names": "Bạch vạn hoa, Dây gối",
        "family": "Celastraceae (Chân danh)",
        "description": "Thân leo, lá xanh đậm",
        "parts_used": "Lá, thân",
        "usage": "Hỗ trợ điều trị ung thư",
        "preparation": "Thân, lá khô sắc nước uống, 20-30g/ngày.",
        "symptoms": "u xơ, u nang, hỗ trợ ung thư, giải độc, nóng trong, miễn dịch kém",
        "image_url": "/images/thumbnails/19_xa_den.jpg",
        "distribution": "Mọc hoang ở rừng núi phía Bắc: Hòa Bình, Ninh Bình, Thanh Hóa.",
        "distribution_coords": [
            {"lat": 20.8171, "lng": 105.3383, "location": "Hòa Bình"},
            {"lat": 20.2506, "lng": 105.9744, "location": "Ninh Bình"},
            {"lat": 19.8067, "lng": 105.7852, "location": "Thanh Hóa"}
        ],
    },
    # 20. Cỏ ngọt
    {
        "name": "Cỏ ngọt",
        "scientific_name": "Stevia rebaudiana",
        "other_names": "Cỏ đường, Stevia",
        "family": "Asteraceae (Cúc)",
        "description": "Lá nhỏ, vị ngọt",
        "parts_used": "Lá",
        "usage": "Tiểu đường",
        "preparation": "Lá phơi khô pha trà uống thay đường.",
        "symptoms": "tiểu đường, đường huyết cao, béo phì, thay thế đường",
        "image_url": "/images/thumbnails/20_co_ngot.jpg",
        "distribution": "Trồng ở một số tỉnh miền Bắc và Tây Nguyên.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 11.9404, "lng": 108.4583, "location": "Đà Lạt, Lâm Đồng"}
        ],
    },
    # 21. Kim ngân hoa
    {
        "name": "Kim ngân hoa",
        "scientific_name": "Lonicera japonica",
        "other_names": "Nhẫn đông, Bạc ngân hoa",
        "family": "Caprifoliaceae (Kim ngân)",
        "description": "Dây leo, hoa trắng vàng",
        "parts_used": "Hoa, lá",
        "usage": "Thanh nhiệt",
        "preparation": "Hoa phơi khô sắc nước uống, 10-20g/ngày. Pha trà kim ngân.",
        "symptoms": "cảm cúm, viêm họng, sốt, mụn nhọt, ban sởi, thanh nhiệt",
        "image_url": "/images/thumbnails/21_kim_ngan_hoa.jpg",
        "distribution": "Mọc hoang ở vùng núi phía Bắc, trồng ở nhiều nơi.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 21.3069, "lng": 105.5986, "location": "Thái Nguyên"},
            {"lat": 22.3363, "lng": 103.8438, "location": "Lào Cai"}
        ],
    },
    # 22. Ké đầu ngựa
    {
        "name": "Ké đầu ngựa",
        "scientific_name": "Xanthium strumarium",
        "other_names": "Thương nhĩ tử, Xương nhĩ",
        "family": "Asteraceae (Cúc)",
        "description": "Lá to, quả gai",
        "parts_used": "Quả",
        "usage": "Viêm xoang",
        "preparation": "Quả sao vàng, sắc nước uống, 6-12g/ngày.",
        "symptoms": "viêm xoang, ngạt mũi, đau đầu, dị ứng, mề đay",
        "image_url": "/images/thumbnails/22_ke_dau_ngua.jpg",
        "distribution": "Mọc hoang ở nhiều nơi, đặc biệt vùng đồi núi phía Bắc.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 21.3069, "lng": 105.5986, "location": "Thái Nguyên"},
            {"lat": 20.8171, "lng": 105.3383, "location": "Hòa Bình"}
        ],
    },
    # 23. Bồ công anh
    {
        "name": "Bồ công anh",
        "scientific_name": "Taraxacum officinale",
        "other_names": "Diếp trời, Rau mũi mác",
        "family": "Asteraceae (Cúc)",
        "description": "Lá mác, hoa vàng",
        "parts_used": "Toàn cây",
        "usage": "Mát gan",
        "preparation": "Cây tươi giã nát đắp ngoài. Sắc nước uống 20-40g khô/ngày.",
        "symptoms": "mụn nhọt, viêm họng, mát gan, sưng đau, nóng trong, giải độc",
        "image_url": "/images/thumbnails/23_bo_cong_anh.jpg",
        "distribution": "Mọc hoang khắp nơi, nhiều ở vùng đồng bằng và trung du Bắc Bộ.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 21.3069, "lng": 105.5986, "location": "Thái Nguyên"},
            {"lat": 20.4388, "lng": 106.1621, "location": "Nam Định"}
        ],
    },
    # 24. Ích mẫu
    {
        "name": "Ích mẫu",
        "scientific_name": "Leonurus japonicus",
        "other_names": "Sung úy, Chói đèn",
        "family": "Lamiaceae (Hoa môi)",
        "description": "Thân vuông, hoa tím",
        "parts_used": "Toàn cây",
        "usage": "Điều hòa kinh nguyệt",
        "preparation": "Toàn cây sắc nước uống, 8-16g/ngày. Viên nén ích mẫu.",
        "symptoms": "kinh nguyệt không đều, đau bụng kinh, sau sinh, huyết áp cao, phù nề",
        "image_url": "/images/thumbnails/24_ich_mau.jpg",
        "distribution": "Mọc hoang và trồng khắp Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 20.4388, "lng": 106.1621, "location": "Nam Định"}
        ],
    },
    # 25. Mã đề
    {
        "name": "Mã đề",
        "scientific_name": "Plantago major",
        "other_names": "Xa tiền thảo, Bông mã đề",
        "family": "Plantaginaceae (Mã đề)",
        "description": "Lá bầu dục, gân song song",
        "parts_used": "Lá, hạt",
        "usage": "Viêm tiết niệu",
        "preparation": "Toàn cây tươi hoặc khô sắc nước uống, 20-40g/ngày.",
        "symptoms": "tiểu buốt, sỏi thận, viêm tiết niệu, ho có đờm, nóng trong, phù nề",
        "image_url": "/images/thumbnails/25_ma_de.jpg",
        "distribution": "Mọc hoang khắp Việt Nam, dễ tìm ở ven đường, bãi cỏ.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"}
        ],
    },
    # 26. Cỏ tranh
    {
        "name": "Cỏ tranh",
        "scientific_name": "Imperata cylindrica",
        "other_names": "Bạch mao căn, Mao căn",
        "family": "Poaceae (Hòa thảo)",
        "description": "Lá dài sắc, rễ trắng",
        "parts_used": "Rễ",
        "usage": "Lợi tiểu",
        "preparation": "Rễ tươi hoặc khô sắc nước uống, 20-40g/ngày.",
        "symptoms": "lợi tiểu, tiểu buốt, tiểu ra máu, thanh nhiệt, sốt nóng",
        "image_url": "/images/thumbnails/26_co_tranh.jpg",
        "distribution": "Mọc hoang khắp Việt Nam, nhiều ở vùng đồi trọc.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 18.6790, "lng": 105.6813, "location": "Nghệ An"},
            {"lat": 14.0583, "lng": 108.2772, "location": "Gia Lai"}
        ],
    },
    # 27. Muồng trâu
    {
        "name": "Muồng trâu",
        "scientific_name": "Cassia alata",
        "other_names": "Muồng xức lác, Muồng lác",
        "family": "Fabaceae (Đậu)",
        "description": "Lá kép, hoa vàng",
        "parts_used": "Lá",
        "usage": "Nhuận tràng",
        "preparation": "Lá tươi hoặc khô sắc nước uống, 20-30g/ngày.",
        "symptoms": "táo bón, nhuận tràng, hắc lào, lang ben, nấm da",
        "image_url": "/images/thumbnails/27_muong_trau.jpg",
        "distribution": "Mọc hoang và trồng ở miền Nam Việt Nam.",
        "distribution_coords": [
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"},
            {"lat": 10.2518, "lng": 106.3754, "location": "Bến Tre"}
        ],
    },
    # 28. Lược vàng
    {
        "name": "Lược vàng",
        "scientific_name": "Callisia fragrans",
        "other_names": "Lan vòi, Cây bạch tuộc",
        "family": "Commelinaceae (Thài lài)",
        "description": "Lá dài, mọng nước",
        "parts_used": "Lá",
        "usage": "Viêm khớp",
        "preparation": "Lá tươi giã đắp ngoài hoặc ngâm rượu xoa bóp.",
        "symptoms": "viêm khớp, đau khớp, đau nhức, bầm tím, vết thương",
        "image_url": "/images/thumbnails/28_luoc_vang.jpg",
        "distribution": "Trồng nhiều ở miền Bắc Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 20.8449, "lng": 106.6881, "location": "Hải Phòng"},
            {"lat": 21.3069, "lng": 105.5986, "location": "Thái Nguyên"}
        ],
    },
    # 29. Thiên lý
    {
        "name": "Thiên lý",
        "scientific_name": "Telosma cordata",
        "other_names": "Hoa thiên lý, Dạ lý hương",
        "family": "Asclepiadaceae (Thiên lý)",
        "description": "Dây leo, hoa xanh",
        "parts_used": "Lá, hoa",
        "usage": "An thần",
        "preparation": "Hoa và lá nấu canh ăn hoặc sắc nước uống.",
        "symptoms": "mất ngủ, an thần, lo âu, stress, suy nhược",
        "image_url": "/images/thumbnails/29_thien_ly.jpg",
        "distribution": "Trồng phổ biến khắp Việt Nam, làm cây cảnh và cây thuốc.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 16.4637, "lng": 107.5909, "location": "Huế"}
        ],
    },
    # 30. Khổ qua
    {
        "name": "Khổ qua",
        "scientific_name": "Momordica charantia",
        "other_names": "Mướp đắng, Cẩm lệ chi",
        "family": "Cucurbitaceae (Bầu bí)",
        "description": "Dây leo, quả sần",
        "parts_used": "Quả",
        "usage": "Tiểu đường",
        "preparation": "Quả nấu canh, ép nước uống, phơi khô pha trà.",
        "symptoms": "tiểu đường, đường huyết cao, thanh nhiệt, giải độc, mụn nhọt",
        "image_url": "/images/thumbnails/30_kho_qua.jpg",
        "distribution": "Trồng phổ biến khắp Việt Nam.",
        "distribution_coords": [
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"},
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"}
        ],
    },
    # 31. Sung
    {
        "name": "Sung",
        "scientific_name": "Ficus racemosa",
        "other_names": "Vô hoa quả, Ưu đàm",
        "family": "Moraceae (Dâu tằm)",
        "description": "Thân gỗ, quả tròn",
        "parts_used": "Quả",
        "usage": "Trĩ",
        "preparation": "Quả tươi nấu nước uống hoặc sắc dùng ngâm rửa.",
        "symptoms": "trĩ, táo bón, lở loét, mụn nhọt, viêm ruột",
        "image_url": "/images/thumbnails/31_sung.jpg",
        "distribution": "Mọc hoang và trồng ở nhiều nơi, nhiều ở miền Nam.",
        "distribution_coords": [
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"},
            {"lat": 10.2518, "lng": 106.3754, "location": "Bến Tre"}
        ],
    },
    # 32. Vối
    {
        "name": "Vối",
        "scientific_name": "Cleistocalyx operculatus",
        "other_names": "Vối nhà, Mần sành",
        "family": "Myrtaceae (Sim)",
        "description": "Lá to, dày",
        "parts_used": "Lá",
        "usage": "Thanh nhiệt",
        "preparation": "Lá và nụ hoa phơi khô nấu nước uống như trà.",
        "symptoms": "thanh nhiệt, tiêu hóa kém, đầy bụng, giải khát, mát gan",
        "image_url": "/images/thumbnails/32_voi.jpg",
        "distribution": "Trồng nhiều ở miền Bắc Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 20.9373, "lng": 106.3146, "location": "Hải Dương"},
            {"lat": 21.1781, "lng": 106.0645, "location": "Bắc Giang"}
        ],
    },
    # 33. Sâm đất
    {
        "name": "Sâm đất",
        "scientific_name": "Boerhavia diffusa",
        "other_names": "Sâm nam, Nhân sâm đất",
        "family": "Nyctaginaceae (Hoa phấn)",
        "description": "Rễ củ, thân bò",
        "parts_used": "Rễ",
        "usage": "Bồi bổ",
        "preparation": "Rễ củ nấu canh, hầm gà hoặc sắc nước uống.",
        "symptoms": "suy nhược, mệt mỏi, bồi bổ sức khỏe, thiếu máu, kém ăn",
        "image_url": "/images/thumbnails/33_sam_dat.jpg",
        "distribution": "Mọc hoang và trồng ở nhiều tỉnh thành.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 18.6790, "lng": 105.6813, "location": "Nghệ An"}
        ],
    },
    # 34. Đinh lăng
    {
        "name": "Đinh lăng",
        "scientific_name": "Polyscias fruticosa",
        "other_names": "Cây gỏi cá, Nam dương sâm",
        "family": "Araliaceae (Nhân sâm)",
        "description": "Lá xẻ, thân gỗ",
        "parts_used": "Lá, rễ",
        "usage": "Tăng đề kháng",
        "preparation": "Rễ, lá sắc nước uống. Rễ ngâm rượu. Lá non ăn sống gỏi cá.",
        "symptoms": "mệt mỏi, suy nhược, stress, giảm trí nhớ, tăng đề kháng, dị ứng",
        "image_url": "/images/thumbnails/34_dinh_lang.jpg",
        "distribution": "Trồng phổ biến khắp Việt Nam, làm cây cảnh và cây thuốc.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"}
        ],
    },
    # 35. Cúc tần
    {
        "name": "Cúc tần",
        "scientific_name": "Pluchea indica",
        "other_names": "Cúc tần dại, Từ bi",
        "family": "Asteraceae (Cúc)",
        "description": "Lá dày, mùi thơm",
        "parts_used": "Lá",
        "usage": "Đau nhức",
        "preparation": "Lá tươi nấu nước xông hoặc sắc nước uống, 15-30g/ngày.",
        "symptoms": "đau nhức, cảm cúm, đau đầu, sốt, phong thấp",
        "image_url": "/images/thumbnails/35_cuc_tan.jpg",
        "distribution": "Mọc hoang phổ biến ở miền Nam Việt Nam.",
        "distribution_coords": [
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"},
            {"lat": 10.2518, "lng": 106.3754, "location": "Bến Tre"}
        ],
    },
    # 36. Me đất
    {
        "name": "Me đất",
        "scientific_name": "Oxalis corniculata",
        "other_names": "Chua me đất, Tạc tương thảo",
        "family": "Oxalidaceae (Me đất)",
        "description": "Lá chẻ 3, vị chua",
        "parts_used": "Toàn cây",
        "usage": "Thanh nhiệt",
        "preparation": "Toàn cây tươi sắc nước uống, 20-40g/ngày.",
        "symptoms": "thanh nhiệt, giải độc, viêm họng, tiêu chảy, mụn nhọt, sốt",
        "image_url": "/images/thumbnails/36_me_dat.jpg",
        "distribution": "Mọc hoang khắp Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"}
        ],
    },
    # 37. Lạc tiên
    {
        "name": "Lạc tiên",
        "scientific_name": "Passiflora foetida",
        "other_names": "Nhãn lồng, Chùm bao, Lồng đèn",
        "family": "Passifloraceae (Lạc tiên)",
        "description": "Dây leo, hoa trắng tím",
        "parts_used": "Toàn cây",
        "usage": "Mất ngủ",
        "preparation": "Toàn cây sắc nước uống, 20-40g/ngày. Quả chín ăn được.",
        "symptoms": "mất ngủ, lo âu, stress, hồi hộp, đau đầu, huyết áp cao",
        "image_url": "/images/thumbnails/37_lac_tien.jpg",
        "distribution": "Mọc hoang khắp Việt Nam, nhiều ở miền Nam.",
        "distribution_coords": [
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"},
            {"lat": 10.3600, "lng": 107.0843, "location": "Bà Rịa - Vũng Tàu"}
        ],
    },
    # 38. Chè xanh
    {
        "name": "Chè xanh",
        "scientific_name": "Camellia sinensis",
        "other_names": "Trà xanh, Trà ta",
        "family": "Theaceae (Chè)",
        "description": "Lá thuôn, xanh bóng",
        "parts_used": "Lá",
        "usage": "Chống oxy hóa",
        "preparation": "Lá tươi hoặc khô hãm nước uống. Trà xanh hàng ngày.",
        "symptoms": "chống oxy hóa, mệt mỏi, giảm cân, thanh nhiệt, tỉnh táo",
        "image_url": "/images/thumbnails/38_che_xanh.jpg",
        "distribution": "Trồng nhiều ở Thái Nguyên, Hà Giang, Lâm Đồng.",
        "distribution_coords": [
            {"lat": 21.3069, "lng": 105.5986, "location": "Thái Nguyên"},
            {"lat": 22.8233, "lng": 104.9837, "location": "Hà Giang"},
            {"lat": 11.9404, "lng": 108.4583, "location": "Đà Lạt, Lâm Đồng"},
            {"lat": 21.7091, "lng": 104.8881, "location": "Yên Bái"}
        ],
    },
    # 39. Dâu tằm
    {
        "name": "Dâu tằm",
        "scientific_name": "Morus alba",
        "other_names": "Dâu ta, Tang",
        "family": "Moraceae (Dâu tằm)",
        "description": "Lá to, quả tím",
        "parts_used": "Lá, quả",
        "usage": "Tiểu đường",
        "preparation": "Lá phơi khô sắc nước uống, quả chín ăn hoặc ngâm rượu.",
        "symptoms": "tiểu đường, đường huyết cao, ho, sốt, đau đầu, hoa mắt",
        "image_url": "/images/thumbnails/39_dau_tam.jpg",
        "distribution": "Trồng nhiều ở miền Bắc và miền Trung.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 11.9404, "lng": 108.4583, "location": "Đà Lạt, Lâm Đồng"},
            {"lat": 15.8801, "lng": 108.3380, "location": "Quảng Nam"}
        ],
    },
    # 40. Sài đất
    {
        "name": "Sài đất",
        "scientific_name": "Wedelia chinensis",
        "other_names": "Húng trám, Cúc nháp",
        "family": "Asteraceae (Cúc)",
        "description": "Thân bò, hoa vàng",
        "parts_used": "Toàn cây",
        "usage": "Viêm họng",
        "preparation": "Toàn cây tươi giã nát đắp hoặc sắc nước uống, 20-40g/ngày.",
        "symptoms": "viêm họng, mụn nhọt, chàm, viêm da, sốt, thanh nhiệt",
        "image_url": "/images/thumbnails/40_sai_dat.jpg",
        "distribution": "Mọc hoang khắp Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"}
        ],
    },
    # 41. Rau sam
    {
        "name": "Rau sam",
        "scientific_name": "Portulaca oleracea",
        "other_names": "Mã xỉ hiện, Sam đất",
        "family": "Portulacaceae (Rau sam)",
        "description": "Thân mọng, lá nhỏ",
        "parts_used": "Toàn cây",
        "usage": "Tiêu viêm",
        "preparation": "Toàn cây tươi sắc nước uống hoặc nấu canh, 30-60g/ngày.",
        "symptoms": "tiêu viêm, tiêu chảy, lỵ, mụn nhọt, viêm ruột, giải độc",
        "image_url": "/images/thumbnails/41_rau_sam.jpg",
        "distribution": "Mọc hoang khắp Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"}
        ],
    },
    # 42. Ngũ gia bì
    {
        "name": "Ngũ gia bì",
        "scientific_name": "Acanthopanax trifoliatus",
        "other_names": "Ngũ gia bì chân chim, Chân chim",
        "family": "Araliaceae (Nhân sâm)",
        "description": "Lá kép chân vịt",
        "parts_used": "Vỏ, rễ",
        "usage": "Đau khớp",
        "preparation": "Vỏ rễ phơi khô sắc nước uống hoặc ngâm rượu, 10-15g/ngày.",
        "symptoms": "đau khớp, phong thấp, đau lưng, mỏi gối, tê bì chân tay",
        "image_url": "/images/thumbnails/42_ngu_gia_bi.jpg",
        "distribution": "Mọc hoang ở rừng núi phía Bắc Việt Nam.",
        "distribution_coords": [
            {"lat": 22.3363, "lng": 103.8438, "location": "Sa Pa, Lào Cai"},
            {"lat": 22.8233, "lng": 104.9837, "location": "Hà Giang"},
            {"lat": 20.8171, "lng": 105.3383, "location": "Hòa Bình"}
        ],
    },
    # 43. Xuyên tâm liên
    {
        "name": "Xuyên tâm liên",
        "scientific_name": "Andrographis paniculata",
        "other_names": "Công cộng, Cỏ đắng",
        "family": "Acanthaceae (Ô rô)",
        "description": "Thân thảo, vị đắng",
        "parts_used": "Toàn cây",
        "usage": "Kháng viêm",
        "preparation": "Toàn cây phơi khô sắc nước uống, 10-20g/ngày. Viên nén.",
        "symptoms": "viêm họng, cảm cúm, sốt, kháng viêm, tiêu chảy, viêm phổi",
        "image_url": "/images/thumbnails/43_xuyen_tam_lien.jpg",
        "distribution": "Trồng ở nhiều tỉnh miền Bắc và miền Trung.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 18.6790, "lng": 105.6813, "location": "Nghệ An"},
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"}
        ],
    },
    # 44. Thìa canh
    {
        "name": "Thìa canh",
        "scientific_name": "Gymnema sylvestre",
        "other_names": "Dây muôi, Dây thìa canh",
        "family": "Asclepiadaceae (Thiên lý)",
        "description": "Dây leo, lá bầu dục",
        "parts_used": "Lá",
        "usage": "Tiểu đường",
        "preparation": "Lá phơi khô sắc nước uống hoặc hãm trà, 10-20g/ngày.",
        "symptoms": "tiểu đường, đường huyết cao, mỡ máu, béo phì",
        "image_url": "/images/thumbnails/44_thia_canh.jpg",
        "distribution": "Mọc hoang ở vùng núi phía Bắc và miền Trung.",
        "distribution_coords": [
            {"lat": 20.8171, "lng": 105.3383, "location": "Hòa Bình"},
            {"lat": 20.2506, "lng": 105.9744, "location": "Ninh Bình"},
            {"lat": 18.6790, "lng": 105.6813, "location": "Nghệ An"}
        ],
    },
    # 45. Bạch hoa xà
    {
        "name": "Bạch hoa xà",
        "scientific_name": "Hedyotis diffusa",
        "other_names": "Bạch hoa xà thiệt thảo, Lưỡi rắn",
        "family": "Rubiaceae (Cà phê)",
        "description": "Thân bò",
        "parts_used": "Toàn cây",
        "usage": "Thanh nhiệt",
        "preparation": "Toàn cây phơi khô sắc nước uống, 15-30g/ngày.",
        "symptoms": "thanh nhiệt, giải độc, viêm ruột thừa, viêm phổi, hỗ trợ ung thư",
        "image_url": "/images/thumbnails/45_bach_hoa_xa.jpg",
        "distribution": "Mọc hoang ở nhiều nơi, nhiều ở miền Bắc.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 21.3069, "lng": 105.5986, "location": "Thái Nguyên"},
            {"lat": 20.4388, "lng": 106.1621, "location": "Nam Định"}
        ],
    },
    # 46. Gấc
    {
        "name": "Gấc",
        "scientific_name": "Momordica cochinchinensis",
        "other_names": "Mộc miết tử, Mác khảu",
        "family": "Cucurbitaceae (Bầu bí)",
        "description": "Dây leo, quả gai",
        "parts_used": "Quả",
        "usage": "Bổ mắt",
        "preparation": "Màng đỏ hạt gấc nấu xôi, ép dầu. Dầu gấc uống hoặc bôi ngoài.",
        "symptoms": "mờ mắt, bổ mắt, thiếu vitamin A, vết thương, bỏng, da khô",
        "image_url": "/images/thumbnails/46_gac.jpg",
        "distribution": "Trồng phổ biến khắp Việt Nam, nhiều ở miền Bắc.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 20.9373, "lng": 106.3146, "location": "Hải Dương"},
            {"lat": 18.6790, "lng": 105.6813, "location": "Nghệ An"},
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"}
        ],
    },
    # 47. Mơ lông
    {
        "name": "Mơ lông",
        "scientific_name": "Paederia foetida",
        "other_names": "Mơ tam thể, Dây thối địt",
        "family": "Rubiaceae (Cà phê)",
        "description": "Lá có lông, mùi hôi",
        "parts_used": "Lá",
        "usage": "Trị ho",
        "preparation": "Lá tươi cuốn thịt nướng, hoặc giã lấy nước uống.",
        "symptoms": "ho, tiêu chảy, lỵ, đau bụng, kiết lỵ, đầy hơi",
        "image_url": "/images/thumbnails/47_mo_long.jpg",
        "distribution": "Mọc hoang và trồng ở miền Bắc Việt Nam.",
        "distribution_coords": [
            {"lat": 21.0285, "lng": 105.8542, "location": "Hà Nội"},
            {"lat": 20.8449, "lng": 106.6881, "location": "Hải Phòng"},
            {"lat": 20.4388, "lng": 106.1621, "location": "Nam Định"}
        ],
    },
    # 48. Nhàu
    {
        "name": "Nhàu",
        "scientific_name": "Morinda citrifolia",
        "other_names": "Trái nhàu, Noni",
        "family": "Rubiaceae (Cà phê)",
        "description": "Thân gỗ nhỏ, quả trắng",
        "parts_used": "Quả, rễ",
        "usage": "Huyết áp",
        "preparation": "Quả chín ngâm mật ong hoặc ép nước uống. Rễ sắc nước.",
        "symptoms": "huyết áp cao, đau nhức, mệt mỏi, tăng cường miễn dịch",
        "image_url": "/images/thumbnails/48_nhau.jpg",
        "distribution": "Trồng nhiều ở miền Nam và miền Trung.",
        "distribution_coords": [
            {"lat": 10.8231, "lng": 106.6297, "location": "TP. Hồ Chí Minh"},
            {"lat": 10.0452, "lng": 105.7469, "location": "Cần Thơ"},
            {"lat": 13.0882, "lng": 109.2930, "location": "Phú Yên"}
        ],
    },
    # 49. Cây vằng
    {
        "name": "Cây vằng",
        "scientific_name": "Jasminum subtriplinerve",
        "other_names": "Vằng sẻ, Lài ba gân",
        "family": "Oleaceae (Nhài)",
        "description": "Lá nhỏ, thân gỗ",
        "parts_used": "Lá",
        "usage": "Lợi sữa",
        "preparation": "Lá phơi khô nấu nước uống thay trà.",
        "symptoms": "lợi sữa, sau sinh, thanh nhiệt, giải độc, tiêu hóa kém",
        "image_url": "/images/thumbnails/49_cay_vang.jpg",
        "distribution": "Trồng nhiều ở miền Trung Việt Nam.",
        "distribution_coords": [
            {"lat": 16.4637, "lng": 107.5909, "location": "Huế"},
            {"lat": 15.8801, "lng": 108.3380, "location": "Quảng Nam"},
            {"lat": 18.6790, "lng": 105.6813, "location": "Nghệ An"}
        ],
    },
    # 50. Dấp cá biển
    {
        "name": "Dấp cá biển",
        "scientific_name": "Houttuynia maritima",
        "other_names": "Giấp cá biển",
        "family": "Saururaceae (Lá giấp)",
        "description": "Lá dày, thân bò",
        "parts_used": "Lá",
        "usage": "Giải độc",
        "preparation": "Lá tươi giã nát đắp ngoài hoặc sắc nước uống.",
        "symptoms": "giải độc, kháng viêm, mụn nhọt, nóng trong, viêm da",
        "image_url": "/images/thumbnails/50_cay_dap_ca_bien.jpg",
        "distribution": "Mọc hoang ở vùng ven biển miền Trung.",
        "distribution_coords": [
            {"lat": 16.0544, "lng": 108.2022, "location": "Đà Nẵng"},
            {"lat": 12.2388, "lng": 109.1967, "location": "Nha Trang"},
            {"lat": 13.0882, "lng": 109.2930, "location": "Phú Yên"}
        ],
    },
]


for plant_data in SAMPLE_PLANTS:
    plant_data["distribution"] = "Phân bố tại các tỉnh miền Nam Việt Nam."
    plant_data["distribution_coords"] = build_southern_distribution_coords(plant_data["name"])


def seed_database():
    """Tạo bảng và đồng bộ dữ liệu mẫu (upsert)."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing_by_name = {plant.name: plant for plant in db.query(Plant).all()}
        created_count = 0
        updated_count = 0

        for data in SAMPLE_PLANTS:
            payload = {**data, "letter": get_first_letter(data["name"])}
            existing = existing_by_name.get(data["name"])

            if existing:
                for field, value in payload.items():
                    setattr(existing, field, value)
                updated_count += 1
            else:
                db.add(Plant(**payload))
                created_count += 1

        db.commit()
        total_count = db.query(Plant).count()
        print(
            "Đồng bộ dữ liệu cây thuốc nam thành công! "
            f"Tạo mới: {created_count}, Cập nhật: {updated_count}, Tổng: {total_count}."
        )
    except Exception as e:
        db.rollback()
        print(f"Lỗi: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
