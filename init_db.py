import sqlite3

# Koneksi ke database (akan otomatis dibuat jika belum ada)
conn = sqlite3.connect("warga.db")
cursor = conn.cursor()

# Buat tabel warga
cursor.execute("""
CREATE TABLE IF NOT EXISTS warga (
    no INTEGER PRIMARY KEY AUTOINCREMENT,
    no_kk TEXT,
    nik TEXT,
    nama_lengkap TEXT,
    tanggal_lahir TEXT,
    umur INTEGER,
    jenis_kelamin TEXT,
    pekerjaan TEXT,
    pendidikan TEXT
)
""")

# Tambahkan data contoh
cursor.execute("""
INSERT INTO warga (no_kk, nik, nama_lengkap, tanggal_lahir, umur, jenis_kelamin, pekerjaan, pendidikan)
VALUES ('320305100311', '3203050776500008', 'KOMAR', '1965-07-07', 61, 'Laki-Laki', 'Buruh Lepas', 'SD')
""")

conn.commit()
conn.close()

print("Database warga.db berhasil dibuat dengan tabel warga.")