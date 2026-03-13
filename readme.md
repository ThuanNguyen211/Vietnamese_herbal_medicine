# 🌿 Vietnamese Herbal Medicine - Cây Thuốc Nam Việt Nam

Web application tra cứu và nhận diện cây thuốc nam Việt Nam, tích hợp AI chatbot.

## 📁 Cấu trúc Project

```
Vietnamese_herbal_medicine/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── database.py         # SQLite database config
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── schemas.py          # Pydantic schemas
│   │   ├── seed_data.py        # Dữ liệu mẫu 22 cây thuốc nam
│   │   ├── routers/
│   │   │   ├── plants.py       # API danh mục & chi tiết cây thuốc
│   │   │   └── chatbot.py      # API chatbot AI
│   │   └── services/
│   │       └── ai_service.py   # 🔌 Placeholder AI model (thay thế khi có model)
│   ├── images/                 # Thư mục chứa ảnh cây thuốc
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # React Frontend
│   ├── public/index.html
│   ├── src/
│   │   ├── App.js              # Routes chính
│   │   ├── components/
│   │   │   ├── Navbar.js       # Thanh điều hướng
│   │   │   └── DistributionMap.js  # Bản đồ Leaflet phân bố cây thuốc
│   │   ├── pages/
│   │   │   ├── CatalogPage.js      # Trang danh mục A-Z (accordion)
│   │   │   ├── PlantDetailPage.js  # Trang chi tiết cây thuốc + bản đồ
│   │   │   └── ChatbotPage.js      # Trang chatbot AI + bản đồ
│   │   └── services/
│   │       └── api.js          # Axios API calls
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🚀 Chạy nhanh (Không Docker)

### Backend (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend (Terminal 2)
```bash
cd frontend
npm install
npm start
```

Truy cập:
- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs

## 🐳 Chạy với Docker
```bash
docker-compose up --build
```

## 🔌 Tích hợp AI Model

Mở file `backend/app/services/ai_service.py` và thay thế 2 hàm placeholder:

### 1. `classify_image()` — Nhận diện ảnh cây thuốc
```python
def classify_image(image_bytes: bytes) -> List[Tuple[str, float]]:
    # Thay bằng model thật (PyTorch, TensorFlow, ONNX...)
    # Return: [("Tên cây", confidence_score), ...]
```

### 2. `match_symptoms_to_plants()` — Gợi ý cây thuốc theo triệu chứng
```python
def match_symptoms_to_plants(symptoms_text: str, db: Session) -> List[Tuple[Plant, float]]:
    # Thay bằng NLP model hoặc embedding search
    # Return: [(Plant object, confidence_score), ...]
```

## 📋 API Endpoints

| Method | Endpoint | Mô tả |
|--------|---------|-------|
| GET | `/api/plants/catalog` | Danh mục A-Z |
| GET | `/api/plants/search?q=...` | Tìm kiếm |
| GET | `/api/plants/{id}` | Chi tiết cây thuốc |
| POST | `/api/chatbot/chat` | Chatbot (text + ảnh) |

## 🗺️ Bản đồ phân bố

Sử dụng Leaflet + OpenStreetMap hiển thị vùng phân bố cây thuốc nam trên bản đồ Việt Nam.
- Trang chi tiết: Bản đồ phân bố từng cây
- Trang chatbot: Bản đồ tổng hợp các cây được gợi ý
