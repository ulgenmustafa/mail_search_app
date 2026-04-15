import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

def search(query):
    cursor.execute(
        """
        SELECT file_path, sender, date, subject
        FROM mails
        WHERE content LIKE ?
        OR sender LIKE ?
        OR subject LIKE ?
        """,
        (f"%{query}%", f"%{query}%", f"%{query}%")
    )
    return cursor.fetchall()

if __name__ == "__main__":
    while True:
        q = input("Ara: ")
        results = search(q)

        for r in results:
            print("Dosya:", r[0])
            print("Gönderen:", r[1])
            print("Tarih:", r[2])
            print("Konu:", r[3])
            print("-" * 40)