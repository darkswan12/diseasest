# Gunakan image resmi Python
FROM python:3.10-slim

# Set direktori kerja
WORKDIR /app

# Salin requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua isi backend ke container
COPY . .

# Jalankan aplikasi Flask
CMD ["python", "app.py"]
