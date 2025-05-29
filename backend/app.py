import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import io
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Nonaktifkan optimisasi oneDNN
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__)
CORS(app, resources={r"/predict/*": {"origins": "*"}})

# Lokasi dan nama file model penyakit tanaman
disease_model_dir = "model"
disease_model_filename = "model_disease_full.h5"
disease_model_path = os.path.join(disease_model_dir, disease_model_filename)

# Variabel global untuk model penyakit tanaman
disease_model = None

# Informasi penyakit tanaman
disease_info = {
    'BACTERIAL SPOT': {
        'Description': "Bakteri menyebabkan bercak gelap pada daun dan buah tanaman.",
        'Treatment': "Kontrol dengan fungisida bakterisida, manajemen tanaman yang baik, dan sanitasi."
    },
    'BLACK MEASLES': {
        'Description': "Jamur ini menimbulkan bercak-bercak kecil berwarna coklat atau hitam pada daun.",
        'Treatment': "Penanganan dengan fungisida, menjaga kebersihan lingkungan, dan mengurangi kelembapan."
    },
    'BLACK ROT': {
        'Description': "Jamur yang menyebabkan bercak hitam pada daun tanaman cruciferous.",
        'Treatment': "Penanganan melalui kebersihan, penggunaan bibit sehat, dan menghindari kondisi lembap."
    },
    'CITRUS GREENING': {
        'Description': "Penyakit bakteri yang serius pada tanaman jeruk, menyebabkan daun menguning dan pertumbuhan abnormal.",
        'Treatment': "Pengendalian serangga vektor, pemangkasan, dan aplikasi antibiotik tertentu."
    },
    'LEAF BLIGHT': {
        'Description': "Jamur pada daun yang menimbulkan bercak coklat atau abu-abu.",
        'Treatment': "Penanganan dengan fungisida, membuang daun yang terinfeksi, dan menjaga kebersihan."
    },
    'LEAF MOLD': {
        'Description': "Jamur yang menimbulkan bercak putih keabu-abuan pada daun.",
        'Treatment': "Pengendalian dengan sirkulasi udara yang baik, membuang daun terinfeksi, dan mengelola kelembapan."
    },
    'LEAF SCORCH': {
        'Description': "Penyakit yang mengakibatkan daun kering dan kuning, sering disebabkan oleh bakteri atau jamur patogen.",
        'Treatment': "Pengelolaan air yang baik, penyemprotan fungisida, dan pemangkasan tanaman."
    },
    'LEAF SPOT': {
        'Description': "Bercak gelap atau coklat pada daun akibat jamur atau bakteri.",
        'Treatment': "Menjaga kebersihan, menyemprotkan fungisida, dan pengaturan irigasi."
    },
    'MOSAIC VIRUS': {
        'Description': "Virus yang menyebabkan daun menguning dengan pola mosaik atau bercak.",
        'Treatment': "Penggunaan bibit bebas virus, pengendalian serangga vektor, dan membuang tanaman terinfeksi."
    },
    'POWDERY MILDEW': {
        'Description': "Jamur yang tampak sebagai serbuk putih pada daun dan bagian tanaman lainnya.",
        'Treatment': "Penyemprotan fungisida, menjaga sirkulasi udara baik, dan menjaga tanaman tetap kering."
    },
    'RUST': {
        'Description': "Jamur yang menyebabkan bercak coklat atau oranye pada daun dan batang.",
        'Treatment': "Menggunakan bibit resisten, menyemprotkan fungisida, dan menjaga kebersihan."
    },
    'SCAB': {
        'Description': "Jamur yang menyebabkan bercak gelap atau abu-abu pada daun, buah, dan batang.",
        'Treatment': "Menjaga kebersihan, penggunaan bibit sehat, dan menyemprotkan fungisida."
    },
    'SPIDER MITES': {
        'Description': "Hama kecil yang merusak tanaman dengan membentuk jaring halus di bawah daun.",
        'Treatment': "Penyemprotan insektisida, menjaga kelembaban udara, dan membuang daun yang terinfeksi."
    },
    'TARGET SPOT': {
        'Description': "Jamur pada daun yang menyebabkan bercak gelap dengan tepi merah.",
        'Treatment': "Penyemprotan fungisida, sirkulasi udara baik, dan pemangkasan tanaman."
    },
    'YELLOW LEAF CURL VIRUS': {
        'Description': "Virus yang menyebabkan daun tanaman menguning, keriput, dan menggulung.",
        'Treatment': "Menggunakan bibit bebas virus, pengendalian serangga vektor, dan membuang tanaman terinfeksi."
    }
}

# Daftar kelas penyakit tanaman
class_names_disease = list(disease_info.keys())

def load_and_process_image(image_data, target_size=(224, 224)):
    img = Image.open(image_data)
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

@app.route('/')
def index():
    return 'API is running'

@app.route('/predict/disease', methods=['POST'])
def predict_disease():
    global disease_model
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Data gambar tidak ditemukan'}), 400

        image_file = request.files['image']
        image_data = io.BytesIO(image_file.read())
        img_array = load_and_process_image(image_data)

        if disease_model is None:
            # Muat model penyakit jika belum dimuat
            if os.path.exists(disease_model_path):
                disease_model = tf.keras.models.load_model(disease_model_path)  # Memuat model dari file
                print(f"Model penyakit berhasil dimuat dari {disease_model_path}")
            else:
                return jsonify({'error': f'File model penyakit tidak ditemukan di {disease_model_path}'}), 500

        # Lakukan prediksi
        predictions = disease_model.predict(img_array)
        predicted_class = tf.argmax(predictions[0]).numpy()
        confidence = predictions[0][predicted_class]
        is_above_threshold = bool(confidence > 0.5)

        # Dapatkan informasi penyakit tanaman
        predicted_disease = class_names_disease[predicted_class]
        disease_details = disease_info[predicted_disease]

        # Kembalikan hasil prediksi
        return jsonify({
            'message': 'Prediksi penyakit tanaman berhasil.',
            'data': {
                'hasil': predicted_disease,
                'skorKepercayaan': float(confidence * 100),
                'isAboveThreshold': is_above_threshold,
                'Description': disease_details['Description'],
                'Treatment': disease_details['Treatment']
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)