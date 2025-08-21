import sqlite3

DB_NAME = "ludo.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    con = get_db()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        wallet REAL DEFAULT 0
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin_wallet (
        id INTEGER PRIMARY KEY,
        amount REAL DEFAULT 0
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player1 INTEGER,
        player2 INTEGER,
        status TEXT DEFAULT 'waiting'
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS screenshots (
        user_id INTEGER,
        file_id TEXT,
        utr TEXT,
        status TEXT DEFAULT 'pending'
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS withdrawals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        status TEXT DEFAULT 'pending'
    )
    """)
    con.commit()
    con.close()


# Add to create_tables()
cur.execute("""
CREATE TABLE IF NOT EXISTS groups (
    group_id INTEGER PRIMARY KEY,
    added_by INTEGER,
    is_premium INTEGER DEFAULT 0,
    plan_start TEXT,
    plan_end TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS plans (
    plan_name TEXT PRIMARY KEY,
    duration_days INTEGER,
    price REAL
)
""")
# Add initial plans
cur.execute("INSERT OR IGNORE INTO plans VALUES ('1mon', 30, 100)")
cur.execute("INSERT OR IGNORE INTO plans VALUES ('3mon', 90, 300)")
cur.execute("INSERT OR IGNORE INTO plans VALUES ('12mon', 365, 1200)")
con.commit()


def add_user(user_id, username):
    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    con.commit()
    con.close()

def get_wallet(user_id):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
    r = cur.fetchone()
    con.close()
    return r["wallet"] if r else 0

def update_wallet(user_id, amount):
    con = get_db()
    cur = con.cursor()
    cur.execute("UPDATE users SET wallet = wallet + ? WHERE user_id = ?", (amount, user_id))
    con.commit()
    con.close()

def set_table_charge(amount):
    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO admin_wallet (id, amount) VALUES (1, ?)", (amount,))
    con.commit()
    con.close()

def get_admin_wallet():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT amount FROM admin_wallet WHERE id = 1")
    r = cur.fetchone()
    con.close()
    return r["amount"] if r else 0

def get_all_users():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT user_id, username, wallet FROM users")
    users = [dict(r) for r in cur.fetchall()]
    con.close()
    return users

def save_screenshot(user_id, file_id, utr=None):
    con = get_db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO screenshots (user_id, file_id, utr, status) VALUES (?, ?, ?, 'pending')",
        (user_id, file_id, utr)
    )
    con.commit()
    con.close()

def check_screenshot_utr(user_id, utr):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM screenshots WHERE user_id = ? AND utr = ? AND status = 'pending'", (user_id, utr))
    r = cur.fetchone()
    con.close()
    return bool(r)

def mark_win_verified(user_id):
    con = get_db()
    cur = con.cursor()
    cur.execute("UPDATE screenshots SET status = 'verified' WHERE user_id = ? AND status = 'pending'", (user_id,))
    con.commit()
    con.close()

def add_withdrawal(user_id, amount):
    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT INTO withdrawals (user_id, amount) VALUES (?, ?)", (user_id, amount))
    con.commit()
    con.close()

def approve_withdrawal(user_id, amount):
    con = get_db()
    cur = con.cursor()
    cur.execute("UPDATE withdrawals SET status = 'approved' WHERE user_id = ? AND amount = ? AND status = 'pending'", (user_id, amount))
    update_wallet(user_id, -amount)
    con.commit()
    con.close()

def get_username(user_id):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT username FROM users WHERE user_id = ?", (user_id,))
    r = cur.fetchone()
    con.close()

    return r["username"] if r else ""



def add_group(group_id, user_id, is_premium=0, start=None, end=None):
    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO groups (group_id, added_by, is_premium, plan_start, plan_end) VALUES (?, ?, ?, ?, ?)",
                (group_id, user_id, is_premium, start, end))
    con.commit()
    con.close()

def set_group_premium(group_id, is_premium, start, end):
    con = get_db()
    cur = con.cursor()
    cur.execute("UPDATE groups SET is_premium=?, plan_start=?, plan_end=? WHERE group_id=?", (is_premium, start, end, group_id))
    con.commit()
    con.close()

def get_group(group_id):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM groups WHERE group_id=?", (group_id,))
    r = cur.fetchone()
    con.close()
    return dict(r) if r else None

def get_plan(plan_name):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM plans WHERE plan_name=?", (plan_name,))
    r = cur.fetchone()
    con.close()
    return dict(r) if r else None
