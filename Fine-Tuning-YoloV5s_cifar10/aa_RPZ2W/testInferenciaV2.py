
# FUNCIONA MILLOR, basat en el test RPZ2W V3 de ResNet: mateixa velocitat pero oferix random sample del test

import os
import torch
import numpy as np
import time
from PIL import Image
from pathlib import Path
from random import sample
from torchvision import transforms

def main():
    
    transform = transforms.Compose([
        transforms.Resize((128,128)),       # OJO el resize estava mal, no es 224x224 sino 128x128
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Ruta del modelo
    model_path = os.path.expanduser('~/codi/TFG/Fine-Tuning-YoloV5s_cifar10/model/best16-1-25')

    # Cargar modelo
    model = torch.hub.load('ultralytics/yolov5' , 'custom' , path=str(model_path), force_reload=True) #, map_location=torch.device('cpu'))
    model.eval()  # Configurar el modelo en modo evaluación
    
    # Definir las clases CIFAR-10
    cifar10_classes = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                        'dog', 'frog', 'horse', 'ship', 'truck']

    # Cargar imágenes aleatorias de cada clase
    path = Path(os.path.expanduser('~/codi/TFG/Fine-Tuning-MNV2_v3_cifar10/aa_PC/content/images/test'))
    total_images = 3000

    # Recopilar imágenes equilibradas de cada subdirectorio
    images = []
    for class_dir in path.iterdir():
        if class_dir.is_dir():
            all_images = list(class_dir.rglob("*.jpg"))
            sampled_images = sample(all_images, min(len(all_images), total_images // len(cifar10_classes)))
            images.extend(sampled_images)

    # Inicializar variables para métricas
    correct_predictions = 0
    total_inference_time = 0

    # Procesar imágenes
    for image_path in images:
        label_str = image_path.parent.name
        true_class = cifar10_classes.index(label_str)

        # Procesar imagen
        image = Image.open(image_path)
        image_tensor = transform(image)
        image_tensor = image_tensor.unsqueeze(0)

        start_time = time.time()
        with torch.no_grad():
            prediction = model(image_tensor)
        inference_time = time.time() - start_time
        total_inference_time += inference_time

        predicted_class = prediction.argmax(dim=1).item()

        print(f"Predicción: {cifar10_classes[predicted_class]}, Tiempo: {inference_time:.4f}s")
        print(f"Etiqueta real: {cifar10_classes[true_class]}")

        if predicted_class == true_class:
            correct_predictions += 1
            print("✅")

    # Calcular el porcentaje de aciertos
    accuracy_result = (correct_predictions / len(images)) * 100
    print(f"Tiempo total de inferencia: {total_inference_time:.2f} segundos")
    print(f"Imágenes correctamente clasificadas: {correct_predictions}/{len(images)}")
    print(f"Porcentaje de aciertos: {accuracy_result:.2f}%")

if __name__ == '__main__':
    main()