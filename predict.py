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
        img.convert('L')

        # Change dimentions
        img = img.resize((256, 256))

        # Convert into numpy array
        img_data = asarray(img)

        # Convert RGB to B or W
        new_data = []
        for i, d1 in enumerate(img_data):
            new_data.append([])
            for d2 in d1:
                if (d2 == [0, 0, 0]).all():
                    new_data[i].append(0)
                else:
                    new_data[i].append(1)
        new_data = np.array(new_data)
        
        # Change dimentions
        x = np.array(new_data).reshape(-1, 256, 256, 1)

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
                


img = Image.open('hospital/static/hospital/img/2.png')
print(predict(img))