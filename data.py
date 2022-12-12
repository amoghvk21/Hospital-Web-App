import numpy as np
from PIL import Image
from numpy import asarray
import tensorflow as tf
import pickle

with tf.device('/gpu:0'):

	# Creating training dataset
	x = []
	y = [[1, 0, 0], [0, 1, 0], [0, 0, 1]] * 1245
	labels = ['Normal', 'COVID', 'Viral Pneumonia']

	# Loads 1245 masks into x list
	for j in range(1245):
		for l in labels:
			image = Image.open(f'archive/COVID-19_Radiography_Dataset/{l}/masks/{l}-{j+1}.png')
			image.convert('L')
			img_data = asarray(image)

			new_data = []
			for i, d1 in enumerate(img_data):
				new_data.append([])
				for d2 in d1:
					if (d2 == [0, 0, 0]).all():
						new_data[i].append(0)
					else:
						new_data[i].append(1)
			x.append(new_data)
			print(f'{l}-{j+1}')

	x = np.array(x).reshape(-1, 256, 256, 1)
	y = np.array(y)

	# Save the contents of x and y
	pickle.dump(x, open("x_train.pickle", "wb"))
	pickle.dump(y, open("y_train.pickle", "wb"))


	# Creating testing dataset
	x = []
	y = [[1, 0, 0], [0, 1, 0], [0, 0, 1]] * 100
	labels = ['Normal', 'COVID', 'Viral Pneumonia']

	# Loads 300 masks into x list
	for j in range(1245, 1345):
		for l in labels:
			image = Image.open(f'archive/COVID-19_Radiography_Dataset/{l}/masks/{l}-{j+1}.png')
			image.convert('L')
			img_data = asarray(image)

			new_data = []
			for i, d1 in enumerate(img_data):
				new_data.append([])
				for d2 in d1:
					if (d2 == [0, 0, 0]).all():
						new_data[i].append(0)
					else:
						new_data[i].append(1)
			x.append(new_data)
			print(f'{l}-{j+1}')

	x = np.array(x).reshape(-1, 256, 256, 1)
	y = np.array(y)


	# Save the contents of x and y
	pickle.dump(x, open("x_test.pickle", "wb"))
	pickle.dump(y, open("y_test.pickle", "wb"))