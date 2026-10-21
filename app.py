import sqlite3
import os

DB_PATH = "memory/cyberai.db"


# =========================
# XOTIRA BAZASINI YARATISH
# =========================

def init_memory():
    os.makedirs("memory", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================
# REMEMBER
# =========================

def remember():
    topic = input("Mavzu: ").strip()

    if not topic:
        return

    content = input("Ma'lumot: ").strip()

    if not content:
        return

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        """
        INSERT INTO memories (topic, content)
        VALUES (?, ?)
        ON CONFLICT(topic)
        DO UPDATE SET content = excluded.content
        """,
        (topic, content)
    )

    conn.commit()
    conn.close()

    print("Saqlandi.")


# =========================
# SEARCH
# =========================

def search():
    conn = sqlite3.connect(DB_PATH)

    topics = conn.execute(
        "SELECT topic FROM memories ORDER BY topic"
    ).fetchall()

    conn.close()

    if not topics:
        print("Xotira bo'sh.")
        return

    print()

    for topic, in topics:
        print(topic)

    print()

    selected = input("Mavzu: ").strip()

    conn = sqlite3.connect(DB_PATH)

    result = conn.execute(
        "SELECT content FROM memories WHERE topic = ?",
        (selected,)
    ).fetchone()

    conn.close()

    if result:
        print()
        print(result[0])
    else:
        print("Bunday mavzu topilmadi.")


# =========================
# DELETE
# =========================

def delete_topic():
    topic = input("Mavzu: ").strip()

    if not topic:
        return

    conn = sqlite3.connect(DB_PATH)

    result = conn.execute(
        "DELETE FROM memories WHERE topic = ?",
        (topic,)
    )

    conn.commit()
    conn.close()

    if result.rowcount > 0:
        print("O'chirildi.")
    else:
        print("Bunday mavzu topilmadi.")


# =========================
# CYBERAI
# =========================

init_memory()

print("WELCOME!")

while True:

    command = input("WebShadoWin-> ").strip().lower()

    if command == "remember":
        remember()

    elif command == "search":
        search()

    elif command == "delete":
        delete_topic()

    elif command == "exit":
        break
