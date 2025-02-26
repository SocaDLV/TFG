#V3 -> Canvie el preprocess_image() a un més eficient amb OpenCV

import os
import re
import time
import numpy as np
import psutil
import cv2

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

from pathlib import Path
from PIL import Image

#os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices=false'   #Desactivar XLA pq genera algún error, avoltes.
#os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices=true'    #Tindre-lo 'True' fa que vaja molt poc a poc.

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'                           # V2-> Desactivar búsqueda de GPU al sistema.

# Cargar el modelo preentrenado MobileNetV2 con pesos de ImageNet
model = MobileNetV2(weights='imagenet')

# Ruta de las imágenes de prueba (dataset ImageNet)
image_folder = Path(r'C:\Users\Ivan\Desktop\Asignatures5tcarrera\TFG\codi\MobileNetV2\tinyImageNet3K')

# Función para redimensionar las imágenes a 224x224, comprueba que tengan todos los canales RGB, y las prepara para la inferencia
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))  # Cambia a 224x224
    img = img.astype(np.float32)       # Asegura el tipo de datos
    img = img / 255.0                  # Normaliza los valores de píxeles (0-1)
    img = img[np.newaxis, :]           # Añadir dimensión de batch para que sea (1, 224, 224, 3)
    return img

# Función para ordenar por número dentro del nombre del archivo
def natural_sort_key(filename):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', filename)]

# Función para medir el uso de CPU y tiempos de inferencia
def classify_and_measure(image_folder):
    image_files = [os.path.join(image_folder, f) for f in sorted(os.listdir(image_folder), key=natural_sort_key) if f.endswith(('.jpg', '.jpeg', '.png', '.JPEG'))]
    
    total_inference_time = 0
    cpu_usage_start = psutil.cpu_percent(interval=1)       # V2 -> Medir uso inicial de CPU, intervalo de 1 segundo para mayor precisión

    for img_file in image_files:
        img = preprocess_image(img_file)
        
        start_time = time.perf_counter()                   # V2 -> time.time per time.perf_counter
        preds = model.predict(img)                         # Hacer la predicción
        inference_time = time.perf_counter() - start_time  # Tiempo de inferencia, V2 -> time.time per time.perf_counter
        total_inference_time += inference_time

        # Decodificar y mostrar la predicción
        decoded_preds = decode_predictions(preds, top=1)[0]
        print(f"Predicción para {img_file}: {decoded_preds}")
        print(f"Tiempo de inferencia: {inference_time:.4f} segundos")
    
    cpu_usage_end = psutil.cpu_percent(interval=1)         # V2 -> Medir el uso del CPU al final, intervalo de 1 segundo para mayor precisión
    
    # Mostrar resultados de rendimiento
    print(f"Tiempo total de inferencia: {total_inference_time:.4f} segundos")
    print(f"Uso medio del CPU: {((cpu_usage_start + cpu_usage_end) / 2):.2f}%")

# Ejecutar la función de clasificación y medición
classify_and_measure(image_folder)