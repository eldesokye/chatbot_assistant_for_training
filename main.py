from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
import os

from database import test_connection, db
from routers import visitors, cashier, heatmap, predictions

# Initialize FastAPI app
app = FastAPI(
    title="Retail Analytics API",
    description="Backend for Retail Analytics System with Computer Vision",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(visitors.router)
app.include_router(cashier.router)
app.include_router(heatmap.router)
app.include_router(predictions.router)

# Custom exception handler
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "path": request.url.path}
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print("🚀 Retail Analytics Backend Starting Up...")
    print("=" * 50)
    
    # Test database connection
    if test_connection():
        print("✅ All systems operational!")
    else:
        print("⚠️  Warning: Database connection issues detected")

# Health check endpoint
@app.get("/")
async def root():
    return {
        "service": "Retail Analytics API",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "visitors": "/api/visitors",
            "cashier": "/api/cashier",
            "heatmap": "/api/heatmap",
            "predictions": "/api/predictions",
            "documentation": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    try:
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                # Check all tables exist
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    AND table_name IN ('visitors', 'cashier', 'heatmap', 'predictions')
                """)
                tables = cur.fetchall()
                
                # Get row counts
                cur.execute("SELECT COUNT(*) as count FROM visitors")
                visitors_count = cur.fetchone()['count']
                
                cur.execute("SELECT COUNT(*) as count FROM cashier")
                cashier_count = cur.fetchone()['count']
                
                return {
                    "status": "healthy",
                    "database": "connected",
                    "tables_available": [t['table_name'] for t in tables],
                    "data_summary": {
                        "visitors_records": visitors_count,
                        "cashier_records": cashier_count
                    },
                    "timestamp": datetime.now().isoformat()
                }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Run the application
if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    print(f"\n📊 Retail Analytics API")
    print(f"   Local: http://localhost:{port}")
    print(f"   Docs: http://localhost:{port}/docs")
    print(f"   Health: http://localhost:{port}/health")
    print(f"\nPress Ctrl+C to stop\n")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )