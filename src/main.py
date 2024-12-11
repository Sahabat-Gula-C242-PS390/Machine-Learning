from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from keras.preprocessing.image import img_to_array, load_img
import io
import PIL

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('src/models/model.h5')

# Define the input shape
input_shape = (224, 224)

# Define class labels
class_labels = [
    "ABC-Kopi-Susu-30g", "Energen-Cokelat-34g", "Energen-Vanila-34g", "Good-Day-Cappuccino-25g", "Good-Day-Mocacinno-20g", "Indocafe-Coffeemix-20g", "Indomie-Goreng-72g", "Indomie-Kari-Ayam-72g", "Indomie-Soto-72g", "Indomilk-Kids-Cokelat-115ml", "Kapal-Api-Signature-25g", "Luwak-White-Coffee-20g", "Nabati-Coklat-37g", "Nabati-Keju-37g", "Nutrisari-Sweet-Orange-14g", "Sari-Gandum-Sandwich-Susu-Cokelat-27g", "Superstar-Chocolate-16g", "Tango-Royal-Chocolate-35g", "Teh-Kotak-Original-200ml","Ultra-Milk-Coklat-125ml"
]   

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']

    try:
        # Convert file stream to a readable image
        img = load_img(io.BytesIO(file.read()), target_size=input_shape + (3,))
        img_array = img_to_array(img) / 255.0  # Normalize the image
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        # Make prediction
        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions, axis=1)[0]
        confidence = float(np.max(predictions))

        # Get the class name
        predicted_class_name = class_labels[predicted_index]

        # Return the result
        return jsonify({
            'predicted_class': predicted_class_name,
            'confidence': confidence
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
