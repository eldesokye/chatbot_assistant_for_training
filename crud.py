from datetime import datetime, timedelta, date
from typing import List, Optional, Dict, Any
from models import *
from database import db

class VisitorCRUD:
    @staticmethod
    def get_all(limit: int = 100) -> List[Dict]:
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM visitors 
                ORDER BY timestamp DESC 
                LIMIT %s
            """, (limit,))
            return cur.fetchall()
    
    @staticmethod
    def get_by_id(visitor_id: int) -> Optional[Dict]:
        with db.get_cursor() as cur:
            cur.execute("SELECT * FROM visitors WHERE id = %s", (visitor_id,))
            return cur.fetchone()
    
    @staticmethod
    def get_current_count() -> int:
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT SUM(count) as total 
                FROM visitors 
                WHERE timestamp > NOW() - INTERVAL '15 minutes'
            """)
            result = cur.fetchone()
            return result['total'] if result['total'] else 0
    
    @staticmethod
    def get_by_date_range(start: datetime, end: datetime) -> List[Dict]:
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM visitors 
                WHERE timestamp BETWEEN %s AND %s 
                ORDER BY timestamp
            """, (start, end))
            return cur.fetchall()
    
    @staticmethod
    def get_section_traffic() -> List[Dict]:
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT section, SUM(count) as total_visitors,
                       COUNT(*) as records_count
                FROM visitors 
                WHERE timestamp > NOW() - INTERVAL '24 hours'
                GROUP BY section 
                ORDER BY total_visitors DESC
            """)
            return cur.fetchall()

class CashierCRUD:
    @staticmethod
    def get_current_status() -> Optional[Dict]:
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM cashier 
                ORDER BY timestamp DESC 
                LIMIT 1
            """)
            return cur.fetchone()
    
    @staticmethod
    def get_queue_history(hours: int = 6) -> List[Dict]:
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT timestamp, queue_length, status, wait_time_minutes
                FROM cashier 
                WHERE timestamp > NOW() - INTERVAL '%s hours'
                ORDER BY timestamp
            """, (hours,))
            return cur.fetchall()
    
    @staticmethod
    def get_busy_periods(threshold: int = 3) -> List[Dict]:
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT DATE_TRUNC('hour', timestamp) as hour_start,
                       AVG(queue_length) as avg_queue,
                       MAX(queue_length) as max_queue
                FROM cashier 
                WHERE timestamp > NOW() - INTERVAL '7 days'
                GROUP BY DATE_TRUNC('hour', timestamp)
                HAVING AVG(queue_length) > %s
                ORDER BY avg_queue DESC
            """, (threshold,))
            return cur.fetchall()

class HeatmapCRUD:
    @staticmethod
    def get_latest() -> List[Dict]:
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT DISTINCT ON (section) *
                FROM heatmap 
                ORDER BY section, timestamp DESC
            """)
            return cur.fetchall()
    
    @staticmethod
    def get_density_analysis() -> Dict[str, Any]:
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT 
                    COUNT(CASE WHEN density_level = 'high' THEN 1 END) as high_count,
                    COUNT(CASE WHEN density_level = 'medium' THEN 1 END) as medium_count,
                    COUNT(CASE WHEN density_level = 'low' THEN 1 END) as low_count,
                    AVG(visitor_count) as avg_visitors
                FROM heatmap 
                WHERE timestamp > NOW() - INTERVAL '1 hour'
            """)
            return cur.fetchone()

class PredictionCRUD:
    @staticmethod
    def get_latest_forecasts() -> List[Dict]:
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT DISTINCT ON (metric_type, forecast_horizon) *
                FROM predictions 
                ORDER BY metric_type, forecast_horizon, prediction_timestamp DESC
            """)
            return cur.fetchall()
    
    @staticmethod
    def get_metric_forecast(metric_type: str, horizon: str = "1h") -> Optional[Dict]:
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT * FROM predictions 
                WHERE metric_type = %s AND forecast_horizon = %s
                ORDER BY prediction_timestamp DESC 
                LIMIT 1
            """, (metric_type, horizon))
            return cur.fetchone()

class AnalyticsCRUD:
    @staticmethod
    def get_daily_summary() -> Dict[str, Any]:
        with db.get_cursor() as cur:
            # Get today's date at midnight
            today_start = datetime.combine(date.today(), datetime.min.time())
            
            # Total visitors today
            cur.execute("""
                SELECT SUM(count) as total_visitors
                FROM visitors 
                WHERE timestamp >= %s
            """, (today_start,))
            visitors_result = cur.fetchone()
            
            # Busiest section
            cur.execute("""
                SELECT section, SUM(count) as total
                FROM visitors 
                WHERE timestamp >= %s
                GROUP BY section 
                ORDER BY total DESC 
                LIMIT 1
            """, (today_start,))
            busiest_result = cur.fetchone()
            
            # Average queue length today
            cur.execute("""
                SELECT AVG(queue_length) as avg_queue
                FROM cashier 
                WHERE timestamp >= %s
            """, (today_start,))
            queue_result = cur.fetchone()
            
            # Peak hour (hour with most visitors)
            cur.execute("""
                SELECT EXTRACT(HOUR FROM timestamp) as hour,
                       SUM(count) as total_visitors
                FROM visitors 
                WHERE timestamp >= %s
                GROUP BY EXTRACT(HOUR FROM timestamp)
                ORDER BY total_visitors DESC 
                LIMIT 1
            """, (today_start,))
            peak_result = cur.fetchone()
            
            return {
                'total_visitors_today': visitors_result['total_visitors'] or 0,
                'busiest_section': busiest_result['section'] if busiest_result else 'N/A',
                'avg_queue_length': round(queue_result['avg_queue'] or 0, 1),
                'peak_hour': f"{int(peak_result['hour'] or 0)}:00" if peak_result else 'N/A',
                'timestamp': datetime.now()
            }