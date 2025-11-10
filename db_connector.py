import sqlite3
from datetime import datetime

class DBConnector:
    def __init__(self, db_path="sentiment_history.db"):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        """Create sentiment_history table if not exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sentiment_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text_input TEXT NOT NULL,
                text_processed TEXT NOT NULL,
                sentiment_label TEXT NOT NULL,
                confidence_score REAL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def insert_history(self, text_input, text_processed, sentiment_label, confidence_score):
        """Insert a new sentiment analysis record"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sentiment_history (text_input, text_processed, sentiment_label, confidence_score, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (text_input, text_processed, sentiment_label, confidence_score, timestamp))
        conn.commit()
        conn.close()

    def fetch_history(self, limit=50):
        """Fetch recent history records"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, text_input, text_processed, sentiment_label, confidence_score, timestamp
            FROM sentiment_history
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def delete_by_id(self, id):
        """Delete a specific record by id"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sentiment_history WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    def delete_all(self):
        """Delete all records"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sentiment_history')
        conn.commit()
        conn.close()