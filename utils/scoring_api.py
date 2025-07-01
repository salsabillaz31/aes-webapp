# app/scoring_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.llama_utils import get_llama_score
from utils.keyword_utils import keyword_matching_score
from utils.db_utils import get_keywords_from_db  # pastikan kamu punya ini
import traceback

app = FastAPI()

class ScoreRequest(BaseModel):
    pertanyaan: str
    jawaban: str
    id_soal: str

@app.post("/score")
def score_jawaban(data: ScoreRequest):
    try:
        # Hitung skor LLM
        score_llm = get_llama_score(data.pertanyaan, data.jawaban)

        # Ambil keywords dari database
        keyword_list = get_keywords_from_db(data.id_soal)
        if not keyword_list:
            raise HTTPException(status_code=404, detail=f"Keyword tidak ditemukan untuk soal {data.id_soal}")

        # Hitung skor keyword
        score_keyword, _ = keyword_matching_score(data.jawaban, keyword_list)

        # Hitung skor final dan bulatkan ke 0–5
        final_score = round((0.6 * score_llm + 0.4 * score_keyword))
        final_score = min(max(final_score, 0), 5)  # jaga batas

        return {
            "llm_score": int(score_llm),
            "keyword_score": int(score_keyword),
            "final_score": int(final_score)  # final dalam 0–5
        }

    except Exception as e:
        print("=== ERROR DI /score ===")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
