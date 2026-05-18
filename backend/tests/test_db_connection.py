from src.database.connection import get_connection

def test():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()
                print(f"Connected! PostgreSQL version: {version[0]}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test()