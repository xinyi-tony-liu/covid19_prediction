import matplotlib.pyplot as plt

def plot_learning_curve(iter_array, train_mse, test_mse, plot):
	plt.title('MSE Training vs. Test')
	plt.plot(iter_array, train_mse, label='Training', linewidth=5)
	plt.plot(iter_array, test_mse, label='Test', linewidth=5)
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)
	plt.xlabel('iterations', fontsize=30)
	plt.ylabel('MSE', fontsize=30)
	plt.legend(loc='best', fontsize=20)
	plt.savefig(plot)
