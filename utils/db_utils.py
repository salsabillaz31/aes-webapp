import psycopg2
import os
import json
from dotenv import load_dotenv

load_dotenv()
def get_keywords_from_db(id_question):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),    
        port=os.getenv("POSTGRES_PORT"),
    )
    cur = conn.cursor()
    cur.execute("SELECT keywords FROM list_soal WHERE id_question = %s", (id_question,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if not result:
        return None

    raw_keywords = result[0]

    # Fallback jika bukan JSON
    if raw_keywords.startswith("["):
        try:
            return json.loads(raw_keywords)
        except:
            pass

    # Fallback parsing dari string biasa: pisah koma
    return [kw.strip() for kw in raw_keywords.split(",") if kw.strip()]


