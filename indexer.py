import os
import sqlite3
from pypdf import PdfReader
from docx import Document
import pandas as pd
import extract_msg

DB = "database.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS mails (
    id INTEGER PRIMARY KEY,
    file_path TEXT UNIQUE,
    content TEXT,
    sender TEXT,
    date TEXT,
    subject TEXT
)
""")

def read_pdf(path):
    try:
        reader = PdfReader(path)
        return " ".join([p.extract_text() or "" for p in reader.pages])
    except:
        return ""

def read_docx(path):
    try:
        doc = Document(path)
        return " ".join([p.text for p in doc.paragraphs])
    except:
        return ""

def read_excel(path):
    try:
        df = pd.read_excel(path)
        return df.to_string()
    except:
        return ""

def read_txt(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def read_msg(path):
    try:
        msg = extract_msg.Message(path)
        body = msg.body or ""
        sender = msg.sender or ""
        date = str(msg.date) if msg.date else ""
        subject = msg.subject or ""
        return body, sender, date, subject
    except:
        return "", "", "", ""

def process_file(path):
    if path.endswith(".msg"):
        return read_msg(path)
    else:
        content = ""
        if path.endswith(".pdf"):
            content = read_pdf(path)
        elif path.endswith(".docx"):
            content = read_docx(path)
        elif path.endswith(".xlsx"):
            content = read_excel(path)
        elif path.endswith(".txt"):
            content = read_txt(path)

        return content, "", "", ""

def index_folder(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            content, sender, date, subject = process_file(path)

            cursor.execute(
                "INSERT OR IGNORE INTO mails (file_path, content, sender, date, subject) VALUES (?, ?, ?, ?, ?)",
                (path, content, sender, date, subject)
            )

    conn.commit()

if __name__ == "__main__":
    folder = "data"
    index_folder(folder)