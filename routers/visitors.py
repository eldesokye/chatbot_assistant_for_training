from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, timedelta
from typing import Optional, List
from models import Visitor, TimeRange, AnalyticsResponse
from crud import VisitorCRUD, AnalyticsCRUD

router = APIRouter(prefix="/api/visitors", tags=["visitors"])

@router.get("/", response_model=List[dict])
async def get_all_visitors(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get all visitor records"""
    return VisitorCRUD.get_all(limit=limit)

@router.get("/current", response_model=dict)
async def get_current_visitors():
    """Get current visitor count"""
    count = VisitorCRUD.get_current_count()
    return {"current_visitors": count, "timestamp": datetime.now()}

@router.get("/sections", response_model=List[dict])
async def get_section_traffic():
    """Get visitor distribution by section"""
    return VisitorCRUD.get_section_traffic()

@router.get("/{visitor_id}", response_model=dict)
async def get_visitor(visitor_id: int):
    """Get specific visitor record by ID"""
    visitor = VisitorCRUD.get_by_id(visitor_id)
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor record not found")
    return visitor

@router.post("/range", response_model=List[dict])
async def get_visitors_by_range(time_range: TimeRange):
    """Get visitors within a time range"""
    return VisitorCRUD.get_by_date_range(
        time_range.start_time, 
        time_range.end_time
    )

@router.get("/analytics/daily", response_model=AnalyticsResponse)
async def get_daily_analytics():
    """Get daily analytics summary"""
    return AnalyticsCRUD.get_daily_summary()