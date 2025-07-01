# utils/test_scoring_debug.py

from utils.llama_utils import get_llama_score
from utils.keyword_utils import keyword_matching_score
from utils.db_utils import get_keywords_from_db

def test_penilaian(id_soal, pertanyaan, jawaban):
    print("=== DEBUG PENILAIAN ===")
    print(f"📝 ID Soal     : {id_soal}")
    print(f"📖 Pertanyaan  : {pertanyaan}")
    print(f"🗣️ Jawaban     : {jawaban}")
    print("-" * 50)

    # Ambil keyword dari DB
    keywords = get_keywords_from_db(id_soal)
    if not keywords:
        print("❌ Keyword tidak ditemukan.")
        return

    print(f"🔑 Keywords ({len(keywords)}): {keywords}")

    # Penilaian Keyword
    keyword_score, matched_keywords = keyword_matching_score(jawaban, keywords)
    print(f"✅ Skor Keyword : {keyword_score}")
    print(f"🎯 Keyword Cocok: {matched_keywords}")

    # Penilaian LLM
    llm_score = get_llama_score(pertanyaan, jawaban)
    print(f"🤖 Skor LLM     : {llm_score}")

    # Final Score (0–5)
    final_score = round(0.6 * llm_score + 0.4 * keyword_score)
    final_score = min(max(final_score, 0), 5)
    print(f"📊 Skor Final   : {final_score}")

    print("=" * 50)


# Contoh penggunaan langsung
if __name__ == "__main__":
    # Ganti sesuai ID soal yang valid
    id_soal = "MLQ6"
    pertanyaan = "Sebutkan beberapa aplikasi machine learning dalam kehidupan sehari-hari."
    jawaban = "Machine learning memiliki berbagai aplikasi dalam kehidupan sehari-hari, antara lain: Sistem Rekomendasi  Digunakan dalam platform seperti Netflix, YouTube, dan Spotify untuk memberikan rekomendasi konten berdasarkan preferensi pengguna.Deteksi Spam dan Penipuan – Digunakan oleh email (Gmail Spam Filter) dan banking system untuk mendeteksi transaksi mencurigakan.Asisten Virtual – Contoh: Google Assistant, Siri, dan Alexa yang menggunakan Natural Language Processing (NLP) untuk memahami dan merespons perintah pengguna.Pengenalan Wajah – Digunakan pada smartphone (Face Unlock) dan sistem keamanan berbasis AI.Mobil Otonom – Digunakan dalam teknologi self-driving cars seperti yang dikembangkan oleh Tesla."

    test_penilaian(id_soal, pertanyaan, jawaban)
