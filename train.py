from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D, Dropout
import tensorflow as tf
import pickle

with tf.device('/gpu:0'):

	# Get contents of x and y
	x = pickle.load(open("x_train.pickle", "rb"))
	y = pickle.load(open("y_train.pickle", "rb"))

	# Configure and train Neural Network
	model = Sequential()

	model.add(Conv2D(64, (3, 3), input_shape=(256, 256, 1)))
	model.add(Activation("relu"))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Conv2D(64, (3, 3)))
	model.add(Activation("relu"))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Flatten())

	model.add(Dense(20, activation='sigmoid'))

	model.add(Dense(20, activation='sigmoid'))

	model.add(Dense(3, activation='sigmoid'))

	model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

	model.fit(x, y, epochs=20)

	# Importing the testing dataset
	x = pickle.load(open("x_test.pickle", "rb"))
	y = pickle.load(open("y_test.pickle", "rb"))

	# Evaluating the model
	loss, acc = model.evaluate(x, y)
	print(f'Loss on test: {loss}')
	print(f'Accuracy on test: {acc}')

	answer = ''
	while answer not in ['y', 'n']:
		answer = input("Do you want to save? (y/n): ")
		if answer == 'y':
			model.save('neuralnet_model')
			print("saved")
		else:
			print("not saving")

# 0.3324086368083954 loss
# 0.8933333158493042 acc