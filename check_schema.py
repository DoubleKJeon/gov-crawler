"""DB 테이블 구조 확인"""
import sqlite3

conn = sqlite3.connect('gov_support.db')
cursor = conn.cursor()

# 테이블 목록
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", [t[0] for t in tables])

# government_supports 테이블 스키마
if tables:
    cursor.execute("PRAGMA table_info(government_supports);")
    columns = cursor.fetchall()
    print("\ngovernment_supports columns:")
    for col in columns:
        print(f"  {col[1]} - {col[2]}")

conn.close()
