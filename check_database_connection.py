import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.connection = None
        
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME", "retail_analytics"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "your_password"),
                port=os.getenv("DB_PORT", "5432")
            )
            print("✅ Connected to PostgreSQL database")
            return self.connection
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return None
    
    def get_visitors(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM visitors ORDER BY timestamp DESC LIMIT 10")
            return cursor.fetchall()
    
    def insert_visitor(self, section_id, count):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO visitors (section_id, visitor_count) VALUES (%s, %s)",
                (section_id, count)
            )
            self.connection.commit()
            return True
    
    def get_cashier_status(self):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM cashier ORDER BY timestamp DESC LIMIT 1")
            return cursor.fetchone()
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("🔌 Database connection closed")

# اختبار الاتصال
if __name__ == "__main__":
    db = Database()
    conn = db.connect()
    
    if conn:
        print("📊 Visitors data:")
        visitors = db.get_visitors()
        for v in visitors:
            print(f"Section {v['section_id']}: {v['visitor_count']} visitors")
           
        db.close()