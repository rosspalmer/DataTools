
import matplotlib.pyplot as plt

def prob_scatter(x, y, prob):

	plt.gcf().clear()
	plt.scatter(x, y, s=100, c=prob, alpha=0.5, cmap='brg')
	plt.show()

