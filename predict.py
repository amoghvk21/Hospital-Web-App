from keras.models import load_model
import tensorflow as tf
from PIL import Image
from numpy import asarray
import numpy as np


def predict(img): 
    with tf.device('/gpu:0'):
        
        # Load the pre trained model
        model = load_model('neuralnet_model')

        # Black and white
        img = img.convert('1')

        # Change dimentions
        img = img.resize((256, 256))

        # Convert into numpy array
        img_data = asarray(img)
        
        # Change dimentions
        x = np.array(img_data).reshape(-1, 256, 256, 1)

        # Predict
        y = model.predict(x)

        # Return the diagnois
        i = y.argmax()
        if i == 0:
            return 'Normal'
        elif i == 1:
            return 'COVID'
        else:
            return 'Viral Pneumonia'