from fastapi import APIRouter, Query
from typing import Optional, List
from models import Prediction
from crud import PredictionCRUD

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

@router.get("/", response_model=List[dict])
async def get_all_predictions():
    """Get all prediction forecasts"""
    return PredictionCRUD.get_latest_forecasts()

@router.get("/metric/{metric_type}", response_model=dict)
async def get_metric_prediction(
    metric_type: str,
    horizon: str = Query("1h", pattern="^(1h|4h|8h|1d|7d)$")
):
    """Get prediction for specific metric"""
    prediction = PredictionCRUD.get_metric_forecast(metric_type, horizon)
    if not prediction:
        return {"message": f"No prediction available for {metric_type} ({horizon})"}
    return prediction

@router.get("/traffic/forecast", response_model=dict)
async def get_traffic_forecast():
    """Get comprehensive traffic forecast"""
    visitors_pred = PredictionCRUD.get_metric_forecast("visitors", "4h")
    queue_pred = PredictionCRUD.get_metric_forecast("cashier_queue", "4h")
    
    return {
        "visitors_forecast": visitors_pred,
        "queue_forecast": queue_pred,
        "recommendation": generate_recommendation(visitors_pred, queue_pred)
    }

def generate_recommendation(visitors_pred, queue_pred):
    """Generate business recommendation based on predictions"""
    if not visitors_pred or not queue_pred:
        return "Insufficient data for recommendation"
    
    if visitors_pred.get('predicted_value', 0) > 50 and queue_pred.get('predicted_value', 0) > 4:
        return "Consider opening additional cashier lanes"
    elif visitors_pred.get('predicted_value', 0) < 10:
        return "Good time for restocking and maintenance"
    else:
        return "Normal operations recommended"