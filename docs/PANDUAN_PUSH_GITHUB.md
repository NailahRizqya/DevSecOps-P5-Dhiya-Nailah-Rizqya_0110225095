# Panduan Membuat Repo & Menjalankan Pipeline

1. Buka https://github.com/new
   - Repository name : `devsecops-p5-<NIM-anda>`
   - Visibility      : **Public**
   - JANGAN centang "Add README" (sudah ada di folder ini)
2. Di terminal, dari dalam folder proyek ini:
   ```bash
   git init -b main
   git add .
   git commit -m "feat: SecureNotes API + DevSecOps pipeline"
   git remote add origin https://github.com/<USERNAME>/devsecops-p5-<NIM>.git
   git push -u origin main
   ```
3. Buka tab **Actions** -> workflow "DevSecOps Pipeline" otomatis berjalan.
4. Screenshot yang dibutuhkan laporan:
   - (a) halaman utama repo (nama repo, daftar file, README)
   - (b) tab Actions (daftar run berhasil)
   - (c) detail run: graf job build -> sast-scan
   - (d) log step "Security Quality Gate" (PASSED)
   - (e) bagian Artifacts (bandit-reports, coverage-report)
   - (f) skenario gagal: Pull Request dengan `demo_vuln.py` -> sast-scan merah
5. (Opsional, disarankan) Settings -> Branches -> Add rule untuk `main`:
   aktifkan "Require status checks to pass" dan pilih `Build & Unit Test`
   serta `SAST Scan (Bandit)` agar gate benar-benar memblokir merge.
