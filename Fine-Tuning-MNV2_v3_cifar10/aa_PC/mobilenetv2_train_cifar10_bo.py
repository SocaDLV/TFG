# -*- coding: utf-8 -*-
"""MobileNetV2_train_cifar10_bo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nQXTtFGGJdaNvrvY53MNCgRyvv4QIOd5

##### Copyright 2019 The TensorFlow Authors.
"""

#@title Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#@title MIT License
#
# Copyright (c) 2017 François Chollet                                                                                                                    # IGNORE_COPYRIGHT: cleared by OSS licensing
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""# Binary Classification with MobileNetV2
In this tutorial, you will learn how to conduct a Binary classification using transfer learning on MobileNetV2 to classify images of daisies and dandelions.

For this notebook we will be using the Daisies and Dandelions dataset which can be found [here](https://public.roboflow.com/classification/flowers_classification/1). This dataset is a collection of 1821 images images in 2 different classes. This tutorial is based on Tensorflow's [Transfer Learning on MobileNetV2 notebook](https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/images/transfer_learning.ipynb).

### Accompanying Blog Post

We recommend that you follow along in this notebook while reading the blog post on [How to Train MobileNetV2 On a Custom Dataset](blog.roboflow.com/how-to-train-mobilenetv2-on-a-custom-dataset/) concurrently.

### Steps Covered in this Tutorial

* Download data using Roboflow and Convert it into a Tensorflow ImageFolder Format
* Construct the model
   * Load in the pretrained base model (and pretrained weights)
   * Stack the classification layers on top
* Train & Evaluate the model
* Fine Tune the model to increase accuracy after convergence

### **About**

[Roboflow](https://roboflow.com) enables teams to deploy custom computer vision models quickly and accurately. Convert data from to annotation format, assess dataset health, preprocess, augment, and more. It's free for your first 1000 source images.

**Looking for a vision model available via API without hassle? Try Roboflow Train.**

![Roboflow Wordmark](https://i.imgur.com/dcLNMhV.png)
"""

import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

"""## Data preprocessing

### Data download

We'll download our dataset from Roboflow. To download the dataset, use the "**Folder Structure**" export format.

To get your data into Roboflow, follow the [Getting Started Guide](https://blog.roboflow.ai/getting-started-with-roboflow/).

![folder.PNG](data:image/png;base64,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)
"""

# Commented out IPython magic to ensure Python compatibility.
#!curl -L "https://app.roboflow.com/ds/7G35G34bXR?key=sT0LplvmfA" > roboflow.zip; unzip roboflow.zip; rm roboflow.zip
# %cd /content/
# %mkdir images/
# %mv train images/train
# %mv test images/test
# %mv valid images/valid

"""We need to turn this dataset into a Tensorflow Dataset format. Fortunately, Tensorflow provides the ImageFolder dataset structure which is compatible with the format we downloaded the data in.

We will then use the builder to build the raw versions of our train, test, and validation data.
"""

import tensorflow_datasets as tfds
builder = tfds.folder_dataset.ImageFolder(r'C:\Users\Ivan\Desktop\Asignatures5tcarrera\TFG\codi\Fine-Tuning-MNV2_v3_cifar10\aa_PC\content\images')
print(builder.info)
raw_train = builder.as_dataset(split='train', shuffle_files=True)
raw_test = builder.as_dataset(split='test', shuffle_files=True)
raw_valid = builder.as_dataset(split='valid', shuffle_files=True)

"""Show images and labels from the training set:"""

tfds.show_examples(raw_train, builder.info)

"""### Format the Data

We can use the `tf.image` module to format the images for the task.

Resize the images to a fixed input size, and rescale the input channels to a range of `[-1,1]`

<!-- TODO(markdaoust): fix the keras_applications preprocessing functions to work in tf2 -->
"""

IMG_SIZE = 224 # All images will be resized to 224x224 -> for MobileNetV2

def format_example(pair):
  image, label = pair['image'], pair['label']
  image = tf.cast(image, tf.float32)
  image = (image/127.5) - 1
  image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
  return image, label

"""Apply this function to each item in the dataset using the map method:"""

train = raw_train.map(format_example)
validation = raw_valid.map(format_example)
test = raw_test.map(format_example)

"""Now shuffle and batch the data."""

BATCH_SIZE = 32
SHUFFLE_BUFFER_SIZE = 1000

train_batches = train.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
validation_batches = validation.batch(BATCH_SIZE)
test_batches = test.batch(BATCH_SIZE)

"""Inspect a batch of data:"""

for image_batch, label_batch in train_batches.take(1):
   pass

image_batch.shape

"""## Create the base model from the pre-trained convnets
You will create the base model from the **MobileNet V2** model developed at Google. This is pre-trained on the ImageNet dataset, a large dataset consisting of 1.4M images and 1000 classes. ImageNet is a research training dataset with a wide variety of categories like `jackfruit` and `syringe`. This base of knowledge will help us classify cats and dogs from our specific dataset.

First, you need to pick which layer of MobileNet V2 you will use for feature extraction. The very last classification layer (on "top", as most diagrams of machine learning models go from bottom to top) is not very useful.  Instead, you will follow the common practice to depend on the very last layer before the flatten operation. This layer is called the "bottleneck layer". The bottleneck layer features retain more generality as compared to the final/top layer.

First, instantiate a MobileNet V2 model pre-loaded with weights trained on ImageNet. By specifying the **include_top=False** argument, you load a network that doesn't include the classification layers at the top, which is ideal for feature extraction.
"""

IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)

# Create the base model from the pre-trained model MobileNet V2
base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet')

"""This feature extractor converts each `160x160x3` image into a `5x5x1280` block of features. See what it does to the example batch of images:
(Corregir, sería 240x240x3 que pasa a 7x7x1280)
"""

feature_batch = base_model(image_batch)
print(feature_batch.shape)

"""## Feature extraction
In this step, you will freeze the convolutional base created from the previous step and to use as a feature extractor. Additionally, you add a classifier on top of it and train the top-level classifier.

### Freeze the convolutional base

It is important to freeze the convolutional base before you compile and train the model. Freezing (by setting layer.trainable = False) prevents the weights in a given layer from being updated during training. MobileNet V2 has many layers, so setting the entire model's trainable flag to False will freeze all the layers.
"""

base_model.trainable = False

# Let's take a look at the base model architecture
base_model.summary()

"""### Add a classification head

To generate predictions from the block of features, average over the spatial `5x5` spatial locations, using a `tf.keras.layers.GlobalAveragePooling2D` layer to convert the features to  a single 1280-element vector per image.
"""

global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
feature_batch_average = global_average_layer(feature_batch)
print(feature_batch_average.shape)

"""Apply a `tf.keras.layers.Dense` layer to convert these features into a single prediction per image. You don't need an activation function here because this prediction will be treated as a `logit`, or a raw prediction value.  Positive numbers predict class 1, negative numbers predict class 0.
-> Canvi a Dense(10) per ser un model en 10 clases y salida softmax.
"""

# Cambiar la capa Dense para que tenga 10 salidas (una por cada clase)
prediction_layer = tf.keras.layers.Dense(10, activation='softmax')
prediction_batch = prediction_layer(feature_batch_average)
print(prediction_batch.shape)  # Debería ser (batch_size, 10)

"""Now stack the feature extractor, and these two layers using a `tf.keras.Sequential` model:"""

model = tf.keras.Sequential([
  base_model,
  global_average_layer,
  prediction_layer
])

"""### Compile the model

You must compile the model before training it.  Since there are two classes, use a binary cross-entropy loss with `from_logits=True` since the model provides a linear output. -> Mi modelo tiene 10 clases. Pasamos a:
"optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)"
"loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)"
"""

base_learning_rate = 0.001
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              metrics=['accuracy'])

model.summary()

"""The 2.5M parameters in MobileNet are frozen, but there are 1.2K _trainable_ parameters in the Dense layer.  These are divided between two `tf.Variable` objects, the weights and biases."""

len(model.trainable_variables)

"""### Train the model

After training for 20 epochs, you should see ~90%+ accuracy.

"""

initial_epochs = 20
validation_steps=20

loss0,accuracy0 = model.evaluate(validation_batches, steps = validation_steps)

print("initial loss: {:.2f}".format(loss0))
print("initial accuracy: {:.2f}".format(accuracy0))

history = model.fit(train_batches,
                    epochs=initial_epochs,
                    validation_data=validation_batches)

"""### Learning curves

Let's take a look at the learning curves of the training and validation accuracy/loss when using the MobileNet V2 base model as a fixed feature extractor.
"""

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.ylim([min(plt.ylim()),1])
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.ylim([0,1.0])
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
plt.show()

"""## Fine tuning
In the feature extraction experiment, you were only training a few layers on top of an MobileNet V2 base model. The weights of the pre-trained network were **not** updated during training.

One way to increase performance even further is to train (or "fine-tune") the weights of the top layers of the pre-trained model alongside the training of the classifier you added. The training process will force the weights to be tuned from generic feature maps to features associated specifically with the dataset.

Note: This should only be attempted after you have trained the top-level classifier with the pre-trained model set to non-trainable. If you add a randomly initialized classifier on top of a pre-trained model and attempt to train all layers jointly, the magnitude of the gradient updates will be too large (due to the random weights from the classifier) and your pre-trained model will forget what it has learned.

Also, you should try to fine-tune a small number of top layers rather than the whole MobileNet model. In most convolutional networks, the higher up a layer is, the more specialized it is. The first few layers learn very simple and generic features that generalize to almost all types of images. As you go higher up, the features are increasingly more specific to the dataset on which the model was trained. The goal of fine-tuning is to adapt these specialized features to work with the new dataset, rather than overwrite the generic learning.

### Un-freeze the top layers of the model

All you need to do is unfreeze the `base_model` and set the bottom layers to be un-trainable. Then, you should recompile the model (necessary for these changes to take effect), and resume training.
"""

base_model.trainable = True

# Let's take a look to see how many layers are in the base model
print("Number of layers in the base model: ", len(base_model.layers))

# Fine-tune from this layer onwards
fine_tune_at = 100

# Freeze all the layers before the `fine_tune_at` layer
for layer in base_model.layers[:fine_tune_at]:
  layer.trainable =  False

"""### Compile the model

Compile the model using a much lower learning rate.
"""

model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              optimizer = tf.keras.optimizers.Adam(learning_rate=base_learning_rate/10),
              metrics=['accuracy'])

model.summary()

len(model.trainable_variables)

"""### Continue training the model

If you trained to convergence earlier, this step will improve your accuracy by a few percentage points.
"""

fine_tune_epochs = 10
total_epochs =  initial_epochs + fine_tune_epochs

history_fine = model.fit(train_batches,
                         epochs=total_epochs,
                         initial_epoch =  history.epoch[-1],
                         validation_data=validation_batches)

"""Let's take a look at the learning curves of the training and validation accuracy/loss when fine-tuning the last few layers of the MobileNet V2 base model and training the classifier on top of it. The validation loss is much higher than the training loss, so you may get some overfitting.

You may also get some overfitting as the new training set is relatively small and similar to the original MobileNet V2 datasets.

After fine tuning the model nearly reaches 98% accuracy.
"""

acc += history_fine.history['accuracy']
val_acc += history_fine.history['val_accuracy']

loss += history_fine.history['loss']
val_loss += history_fine.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.ylim([0.8, 1])
plt.plot([initial_epochs-1,initial_epochs-1],
          plt.ylim(), label='Start Fine Tuning')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.ylim([0, 1.0])
plt.plot([initial_epochs-1,initial_epochs-1],
         plt.ylim(), label='Start Fine Tuning')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
plt.show()

"""# Infer on a Sample Image"""

test_batches = test.batch(1)
for image, label in test_batches.take(1):
  pass
plt.imshow(np.squeeze(image))
plt.title("Dandelion" if model.predict(image) > 0 else "Daisy")

# Tomar una imagen del conjunto de test
test_batches = test.batch(1)  # Crea batches de tamaño 1 para iterar
for image, label in test_batches.take(1):
    break  # Toma solo la primera imagen y su etiqueta

# Realizar la predicción
prediction = model.predict(image)  # Predice sobre la imagen
predicted_class = np.argmax(prediction)  # Clase con mayor probabilidad
true_class = label.numpy()[0]  # Clase verdadera
cifar10_classes = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                   'dog', 'frog', 'horse', 'ship', 'truck']


# Mostrar la imagen con la clase predicha
plt.imshow(np.squeeze(image))
plt.title(f"Predicted: {cifar10_classes[predicted_class]}, True: {cifar10_classes[true_class]}")
plt.axis('off')
plt.show()

"""EXTRA: Test para 3000 imágenes de test"""

import time
import numpy as np

# Definir el conjunto de clases de CIFAR-10
cifar10_classes = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                   'dog', 'frog', 'horse', 'ship', 'truck']

# Variables para métricas
correct_predictions = 0
total_images = 3000
start_time = time.time()  # Marca el inicio del tiempo

# Realizar inferencia sobre las 3000 imágenes
for i, (image, label) in enumerate(test.take(total_images)):
    # Realizar la predicción
    image = tf.expand_dims(image, axis=0)  # Añadir la dimensión de batch
    prediction = model.predict(image)  # Predicción para la imagen
    predicted_class = np.argmax(prediction)  # Clase con mayor probabilidad
    true_class = label.numpy()  # Clase verdadera

    # Comparar las predicciones y contar los aciertos
    if predicted_class == true_class:
        correct_predictions += 1

# Calcular el tiempo total de inferencia
end_time = time.time()
total_inference_time = end_time - start_time

# Calcular el porcentaje de aciertos
accuracy = (correct_predictions / total_images) * 100

# Mostrar resultados
print(f"Tiempo total de inferencia: {total_inference_time:.2f} segundos")
print(f"Imágenes correctamente clasificadas: {correct_predictions}/{total_images}")
print(f"Porcentaje de aciertos: {accuracy:.2f}%")

"""EXTRA: Descargar el modelo"""

# Paso 1: Guardar el modelo
model.save(Path(r'C:\Users\Ivan\Desktop\Asignatures5tcarrera\TFG\codi\Fine-Tuning-MNV2_v3_cifar10\aa_PC\mnv2_cifar10_bo_v1.h5'))  # Guardar en formato H5 (también puede ser .savedmodel)

# Paso 2: Descargar el archivo en Google Colab
#from google.colab import files
#files.download('mnv2_cifar10_bo_v1.h5')  # Cambia el nombre del archivo según el nombre de tu modelo

"""## Summary:

* **Using a pre-trained model for feature extraction**:  When working with a small dataset, it is a common practice to take advantage of features learned by a model trained on a larger dataset in the same domain. This is done by instantiating the pre-trained model and adding a fully-connected classifier on top. The pre-trained model is "frozen" and only the weights of the classifier get updated during training.
In this case, the convolutional base extracted all the features associated with each image and you just trained a classifier that determines the image class given that set of extracted features.

* **Fine-tuning a pre-trained model**: To further improve performance, one might want to repurpose the top-level layers of the pre-trained models to the new dataset via fine-tuning.
In this case, you tuned your weights such that your model learned high-level features specific to the dataset. This technique is usually recommended when the training dataset is large and very similar to the original dataset that the pre-trained model was trained on.

"""