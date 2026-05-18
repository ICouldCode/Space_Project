from src.database.connection import get_connection

class db:
    
    @staticmethod
    def execute(query, params=None):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)

    @staticmethod
    def fetchall(query, params=None):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()
            
    @staticmethod
    def fetchone(query, params=None):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchone()