from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from app.database import get_db
from app.models import Plant
from app.schemas import PlantOut, PlantSummary, CatalogGroup

router = APIRouter(prefix="/api/plants", tags=["plants"])


# Thứ tự alphabet tiếng Việt
VIETNAMESE_ALPHABET = [
    "A", "Ă", "Â", "B", "C", "D", "Đ", "E", "Ê", "G", "H",
    "I", "K", "L", "M", "N", "O", "Ô", "Ơ", "P", "Q", "R",
    "S", "T", "U", "Ư", "V", "X", "Y"
]


@router.get("/catalog", response_model=List[CatalogGroup])
def get_catalog(db: Session = Depends(get_db)):
    """Lấy danh mục cây thuốc nam, nhóm theo chữ cái đầu."""
    plants = db.query(Plant).order_by(Plant.name).all()

    groups = {}
    for plant in plants:
        letter = plant.letter.upper()
        if letter not in groups:
            groups[letter] = []
        groups[letter].append(PlantSummary.model_validate(plant))

    # Sắp xếp theo thứ tự alphabet tiếng Việt
    result = []
    for letter in VIETNAMESE_ALPHABET:
        if letter in groups:
            result.append(CatalogGroup(letter=letter, plants=groups[letter]))

    # Thêm các chữ cái không có trong danh sách (nếu có)
    for letter in sorted(groups.keys()):
        if letter not in VIETNAMESE_ALPHABET:
            result.append(CatalogGroup(letter=letter, plants=groups[letter]))

    return result


@router.get("/search", response_model=List[PlantSummary])
def search_plants(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Tìm kiếm cây thuốc nam theo tên."""
    plants = db.query(Plant).filter(
        Plant.name.ilike(f"%{q}%")
    ).order_by(Plant.name).limit(20).all()
    return plants


@router.get("/{plant_id}", response_model=PlantOut)
def get_plant_detail(plant_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết một cây thuốc nam."""
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy cây thuốc nam")
    return plant
