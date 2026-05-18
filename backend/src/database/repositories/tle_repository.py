from src.database.db import db

class TLERepo:
    
    @staticmethod
    def insert(cat_nr, name, line1, line2):
        db.execute(
            """
            INSERT INTO tle_history (cat_nr, name, line1, line2, fetched_at)
            VALUES (%s, %s, %s, %s, NOW())
            """,
            (cat_nr, name, line1, line2)
        )
    
    @staticmethod
    def get_latest(cat_nr):
        return db.fetchone(
            """
            SELECT id, cat_nr, name, line1, line2, fetched_at 
            FROM tle_history 
            WHERE cat_nr = %s 
            ORDER BY fetched_at DESC 
            LIMIT 1
            """,
            (cat_nr,)
        )

    @staticmethod
    def get_history(cat_nr):
        return db.fetchall(
            "SELECT * FROM tle_history WHERE cat_nr = %s ORDER BY fetched_at DESC",
            (cat_nr,)
        )
