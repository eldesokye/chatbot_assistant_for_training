from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List, Dict, Any

# Visitor Models
class VisitorBase(BaseModel):
    section: str
    count: int
    gender_distribution: Optional[Dict[str, int]] = None

class VisitorCreate(VisitorBase):
    pass

class Visitor(VisitorBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Cashier Models
class CashierBase(BaseModel):
    queue_length: int
    wait_time_minutes: Optional[float] = None
    transactions_count: Optional[int] = None
    status: str = Field(..., pattern="^(busy|normal|idle)$")

class CashierCreate(CashierBase):
    pass

class Cashier(CashierBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Heatmap Models
class HeatmapBase(BaseModel):
    section: str
    density_level: str = Field(..., pattern="^(high|medium|low)$")
    coordinates: Optional[Dict[str, Any]] = None
    visitor_count: int

class HeatmapCreate(HeatmapBase):
    pass

class Heatmap(HeatmapBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Prediction Models
class PredictionBase(BaseModel):
    metric_type: str = Field(..., pattern="^(visitors|cashier_queue|conversions)$")
    predicted_value: float
    confidence_level: float = Field(..., ge=0, le=1)
    forecast_horizon: str  # e.g., "1h", "4h", "1d"

class PredictionCreate(PredictionBase):
    pass

class Prediction(PredictionBase):
    id: int
    prediction_timestamp: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Analytics Models
class AnalyticsResponse(BaseModel):
    total_visitors_today: int
    busiest_section: str
    avg_queue_length: float
    peak_hour: str
    conversion_rate: Optional[float] = None

class TimeRange(BaseModel):
    start_time: datetime
    end_time: datetime = Field(default_factory=lambda: datetime.now())