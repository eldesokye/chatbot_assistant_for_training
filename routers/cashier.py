from fastapi import APIRouter, Query
from datetime import datetime
from typing import List
from models import Cashier
from crud import CashierCRUD

router = APIRouter(prefix="/api/cashier", tags=["cashier"])

@router.get("/current", response_model=dict)
async def get_current_cashier_status():
    """Get current cashier queue status"""
    status = CashierCRUD.get_current_status()
    if not status:
        return {"message": "No cashier data available", "timestamp": datetime.now()}
    return status

@router.get("/history", response_model=List[dict])
async def get_queue_history(hours: int = Query(6, ge=1, le=168)):
    """Get queue history for specified hours"""
    return CashierCRUD.get_queue_history(hours)

@router.get("/busy-periods", response_model=List[dict])
async def get_busy_periods(threshold: int = Query(3, ge=1, le=20)):
    """Get periods when queue was busy"""
    return CashierCRUD.get_busy_periods(threshold)

@router.get("/wait-time", response_model=dict)
async def estimate_wait_time():
    """Estimate current wait time based on queue"""
    status = CashierCRUD.get_current_status()
    if not status:
        return {"estimated_wait_minutes": 0, "message": "No data"}
    
    # Simple estimation: 2 minutes per person in queue
    wait_time = status['queue_length'] * 2
    return {
        "estimated_wait_minutes": wait_time,
        "queue_length": status['queue_length'],
        "timestamp": datetime.now()
    }