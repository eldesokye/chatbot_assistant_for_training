import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

load_dotenv()

class Database:
    def __init__(self):
        self.connection_string = os.getenv('DATABASE_URL')
    
    @contextmanager
    def get_connection(self):
        """Get a database connection with automatic cleanup"""
        conn = None
        try:
            conn = psycopg2.connect(
                self.connection_string,
                cursor_factory=RealDictCursor,
                sslmode='require'
            )
            yield conn
        except psycopg2.OperationalError as e:
            print(f"Database connection failed: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    @contextmanager
    def get_cursor(self):
        """Get a database cursor with automatic cleanup"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise
            finally:
                cursor.close()

# Global database instance
db = Database()

def test_connection():
    """Test database connection"""
    try:
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version(), current_database(), current_user")
                result = cur.fetchone()
                print("✅ Database connected successfully!")
                print(f"   PostgreSQL: {result['version'].split(',')[0]}")
                print(f"   Database: {result['current_database']}")
                print(f"   User: {result['current_user']}")
                return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False