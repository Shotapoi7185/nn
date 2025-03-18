from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import io
from PIL import Image
import base64
from io import BytesIO
import tensorflow as tf
# สร้างแอป Flask
app = Flask(__name__)
tf.config.set_visible_devices([], 'GPU')
knn = joblib.load('knn_model.pkl')
svm = joblib.load('svm_model.pkl')
nn = load_model('best_model.h5')
# สร้าง route สำหรับ API
CORS(app,origins="*")
@app.route('/')
def hello_world():
    return jsonify(message=[0,1,2,3])

# กำหนด route สำหรับทำนาย (predict)
@app.route('/predict_knn', methods=['POST'])
def predict_knn():
    input_data = None
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({'error': 'Invalid JSON format or no data provided'}), 400
        
        if 'input' not in data:
            return jsonify({'error': 'No input data provided'}), 400
        
        input_data = np.array(data['input']).reshape(1, -1)
        prediction = knn.predict(input_data)
        print(f"Input data: {input_data}")
        print(f"Prediction: {prediction}")
        print(prediction)
        return jsonify(prediction=prediction.tolist())

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict_svm', methods=['POST'])
def predict_svm():
    try:
        data = request.get_json()

        if 'input' not in data:
            return jsonify({'error': 'No input data provided'}), 400
        
        input_data = np.array(data['input']).reshape(1, -1)
        
        prediction = svm.predict(input_data)

        return jsonify(prediction=prediction.tolist())

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/predict_nn', methods=['POST'])
def predict_nn():
    try:
        data = request.get_json()

        if 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400

        image_data = data['image']
        
        # แปลง Base64 เป็นภาพ
        img_data = base64.b64decode(image_data.split(',')[1])  # ลบ "data:image/jpeg;base64," ออกก่อน

        # แปลง img_data เป็นไฟล์ภาพที่สามารถใช้ใน Keras ได้
        img = Image.open(BytesIO(img_data))
        img = img.resize((224, 224))  # ปรับขนาดภาพตามที่โมเดลต้องการ
        img_array = np.array(img)  # แปลงเป็น numpy array
        img_array = np.expand_dims(img_array, axis=0)  # เพิ่มมิติ
        img_array = img_array / 255.0  # Normalize ข้อมูล

        # ทำนายผล
        prediction = nn.predict(img_array)

        return jsonify(prediction=prediction.tolist())

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)