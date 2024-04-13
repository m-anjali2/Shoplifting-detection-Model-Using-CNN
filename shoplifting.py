# -*- coding: utf-8 -*-
"""Shoplifting.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/112kV9DqbFBXOMVOMteYwLydOSN-H8Vne
"""

from google.colab import drive
drive.mount('/content/drive')

# Import necessary libraries
import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Set paths and parameters
train_path = '/content/drive/MyDrive/Shoplifting/shoplifting.v1i.tensorflow/train'
valid_path = '/content/drive/MyDrive/Shoplifting/shoplifting.v1i.tensorflow/valid'
batch_size = 32
epochs = 10
img_height = 180
img_width = 180

# Data preprocessing using ImageDataGenerator
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255)
valid_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary')

valid_generator = valid_datagen.flow_from_directory(
    valid_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary')

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.summary()

from keras.layers import Flatten, Dense

# Flatten the data for the fully connected layer
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
from tensorflow.keras.optimizers import Adam

model.compile(optimizer=Adam(lr=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,
    epochs=epochs,
    validation_data=valid_generator)

train_steps_per_epoch = len(train_generator)
valid_steps_per_epoch = len(valid_generator)

print("Number of steps per epoch for training:", train_steps_per_epoch)
print("Number of steps per epoch for validation:", valid_steps_per_epoch)

import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions

def load_image(img_path, size=(180, 180)):
    img = image.load_img(img_path, target_size=size)
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    return preprocessed_img

img_path = '/content/drive/MyDrive/Shoplifting/shoplifting.v1i.tensorflow/ShoplifterTesting.jpg'
img = load_image(img_path)

# Make a prediction using the trained model
prediction = model.predict(img)

# Postprocess the prediction
if prediction > 0.8:
    print('The image is more likely to be a shoplifter.')
else:
    print('The image is more likely not to be a shoplifter.')