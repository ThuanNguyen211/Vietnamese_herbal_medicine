from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import engine, Base
from app.routers import plants, map as map_router
from app.seed_data import seed_database

# Tạo bảng và seed dữ liệu
Base.metadata.create_all(bind=engine)
seed_database()

app = FastAPI(
    title="Vietnamese Herbal Medicine API",
    description="API cho ứng dụng Cây thuốc nam Việt Nam",
    version="1.0.0",
)

# CORS - cho phép frontend truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files cho ảnh
images_dir = os.path.join(os.path.dirname(__file__), "..", "images")
os.makedirs(images_dir, exist_ok=True)
app.mount("/images", StaticFiles(directory=images_dir), name="images")

# Routers
app.include_router(plants.router)
app.include_router(map_router.router)
app.include_router(map_router.legacy_router)


@app.get("/")
def root():
    return {
        "message": "Vietnamese Herbal Medicine API",
        "docs": "/docs",
        "endpoints": {
            "catalog": "/api/plants/catalog",
            "search": "/api/plants/search?q=...",
            "detail": "/api/plants/{id}",
            "map": "/api/map/chat",
            "chatbot_legacy": "/api/chatbot/chat",
        }
    }
