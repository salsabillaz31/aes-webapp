import requests

data = {
    "pertanyaan": "Apa itu KDD?",
    "jawaban": "gatau",
    "id_soal": "DMQ1"
}

response = requests.post("http://127.0.0.1:8000/score", json=data)
print(response.status_code)
print(response.json())
