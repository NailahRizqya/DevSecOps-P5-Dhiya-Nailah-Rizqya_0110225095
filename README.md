# SecureNotes API — DevSecOps Pipeline (Praktikum 5)

## 1. Nama Aplikasi & Fungsi
**SecureNotes API** adalah REST API sederhana untuk menyimpan catatan pribadi.
Pengguna dapat mendaftar, login (mendapat token bertanda tangan HMAC), lalu
membuat, mencari, membaca, dan menghapus catatan miliknya sendiri. Aplikasi
sengaja dirancang dengan praktik aman (password di-hash, query terparameter,
validasi input, secret dari environment variable) agar relevan sebagai objek
latihan DevSecOps.

| Endpoint | Metode | Keterangan |
|---|---|---|
| `/health` | GET | Cek status layanan |
| `/register` | POST | Daftar pengguna baru |
| `/login` | POST | Login, menghasilkan token |
| `/notes` | GET / POST | Daftar (opsional `?q=`) / buat catatan |
| `/notes/<id>` | GET / DELETE | Baca / hapus satu catatan |

## 2. Bahasa & Framework
- Python 3.12, Flask 3, SQLite (modul bawaan `sqlite3`)
- Pengujian: pytest + pytest-cov
- SAST: Bandit

Struktur source code:

```
app/__init__.py     application factory
app/config.py       konfigurasi (dari environment variable)
app/models.py       akses database (parameterized query)
app/routes.py       endpoint REST + autentikasi token
app/security.py     hashing password, pembuatan & verifikasi token
app/validators.py   validasi input
run.py              entry point
scripts/quality_gate.py   evaluator Quality Gate hasil Bandit
tests/              20 unit test
```

## 3. Cara Menjalankan
```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

export SECURENOTES_SECRET="isi-dengan-string-acak-panjang"   # Windows PowerShell: $env:SECURENOTES_SECRET="..."
python run.py                        # berjalan di http://127.0.0.1:5000
```

Contoh pemakaian:
```bash
curl -X POST localhost:5000/register -H "Content-Type: application/json" \
     -d '{"username":"budi","password":"rahasia123"}'
curl -X POST localhost:5000/login -H "Content-Type: application/json" \
     -d '{"username":"budi","password":"rahasia123"}'      # salin nilai "token"
curl -X POST localhost:5000/notes -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" -d '{"title":"Belanja","content":"susu"}'
```

Menjalankan test dan SAST secara lokal:
```bash
pytest --cov=app --cov=scripts --cov-fail-under=80
bandit -r app run.py -f json -o bandit-report.json --exit-zero
python scripts/quality_gate.py bandit-report.json
```

## 4. Overview Pipeline CI/CD
Workflow: `.github/workflows/devsecops.yml`
Pemicu: **push** ke `main` dan **pull_request** ke `main`. Runner: `ubuntu-latest`.

```
 push / PR ke main
        │
        ▼
 ┌──────────────────────────┐        ┌──────────────────────────────────┐
 │ Job 1: build             │ needs  │ Job 2: sast-scan                 │
 │ - install dependencies   │ ─────► │ - Bandit (SAST) -> laporan JSON  │
 │ - 20 unit test (pytest)  │        │ - Security Quality Gate          │
 │ - Coverage Gate >= 80%   │        │ - upload laporan sebagai artifact│
 └──────────────────────────┘        └──────────────────────────────────┘
```

**Quality Gate** (pipeline gagal bila dilanggar):
| Gate | Aturan |
|---|---|
| Coverage | total coverage `app` + `scripts` ≥ 80% |
| SAST – HIGH | 0 temuan |
| SAST – MEDIUM | 0 temuan |
| SAST – LOW | maksimal 5 temuan |

Untuk membuktikan gate bekerja, salin isi `docs/demo_vulnerable_sample.py.txt`
ke `app/demo_vuln.py` pada sebuah branch, buka Pull Request ke `main`, dan
job `sast-scan` akan **gagal** (HIGH=2, MEDIUM=2). Hapus file tersebut agar
pipeline kembali hijau.
