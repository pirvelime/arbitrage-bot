# market_data.py
import sqlite3
from datetime import datetime
from typing import List, Dict, Union, Optional
from dataclasses import dataclass

@dataclass
class MarketData:
    token: str
    symbol: str
    slug: str
    exchange: str
    price: str
    volume: float
    link: Optional[str] = None
    date: Optional[datetime] = None

    def validate(self):
        """Validate market data fields."""
        if not all([self.token, self.symbol, self.slug, self.exchange, self.price]):
            raise ValueError("Required fields cannot be empty")
        
        if self.link and not (self.link.startswith('http://') or self.link.startswith('https://')):
            raise ValueError("Link must be a valid HTTP(S) URL")

class MarketDataDB:
    def __init__(self, db_path: str = "market_data.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = None
        self._connect()
    
    def _connect(self):
        """Create a database connection."""
        try:
            self.conn = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    def _ensure_connection(self):
        """Ensure database connection is active."""
        if self.conn is None:
            self._connect()
    
    def insert_one(self, data: MarketData) -> bool:
        """Insert a single market data record."""
        # Validate data before insertion
        data.validate()
        
        self._ensure_connection()
        sql = '''INSERT INTO market_data 
                (token, symbol, slug, link, exchange, price, volume, date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        try:
            date = data.date or datetime.now()
            cur = self.conn.cursor()
            cur.execute(sql, (
                data.token,
                data.symbol,
                data.slug,
                data.link,
                data.exchange,
                data.price,
                data.volume,
                date
            ))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
            return False

    def insert_many(self, data_list: List[MarketData]) -> Dict[int, bool]:
        """Insert multiple market data records."""
        results = {}
        for i, data in enumerate(data_list):
            results[i] = self.insert_one(data)
        return results
    
    def get_by_symbol(self, symbol: str, limit: int = 100) -> List[Dict]:
        """Retrieve market data for a specific symbol."""
        self._ensure_connection()
        sql = '''SELECT * FROM market_data 
                WHERE symbol = ? 
                ORDER BY date DESC 
                LIMIT ?'''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (symbol, limit))
            columns = [description[0] for description in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
        except sqlite3.Error as e:
            print(f"Error retrieving data: {e}")
            return []

    def get_by_slug(self, slug: str, limit: int = 100) -> List[Dict]:
        """Retrieve market data for a specific slug."""
        self._ensure_connection()
        sql = '''SELECT * FROM market_data 
                WHERE slug = ? 
                ORDER BY date DESC 
                LIMIT ?'''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (slug, limit))
            columns = [description[0] for description in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
        except sqlite3.Error as e:
            print(f"Error retrieving data: {e}")
            return []
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __enter__(self):
        """Context manager entry."""
        self._ensure_connection()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
