import sqlite3
import hashlib

def connect():
    return sqlite3.connect("users.db", check_same_thread=False)

# ===============================
# CREATE USER TABLE
# ===============================
def init_db():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS history(
        username TEXT,
        course TEXT
    )
    """)

    conn.commit()
    conn.close()

# ===============================
# AUTH FUNCTIONS
# ===============================
def create_user(username, password):
    conn = connect()
    c = conn.cursor()

    hashed = hashlib.sha256(password.encode()).hexdigest()

    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    conn = connect()
    c = conn.cursor()

    hashed = hashlib.sha256(password.encode()).hexdigest()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
    return c.fetchone()

# ===============================
# HISTORY
# ===============================
def save_history(username, course):
    conn = connect()
    c = conn.cursor()

    c.execute("INSERT INTO history VALUES (?, ?)", (username, course))

    conn.commit()
    conn.close()

def get_history(username):
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT course FROM history WHERE username=?", (username,))
    data = c.fetchall()

    conn.close()
    return data