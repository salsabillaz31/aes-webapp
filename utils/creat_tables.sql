CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    role TEXT CHECK (role IN ('mahasiswa', 'dosen')) NOT NULL
);
CREATE TABLE list_soal (
    id_question TEXT PRIMARY KEY,  -- contoh: 'ML01'
	kompetensi TEXT NOT NULL,
    pertanyaan TEXT NOT NULL,
    keywords TEXT
);
CREATE TABLE nama_ujian (
    id_ujian SERIAL PRIMARY KEY,
    nama_ujian TEXT NOT NULL,
    dibuat_oleh TEXT REFERENCES users(username) ON DELETE SET NULL,
    tanggal_mulai TIMESTAMP,
    tanggal_selesai TIMESTAMP,
    aktif BOOLEAN DEFAULT TRUE
);
CREATE TABLE soal_ujian (
    id SERIAL PRIMARY KEY,
    id_ujian INTEGER REFERENCES nama_ujian(id_ujian) ON DELETE CASCADE,
    id_question TEXT REFERENCES list_soal(id_question) ON DELETE CASCADE,
    urutan INTEGER
);
CREATE TABLE jawaban_mahasiswa (
    username TEXT REFERENCES users(username) ON DELETE CASCADE,
    id_ujian INTEGER REFERENCES nama_ujian(id_ujian) ON DELETE CASCADE,
    id_question TEXT REFERENCES list_soal(id_question) ON DELETE CASCADE,
    jawaban TEXT NOT NULL,
    skor_keyword INTEGER,
    skor_llm INTEGER,
    skor_final INTEGER,
    waktu_submit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (username, id_ujian, id_question)
);
