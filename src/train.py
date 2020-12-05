# Imports
import argparse
import torch
import torchvision
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import torchvision.datasets as datasets
import torchvision.transforms as transforms

from bilstm import BiLSTM
from helpers import *
from load_data import *

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Parse input arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
				help="path to input dataset")
ap.add_argument("-e", "--epochs", type=int, default=25,
				help="# of epochs to train our network for")
ap.add_argument("-p", "--plot", type=str, default="plot.png",
				help="path to output loss/accuracy plot")
args = vars(ap.parse_args())

# Parameters:
# numconf
# numdeaths
# numdeaths
# numtested
# numrecover
# ratetested
# numtoday
# percentoday
# ratetotal
# numdeathstoday
# percentactive
# numactive

# Hyperparameters
num_layers = 2
hidden_size = 256
num_classes = 10
learning_rate = 0.001
batch_size = 64
num_epochs = 5

# Create RatingDataset class to help with loading data
class CovidDataset(Dataset):
	def __init__(self, data, targets):
		self.data = data
		self.targets = targets
	
	def __len__(self):
		return len(self.data)
	
	def __getitem__(self, idx):
		return torch.FloatTensor(self.data[idx]).to(device), \
				torch.FloatTensor([self.targets[idx]]).to(device)

# Load data
train_x, test_x, train_y, test_y = load_data(args['dataset'])

# Create dataloaders
train_loader = DataLoader(CovidDataset(train_x, train_y), shuffle=False)
test_loader = DataLoader(CovidDataset(test_x, test_y), shuffle=False)

# Initialize network
model = BiLSTM(len(train_x[0]), hidden_size, num_layers, num_classes, device).to(device)

# Loss and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

train_mse = []
test_mse = []

# Train Network
for epoch in range(args['epochs']):
	for batch_idx, (data, targets) in enumerate(train_loader):
		optimizer.zero_grad()

		model.hidden = model.init_hidden()

		# forward
		y_pred = model(data)

		# calculate loss
		loss = criterion(prediction, targets)

		# backward
		loss.backward()

		# gradient descent or adam step
		optimizer.step()

		train_loss_tot += loss.item()

	test_loss_tot = 0
	test_count = 0
	with torch.no_grad():
		for i, (data, targets) in enumerate(test_dataloader):
			test_count += 1

			# Predict rating and calculate loss
			prediction = model(row_batch.squeeze(), col_batch.squeeze())
			prediction = torch.diagonal(prediction)
			loss = loss_func(prediction, rating_batch.squeeze())

			# Update loss total
			test_loss_tot += loss.item()

	train_mse += [train_loss_tot / train_count]
	test_mse += [test_loss_tot / test_count]
	print('[epoch:{}] Train MSE: {}, Test MSE: {}'.format(
		epoch,
		train_mse[-1],
		test_mse[-1]
	))

print('Finished training!')
plot_learning_curve(list(range(args['epochs'])), train_mse, test_mse, args['plot'])
