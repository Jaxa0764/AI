import sqlite3

DB_PATH = "memory/memory.db"


def init_memory():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def remember(topic, content):
    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "INSERT INTO memories (topic, content) VALUES (?, ?)",
        (topic, content)
    )

    conn.commit()
    conn.close()


def search_memory(keyword):
    conn = sqlite3.connect(DB_PATH)

    rows = conn.execute(
        """
        SELECT topic, content, created_at
        FROM memories
        WHERE topic LIKE ? OR content LIKE ?
        ORDER BY id DESC
        """,
        (f"%{keyword}%", f"%{keyword}%")
    ).fetchall()

    conn.close()

    return rows
