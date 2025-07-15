

def get_dynamic_schema(db_path="app.db"):
    import sqlite3
    schema_str = "Database Schema:\n"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        schema_str += f"Table: {table}\nColumns:\n"
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            notnull = "NOT NULL" if col[3] else ""
            pk = "PRIMARY KEY" if col[5] else ""
            extras = ", ".join(filter(None, [col_type, pk, notnull]))
            schema_str += f"- {col_name}: {extras}\n"
    conn.close()
    return schema_str


def call_groq_llm(prompt, schema=None):
    import requests
    import os
    from dotenv import load_dotenv

    load_dotenv()

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    if schema is None:
        # Use dynamic schema from the default db path (update if needed)
        schema = get_dynamic_schema()
    full_prompt = f"{schema}\n\nUser Query: {prompt}\n\nOnly return the sql query, do not return any other text."
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": full_prompt}
        ]
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("Error:", response.status_code, response.text)
        return None