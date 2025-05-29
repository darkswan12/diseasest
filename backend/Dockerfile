# Gunakan image python
FROM python:3.9-slim

# Set direktori kerja di container
WORKDIR /app

# Salin requirements dan install dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file
COPY . .

# Port untuk Cloud Run
ENV PORT=8080

# Jalankan aplikasi dengan Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
