import sqlite3
import hashlib
import json
from datetime import datetime

DB_NAME = "audit_ledger.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_id TEXT,
            prompt TEXT,
            repsonse TEXT,
            token_count INTEGER,
            audit_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

def generate_hash(data_dict):
    # Sort keys to ensure the hash is deterministic
    encoded_data = json.dumps(data_dict, sort_keys=True).encode('utf-8')
    return hashlib.sha256(encoded_data).hexdigest()

def log_interaction(user_id, prompt, response, tokens):
    timestamp = datatime.utcnow().isoformat()

    # The dta we want to make immutable
    record = {
        "timestamp": timestamp,
        "user_id": user_id,
        "prompt": prompt,
        "response": response
    }

    # Create the cryptographic signature
    audit_hash = generate_hash(record)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO audit_logs (timestamp, user_id, prompt, response, token_count, audit_hash)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, user_id, prompt, response, tokens, audit_hash))
    conn.commit()
    conn.close()
    return audit_hash

if __name__ == "__main__":
    init_db()
    print(" Audit Ledger Initialized.")