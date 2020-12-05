import torch
import torch.nn as nn

class BiLSTM(nn.Module):
	def __init__(self, input_size, hidden_size, num_layers, num_classes, device=None, batch_size=1):
		super(BiLSTM, self).__init__()
		self.input_size = input_size
		self.hidden_size = hidden_size
		self.batch_size = batch_size
		self.num_layers = num_layers
		self.device = device

		self.lstm = nn.LSTM(
			input_size,
			hidden_size,
			num_layers,
			bidirectional=True
		)
		# hidden_size * 2 to account for both forward and reversed hidden states.
		# 1 since we have a single output.
		self.fc = nn.Linear(hidden_size * 2, 1)

	
	def init_hidden(self):
		return (torch.zeros(self.num_layers, self.batch_size, self.hidden_size).to(self.device),
				torch.zeros(self.num_layers, self.batch_size, self.hidden_size).to(self.device))

	def forward(self, x):
		print(x.shape)
		print(x)
		out, self.hidden = self.lstm(x.view(len(x), self.batch_size, -1), self.hidden)
		out = self.fc(out.view(len(x), -1))
		return out.view(-1)
