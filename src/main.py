from flask import Flask, request, jsonify
import numpy
import pandas as pd
import tensorflow as tf
import io

MODEL_PATH = "src/models/model.h5"
CLASS_LABELS_PATH = "image_names.csv"
TOP_N = 5

app = Flask(__name__)

model = tf.keras.models.load_model(MODEL_PATH)
class_labels_csv = pd.read_csv(CLASS_LABELS_PATH)
class_labels = sorted(class_labels_csv['image_name'].tolist())
input_shape = (224, 224)

# print(class_labels)


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'status': 'failed', 'error': 'No image provided'}), 400

    file = request.files['image']

    if file.content_type not in ['image/jpeg', 'image/png']:
        return jsonify({'status': 'failed', 'error': 'File is not an image'}), 400

    if len(file.read()) > 10 * 1024 * 1024:  # 10MB limit
        return jsonify({'status': 'failed', 'error': 'File is too large'}), 400

    file.seek(0)  # Reset file pointer after reading

    try:
        # Convert file stream to a readable image
        img = tf.keras.preprocessing.image.load_img(
            io.BytesIO(file.read()), target_size=input_shape + (3,))
        img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
        img_array = numpy.expand_dims(img_array, axis=0)

        # Make prediction
        predictions = model.predict(img_array)[0]
        top_indices = predictions.argsort()[-TOP_N:][::-1]
        top_predictions = [
            {'label': class_labels[i], 'prediction': f"{predictions[i] * 100:.2f}%"} for i in top_indices
        ]

        # Return the result
        return jsonify({
            'status': 'success',
            'data': top_predictions
        }), 200

    except Exception as e:
        return jsonify({'status': 'failed', 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
