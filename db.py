import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SSL_MODE = os.getenv("SSL_MODE", 'disable')

def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode=SSL_MODE, cursor_factory=RealDictCursor)

def init_db():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id SERIAL PRIMARY KEY,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                location TEXT,
                link TEXT UNIQUE NOT NULL,
                age TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()

def get_existing_listings():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT company, role, location, link, age FROM listings;")
        return cur.fetchall()

def insert_new_listings(listings):
    with get_connection() as conn, conn.cursor() as cur:
        for l in listings:
            try:
                cur.execute("""
                    INSERT INTO listings (company, role, location, link, age)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (link) DO NOTHING;
                """, (l['company'], l['role'], l['location'], l['link'], l['age']))
            except Exception as e:
                print(f"Failed to insert {l['company']} | {l['role']}: {e}")
        conn.commit()
