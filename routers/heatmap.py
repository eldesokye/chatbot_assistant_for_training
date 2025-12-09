from fastapi import APIRouter
from typing import List
from crud import HeatmapCRUD

router = APIRouter(prefix="/api/heatmap", tags=["heatmap"])

@router.get("/", response_model=List[dict])
async def get_latest_heatmap():
    """Get latest heatmap data for all sections"""
    return HeatmapCRUD.get_latest()

@router.get("/analysis", response_model=dict)
async def get_density_analysis():
    """Get heatmap density analysis"""
    return HeatmapCRUD.get_density_analysis()

@router.get("/density/{level}", response_model=List[dict])
async def get_by_density_level(level: str):
    """Get sections by density level (high/medium/low)"""
    data = HeatmapCRUD.get_latest()
    filtered = [item for item in data if item['density_level'] == level]
    return filtered