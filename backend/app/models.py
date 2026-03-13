from sqlalchemy import Column, Integer, String, Text, Float, JSON
from app.database import Base


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)           # Tên tiếng Việt
    scientific_name = Column(String(300), nullable=True)              # Tên khoa học
    other_names = Column(Text, nullable=True)                        # Tên gọi khác
    family = Column(String(200), nullable=True)                      # Họ thực vật
    description = Column(Text, nullable=True)                        # Mô tả hình dạng
    parts_used = Column(Text, nullable=True)                         # Bộ phận dùng
    usage = Column(Text, nullable=True)                              # Công dụng chữa bệnh
    preparation = Column(Text, nullable=True)                        # Cách dùng / bào chế
    symptoms = Column(Text, nullable=True)                           # Triệu chứng điều trị (comma-separated)
    image_url = Column(String(500), nullable=True)                   # URL ảnh
    # Thông tin phân bố địa lý
    distribution = Column(Text, nullable=True)                       # Mô tả vùng phân bố
    # Danh sách tọa độ phân bố: [{"lat": ..., "lng": ..., "location": "..."}]
    distribution_coords = Column(JSON, nullable=True)
    letter = Column(String(5), nullable=False, index=True)           # Chữ cái đầu (A, B, C...)


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    user_message = Column(Text, nullable=True)
    image_path = Column(String(500), nullable=True)
    bot_response = Column(Text, nullable=True)
    recommended_plant_ids = Column(JSON, nullable=True)
    created_at = Column(String(50), nullable=True)
