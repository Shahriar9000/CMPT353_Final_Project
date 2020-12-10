import sys

import pandas as pd 
import numpy as np 

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.SVM import SVC
from sklearn.neighbors import KNeighborsClassifier

from keras.models import Sequential
from keras.layers.core import Dense, Activation

from sklearn.decomposition import PCA


def useNeuralNet(X_train, X_valid, y_train, y_valid):

	model = Sequential()
	model.add(Dense(4, input_shape=(2,)))
	model.add(Activation('sigmoid'))
	model.add(Dense(3))
	model.add(Activation('sigmoid'))
	model.add(Dense(3))
	model.add(Activation('softmax'))

	model.compile(loss='categorical_crossentropy',
	        optimizer='sgd', metrics=['accuracy'])

	model.fit(X_train, y_train, epochs=2000, batch_size=75, verbose=0)
	print(model.evaluate(X_valid, y_valid)[1])

	y_probab = model.predict(X_valid)
	y_predict = model.predict_classes(X_valid)
	print(y_probab[:4])
	print(y_predict[:4])

	return


def main():
	data = pd.read_csv(infile)
	X = data.loc[:, data.columns != 'action']
	y = data['action']

	X_train, X_valid, y_train, y_valid = train_test_split(X, y)

	model = make_pipeline(
			PCA(1355)
			VotingClassifier([
			    ('knn', KNeighborsClassifier(5)),
			    ('svm', SVC(kernel='linear', C=0.1)),
			    ('tree1', RandomForestClassifier(max_depth=4)),
			    ('tree2', RandomForestClassifier(min_samples_leaf=10)),
			])
		)


	model.fit(X_train, y_train)
	print(model.score(X_train, y_train))
	print(model.score(X_valid, y_valid))

if __name__ == '__main__':
	input_data = sys.argv[1]
	main(input_data)




