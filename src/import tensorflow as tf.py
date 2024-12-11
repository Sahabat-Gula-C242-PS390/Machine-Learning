import tensorflow as tf

# Load model
model = tf.keras.models.load_model('final_model_2.h5')

# Cek layer terakhir
print(model.summary())  # Cek output layer
print(model.output)     # Cek jumlah kelas (biasanya dari softmax layer)

# Jika ada metadata class names, bisa dicek seperti ini:
if hasattr(model, 'class_names'):
    print(model.class_names)
else:
    print("Class names not available in the model.")
