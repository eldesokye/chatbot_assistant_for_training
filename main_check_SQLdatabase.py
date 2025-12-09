from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import psycopg2
import os

# Load environment variables
load_dotenv()
app = FastAPI()

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        os.getenv('DATABASE_URL'),
        sslmode='require'  # Required for Railway
    )
    return conn

@app.get("/")
def read_root():
    return {"message": "Retail Analytics Backend is live!"}

@app.get("/api/health")
def health_check():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW()")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return {"status": "Database connected!", "time": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/api/visitors/current")
def get_current_visitors():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Adjust this query to match your actual 'visitors' table schema
        cur.execute("""
            SELECT COUNT(*) as current_visitors 
            FROM visitors 
            WHERE timestamp > NOW() - INTERVAL '5 minutes'
        """)
        result = cur.fetchone()
        cur.close()
        conn.close()
        return {"current_visitors": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

# To run: uvicorn main:app --reload