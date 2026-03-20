# 🌿 Cây Thuốc Nam Việt Nam

Ứng dụng web tra cứu và nhận diện cây thuốc nam Việt Nam, tích hợp AI map và mô hình học sâu **DenseNet201** để phân loại ảnh 50 loài cây thuốc.

---

## ✨ Tính năng

- **Danh mục A-Z** — Tra cứu toàn bộ 50 cây thuốc nam theo bảng chữ cái với giao diện accordion
- **Trang chi tiết cây thuốc** — Thông tin đầy đủ: tên khoa học, công dụng, bộ phận dùng, cách chế biến, kèm ảnh và bản đồ phân bố
- **Map AI** — Nhập mô tả triệu chứng hoặc tải ảnh lên để được gợi ý cây thuốc phù hợp
- **Nhận diện ảnh** — Mô hình DenseNet201 phân loại 50 loài cây thuốc từ ảnh chụp
- **Bản đồ phân bố** — Hiển thị vùng phân bố từng cây trên bản đồ Việt Nam (Leaflet + OpenStreetMap)

---

## 🛠️ Công nghệ

| Thành phần | Công nghệ |
|---|---|
| Backend | FastAPI 0.104, Python 3.10+ |
| Database | SQLite + SQLAlchemy 2.0 |
| AI Model | PyTorch, DenseNet201 (50 classes) |
| Frontend | React 18, React Router v6 |
| Bản đồ | Leaflet 1.9, React-Leaflet 4.2 |
| HTTP Client | Axios 1.6 |

---

## 📁 Cấu trúc Project

```
Vietnamese_herbal_medicine/
├── backend/
│   ├── densenet_best.pth           # Trọng số mô hình DenseNet201 đã huấn luyện
│   ├── requirements.txt
│   └── app/
│       ├── main.py                 # FastAPI entry point, CORS, static files
│       ├── database.py             # Cấu hình SQLite
│       ├── models.py               # SQLAlchemy ORM models
│       ├── schemas.py              # Pydantic schemas
│       ├── seed_data.py            # Dữ liệu 50 cây thuốc nam
│       ├── routers/
│       │   ├── plants.py           # API danh mục, tìm kiếm, chi tiết cây
│       │   └── map.py              # API map (text + ảnh)
│       └── services/
│           └── ai_service.py       # DenseNet201 inference + khớp triệu chứng
├── frontend/
│   ├── package.json
│   └── src/
│       ├── App.js                  # Định nghĩa routes
│       ├── components/
│       │   ├── Navbar.js           # Thanh điều hướng
│       │   └── DistributionMap.js  # Bản đồ Leaflet
│       ├── pages/
│       │   ├── CatalogPage.js      # Danh mục A-Z
│       │   ├── PlantDetailPage.js  # Chi tiết cây thuốc
│       │   └── MapPage.js          # Map + bản đồ gợi ý
│       └── services/
│           └── api.js              # Axios API calls
└── README.md
```

---

## 🚀 Hướng dẫn chạy

### Yêu cầu

- Python 3.10+
- Node.js 18+
- File `backend/densenet_best.pth` (trọng số mô hình đã huấn luyện)

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm start
```

Sau khi khởi động:

| Dịch vụ | URL |
|---|---|
| Ứng dụng web | http://localhost:3000 |
| API Documentation (Swagger) | http://localhost:8000/docs |
| API Documentation (ReDoc) | http://localhost:8000/redoc |

---

## 📋 API Endpoints

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/api/plants/catalog` | Danh mục cây thuốc theo bảng chữ cái A-Z |
| GET | `/api/plants/search?q=...` | Tìm kiếm theo tên hoặc triệu chứng |
| GET | `/api/plants/{id}` | Thông tin chi tiết một cây thuốc |
| POST | `/api/map/chat` | Chat với AI (hỗ trợ text và file ảnh) |

### Ví dụ — Gửi ảnh đến map

```bash
curl -X POST http://localhost:8000/api/map/chat \
  -F "message=Cây này chữa bệnh gì?" \
  -F "image=@anh_cay_thuoc.jpg"
```

---

## 🤖 Mô hình AI

### Nhận diện ảnh (`classify_image`)

- Kiến trúc: **DenseNet201** (pretrained ImageNet, fine-tuned 50 classes)
- Input: ảnh bất kỳ định dạng (JPEG, PNG, ...), resize về `224×224`
- Normalization: mean `[0.485, 0.456, 0.406]`, std `[0.229, 0.224, 0.225]`
- Output: top-2 kết quả kèm điểm confidence (softmax)
- Device: tự động dùng GPU nếu có, fallback về CPU

### 50 Loài cây thuốc được nhận diện

| # | Tên cây | # | Tên cây | # | Tên cây |
|---|---|---|---|---|---|
| 1 | Rau má | 18 | Hoàn ngọc | 35 | Cúc tần |
| 2 | Diếp cá | 19 | Xạ đen | 36 | Me đất |
| 3 | Tía tô | 20 | Cỏ ngọt | 37 | Lạc tiên |
| 4 | Sả | 21 | Kim ngân hoa | 38 | Chè xanh |
| 5 | Gừng | 22 | Ké đầu ngựa | 39 | Dâu tằm |
| 6 | Nghệ vàng | 23 | Bồ công anh | 40 | Sài đất |
| 7 | Nghệ đen | 24 | Ích mẫu | 41 | Rau sam |
| 8 | Lá lốt | 25 | Mã đề | 42 | Ngũ gia bì |
| 9 | Kinh giới | 26 | Cỏ tranh | 43 | Xuyên tâm liên |
| 10 | Húng chanh | 27 | Muồng trâu | 44 | Thìa canh |
| 11 | Bạc hà | 28 | Lược vàng | 45 | Bạch hoa xà |
| 12 | Ngải cứu | 29 | Thiên lý | 46 | Gấc |
| 13 | Cỏ mần trầu | 30 | Khổ qua | 47 | Mơ lông |
| 14 | Chó đẻ răng cưa | 31 | Sung | 48 | Nhàu |
| 15 | Nhọ nồi | 32 | Vối | 49 | Cây vằng |
| 16 | Trinh nữ | 33 | Sâm đất | 50 | Dấp cá biển |
| 17 | Dừa cạn | 34 | Đinh lăng | | |

### Khớp triệu chứng (`match_symptoms_to_plants`)

Tìm kiếm cây thuốc phù hợp dựa trên từ khóa triệu chứng trong văn bản người dùng nhập, sử dụng chuẩn hóa Unicode tiếng Việt để khớp không phân biệt dấu.