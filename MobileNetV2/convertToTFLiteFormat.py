import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2

# Cargar el modelo MobileNetV2 preentrenado con pesos de ImageNet
model = MobileNetV2(weights='imagenet')

# Configurar el convertidor de TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # Activar optimizaciones
converter.target_spec.supported_types = [tf.float16]  # Reducir precisión a float16 (opcional, para reducir tamaño y mejorar rendimiento)

# Convertir el modelo a formato TensorFlow Lite
try:
    tflite_model = converter.convert()
    # Guardar el modelo convertido
    with open("mobilenet_v2_optimized.tflite", "wb") as f:
        f.write(tflite_model)
    print("Conversión a TensorFlow Lite exitosa.")
except Exception as e:
    print("Error en la conversión:", e)