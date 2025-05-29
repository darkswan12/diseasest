# 🦠 Diseasest

**Diseasest** adalah aplikasi web berbasis Python dan JavaScript yang bertujuan untuk membantu pengguna dalam menganalisis dan memprediksi penyakit berdasarkan gejala yang dimasukkan. Proyek ini menggabungkan antarmuka pengguna yang intuitif dengan backend yang kuat untuk memberikan prediksi yang akurat.

🌐 **Coba aplikasinya di sini**: [https://diseasest.netlify.app/](https://diseasest.netlify.app/)

---

## ✨ Fitur

- 🔍 **Prediksi Penyakit**: Menggunakan algoritma machine learning untuk memprediksi kemungkinan penyakit berdasarkan gejala yang Anda masukkan.
- 💡 **Antarmuka Interaktif**: Desain responsif dan mudah digunakan, cocok untuk semua kalangan.
- 📊 **Visualisasi Data**: Menyediakan informasi hasil prediksi dalam bentuk yang mudah dipahami.
- 🔄 **Integrasi Backend & Frontend**: Arsitektur proyek terstruktur dengan baik dan terpisah antara backend dan frontend.

---

## 🛠️ Teknologi yang Digunakan

- 🐍 **Backend**: Python
- 🌐 **Frontend**: JavaScript, HTML, CSS
- 🐳 **Docker**: Untuk containerization dan kemudahan deployment

---

## 📁 Struktur Proyek

```
diseasest/
├── backend/
│   └── ... (kode backend)
├── frontend/
│   └── ... (kode frontend)
├── Dockerfile
├── README.md
└── ...
```

---

## 🚀 Cara Menjalankan Proyek

1. **Clone repositori ini**:

   ```bash
   git clone https://github.com/darkswan12/diseasest.git
   cd diseasest
   ```

2. **Bangun dan jalankan dengan Docker**:

   Pastikan Docker telah terinstal di sistem Anda.

   ```bash
   docker build -t diseasest-app .
   docker run -p 8000:8000 diseasest-app
   ```

3. **Akses aplikasi di browser**:

   Buka [http://localhost:8000](http://localhost:8000) untuk mulai menggunakan aplikasi.

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Jika Anda ingin membantu mengembangkan proyek ini:

1. Fork repositori ini
2. Buat branch fitur (`git checkout -b fitur-baru`)
3. Commit perubahan Anda (`git commit -m 'Tambah fitur baru'`)
4. Push ke branch (`git push origin fitur-baru`)
5. Buat Pull Request

---

## 📝 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

---

Terima kasih telah mengunjungi proyek ini! 🎉 Jangan lupa untuk memberikan ⭐ di GitHub jika Anda merasa proyek ini bermanfaat.
