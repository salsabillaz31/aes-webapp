from dotenv import load_dotenv
import os
import openai
import json
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def create_aes_prompt(question, answer):
    return f"""
Anda adalah penilai esai otomatis untuk ujian kompetensi Data Scientist. Tugas Anda adalah menilai jawaban mahasiswa berdasarkan pertanyaan dan kualitas isi jawaban.

Gunakan rubrik penilaian berikut (Skala 0–5):

- Skor 0: Jawaban kosong atau tidak relevan dengan pertanyaan, meskipun panjang.
- Skor 1: Mengandung satu atau lebih keyword, tetapi penjelasan tidak jelas, tidak terstruktur, dan tidak menunjukkan pemahaman. Jawaban cenderung acak.
- Skor 2: Mengandung beberapa keyword penting tetapi belum menunjukkan penguasaan materi. Penjelasan masih terbatas dan belum membentuk pengertian utuh.
- Skor 3: Jawaban tepat dan sesuai inti konsep, namun terlalu umum atau masih kurang dari segi penjelasan tambahan. Bisa menjawab dengan baik, tetapi masih kurang satu dua aspek penting.
- Skor 4: Jawaban tepat, cukup lengkap, mengandung hampir semua keyword penting dan tidak keluar dari konteks. Cocok untuk pertanyaan yang membutuhkan penjabaran lebih luas.
- Skor 5: Jawaban tepat, lengkap, dan efisien. Mengandung seluruh keyword penting dan menjawab secara langsung sesuai cakupan pertanyaan, tanpa keluar dari topik. Tidak diukur dari panjangnya, tapi dari akurasi dan kelengkapan inti konsep.

--- 
Pertanyaan:
{question}

Jawaban Mahasiswa:
{answer}
---

Tugas Anda:
Berdasarkan rubrik di atas, berikan penilaian dalam format berikut:

Skor: [0-5]  
"""

def create_aes_prompt_fewshot(question, answer):
    examples = [
        {
            
            "question": "Apa yang dimaksud dengan Knowledge Discovery in Databases (KDD)?",
            "answer": "Proses Knowledge Discovery in Databases (KDD) melibatkan beberapa tahapan utama: (1) Seleksi Data, yaitu pemilihan data yang relevan dari sumber yang besar, (2) Preprocessing atau pembersihan data untuk menghilangkan noise dan data yang tidak konsisten, (3) Transformasi data agar sesuai untuk analisis, (4) Data Mining, yaitu proses utama dalam menemukan pola atau informasi yang bermanfaat, dan (5) Evaluasi dan interpretasi hasil untuk memastikan pola yang ditemukan memiliki nilai yang bermakna.",
            "score": 0
        },
        {
            
            "question": "Apa yang dimaksud dengan Knowledge Discovery in Databases (KDD)?",
            "answer": "KDD itu sesuatu yang berkaitan dengan data.",
            "score": 1
        },
        {
            "question": "Apa yang dimaksud dengan Knowledge Discovery in Databases (KDD)?",
            "answer": "KDD adalah proses dalam data science yang digunakan untuk mendapatkan informasi.",
            "score": 2
        },
        {
            "question": "Apa yang dimaksud dengan Knowledge Discovery in Databases (KDD)?",
            "answer": "KDD adalah proses untuk menemukan pola atau informasi dalam database yang besar.",
            "score": 3
        },
        {
            "question": "Apa yang dimaksud dengan Knowledge Discovery in Databases (KDD)?",
            "answer": "KDD adalah proses menemukan pola atau informasi penting dalam database yang besar melalui beberapa tahapan, seperti preprocessing dan data mining.",
            "score": 4
        },
        {
            "question": "Jelaskan perbedaan supervised dan unsupervised learning.",
            "answer": "Knowledge Discovery in Databases (KDD) adalah proses ekstraksi informasi atau pola yang berguna dari kumpulan data dalam database besar. Proses ini terdiri dari beberapa tahapan utama, yaitu seleksi data, preprocessing, transformasi, data mining, dan interpretasi/evaluasi hasil.",
            "score": 5
        }
    ]

    fewshot_part = "\n".join([
        f"""Pertanyaan: {ex["question"]}
Jawaban: {ex["answer"]}
Skor: {ex["score"]}\n"""
        for ex in examples
    ])

    instruction = f"""
Anda adalah asisten penilai esai otomatis untuk kompetensi Data Scientist.
Tugas Anda adalah memberikan skor 0 sampai 5 berdasarkan rubrik berikut:

- Skor 0: Jawaban kosong atau tidak relevan.
- Skor 1: Mengandung keyword, tetapi penjelasan acak/tidak jelas.
- Skor 2: Beberapa keyword penting, belum membentuk pemahaman utuh.
- Skor 3: Sesuai konsep tapi terlalu umum/kurang aspek penting.
- Skor 4: Jawaban tepat dan lengkap, hampir semua keyword penting.
- Skor 5: Lengkap, fokus, semua keyword penting, tidak keluar konteks.

Berikan hanya JSON dengan format:
{{"skor": int}}

Berikut beberapa contoh:

{fewshot_part}

Sekarang nilai jawaban berikut:

Pertanyaan: {question}
Jawaban: {answer}

Jawaban JSON:
"""
    return instruction.strip()

def get_llama_score(question, answer):
    prompt = create_aes_prompt_fewshot(question, answer)

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
    )

    # Ambil isi respons
    content = response.choices[0].message.content.strip()

    try:
        # Parse string JSON jadi dict Python
        parsed = json.loads(content)
        return int(parsed["skor"])
    except Exception as e:
        print("Gagal parsing respons:", content)
        return 1  # fallback biar sistem tetap jalan

'''
# Untuk testing langsung
if __name__ == "__main__":
    question = "Jelaskan proses yang terlibat dalam KDD."
    answer = "Knowledge Discovery in Databases (KDD) adalah proses ekstraksi informasi atau pola yang berguna dari kumpulan data dalam database besar. Proses ini terdiri dari beberapa tahapan utama, yaitu seleksi data, preprocessing, transformasi, data mining, dan interpretasi/evaluasi hasil."

    result = get_llama_score(question, answer)
    print("=== HASIL PENILAIAN ===")
    print(result)
'''
