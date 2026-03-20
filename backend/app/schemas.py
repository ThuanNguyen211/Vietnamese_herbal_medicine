from pydantic import BaseModel
from typing import Optional, List


# ============ Plant Schemas ============
class DistributionCoord(BaseModel):
    lat: float
    lng: float
    location: str


class PlantBase(BaseModel):
    name: str
    scientific_name: Optional[str] = None
    other_names: Optional[str] = None
    family: Optional[str] = None
    description: Optional[str] = None
    parts_used: Optional[str] = None
    usage: Optional[str] = None
    preparation: Optional[str] = None
    symptoms: Optional[str] = None
    image_url: Optional[str] = None
    distribution: Optional[str] = None
    distribution_coords: Optional[List[DistributionCoord]] = None
    letter: str


class PlantOut(PlantBase):
    id: int

    class Config:
        from_attributes = True


class PlantSummary(BaseModel):
    id: int
    name: str
    scientific_name: Optional[str] = None
    image_url: Optional[str] = None
    usage: Optional[str] = None
    letter: str

    class Config:
        from_attributes = True


class CatalogGroup(BaseModel):
    letter: str
    plants: List[PlantSummary]


# ============ Map Schemas ============
class MapRequest(BaseModel):
    message: Optional[str] = None
    session_id: Optional[str] = None


class RecommendedPlant(BaseModel):
    id: int
    name: str
    scientific_name: Optional[str] = None
    image_url: Optional[str] = None
    usage: Optional[str] = None
    distribution_coords: Optional[List[DistributionCoord]] = None
    confidence: Optional[float] = None


class MapResponse(BaseModel):
    reply: str
    recommended_plants: List[RecommendedPlant] = []
    session_id: str
