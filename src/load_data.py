import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(dataset_path='../data'):
	X = []
	Y = []
	df = pd.read_csv(dataset_path + '/covidontario.csv')
	for idx, row in df.iterrows():
		x = (
			row['numdeaths'],
			row['numtested'],
			row['numrecover'],
			row['ratetested'],
			row['numtoday'],
			row['percentoday'],
			row['ratetotal'],
			row['numdeathstoday'],
			row['percentactive'],
			row['numactive']
		)
		X.append(x)
		Y.append(row['numconf'])
	X = np.array(X)
	Y = np.array(Y)
	(train_x, test_x, train_y, test_y) = train_test_split(
		X,
		Y,
		test_size=.2,
		shuffle=False,
		random_state=42,
	)
	return (train_x, test_x, train_y, test_y)


