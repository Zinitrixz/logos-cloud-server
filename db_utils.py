import psycopg2
import pandas as pd
from config import DB_SETTINGS

def get_connection():
    return psycopg2.connect(**DB_SETTINGS)

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(open("models.sql", "r", encoding="utf-8").read())
        conn.commit()

# --- USERS ---

def create_user(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING", (username,))
        conn.commit()

def get_user_id(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            result = cur.fetchone()
            return result[0] if result else None

def get_user_state(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT mode, active_role, wincoin FROM users WHERE username = %s", (username,))
            row = cur.fetchone()
            if row:
                return {"mode": row[0], "role": row[1], "wincoin": row[2]}
            return {}

def update_user_state(username, mode, role, wincoin):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE users SET mode = %s, active_role = %s, wincoin = %s
                WHERE username = %s
            """, (mode, role, wincoin, username))
        conn.commit()

# --- INSIGHTS ---

def save_insight(username, zone, insight, wincoin):
    user_id = get_user_id(username)
    if user_id:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO insights (user_id, zone, insight, wincoin)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, zone, insight, wincoin))
            conn.commit()

def get_insights(username):
    user_id = get_user_id(username)
    if not user_id:
        return []
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT zone, insight, wincoin, timestamp
                FROM insights
                WHERE user_id = %s
                ORDER BY timestamp DESC
            """, (user_id,))
            return [
                {"zone": row[0], "insight": row[1], "wincoin": row[2], "timestamp": str(row[3])}
                for row in cur.fetchall()
            ]

# --- CARDS / TASKS / ROLES / RITUALS ---

def draw_card(category, zone=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if zone:
                cur.execute("""
                    SELECT title, description FROM cards
                    WHERE category = %s AND zone = %s
                    ORDER BY random() LIMIT 1
                """, (category, zone))
            else:
                cur.execute("""
                    SELECT title, description FROM cards
                    WHERE category = %s
                    ORDER BY random() LIMIT 1
                """, (category,))
            card = cur.fetchone()
            if card:
                return {"card": card[0], "description": card[1]}
            return {}

def get_task(zone):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT task FROM tasks
                WHERE zone = %s
                ORDER BY random() LIMIT 1
            """, (zone,))
            row = cur.fetchone()
            return {"task": row[0]} if row else {}

def get_role_by_zone(zone):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT role, description FROM roles
                WHERE zone = %s
                ORDER BY random() LIMIT 1
            """, (zone,))
            row = cur.fetchone()
            return {"role": row[0], "description": row[1]} if row else {}

def get_ritual(mode, trigger):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT name, description FROM rituals
                WHERE mode = %s AND trigger = %s
                ORDER BY random() LIMIT 1
            """, (mode, trigger))
            row = cur.fetchone()
            return {"name": row[0], "description": row[1]} if row else {}

# --- ZION ---

def store_zion(content, ztype="insight", created_by="Logos"):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO zion_manifest (type, content, created_by)
                VALUES (%s, %s, %s)
            """, (ztype, content, created_by))
        conn.commit()

def get_zion_manifest(limit=10):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT type, content, timestamp FROM zion_manifest
                ORDER BY timestamp DESC LIMIT %s
            """, (limit,))
            return [
                {"type": row[0], "content": row[1], "timestamp": str(row[2])}
                for row in cur.fetchall()
            ]

# --- INITIAL LOADERS (CSV/JSON TO DB) ---

def load_cards_from_json(filepath="data/logos_knowledge_core.json"):
    df = pd.read_json(filepath)
    with get_connection() as conn:
        with conn.cursor() as cur:
            for _, row in df.iterrows():
                cur.execute("""
                    INSERT INTO cards (category, zone, title, description)
                    VALUES (%s, %s, %s, %s)
                """, (row["category"], row["zone"], row["title"], row["description"]))
        conn.commit()

def load_roles_from_json(filepath="data/logos_roles.json"):
    df = pd.read_json(filepath)
    with get_connection() as conn:
        with conn.cursor() as cur:
            for _, row in df.iterrows():
                cur.execute("""
                    INSERT INTO roles (zone, role, description)
                    VALUES (%s, %s, %s)
                """, (row["zone"], row["role"], row["description"]))
        conn.commit()
