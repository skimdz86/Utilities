import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math
from numpy import loadtxt
import os
import sys


def plotGaussian(elements, figure, confidence):

	plt.figure(figure)
	plt.plot(elements, np.zeros_like(elements), 'rx')
	#plt.show()

	#os.system("pause")

	mu = np.average(elements)

	print('mu: ' + str(mu))

	variance = np.var(elements)
	print('variance: ' + str(variance))
	
	sigma = math.sqrt(variance)
	print('sigma: ' + str(sigma))
	
	conf_int = stats.norm.interval(confidence, loc=mu, scale=sigma)
	print('Confidence interval for ' + str(confidence) + ': ' + str(conf_int))
	
	plt.plot(conf_int, np.zeros_like(conf_int), 'bo')
	plt.axvline(x=conf_int[0], ymin=0, ymax=1, color='g', linestyle='--')
	plt.axvline(x=conf_int[1], ymin=0, ymax=1, color='g', linestyle='--')
	
	x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
	plt.plot(x, stats.norm.pdf(x, mu, sigma))
	#plt.show()
	return plt



if __name__ == "__main__":
	#print(f"Arguments count: {len(sys.argv)}")
	#for i, arg in enumerate(sys.argv):
	#	print(f"Argument {i:>6}: {arg}")
	
	if len(sys.argv) >=2:
		confidence = float(sys.argv[1])
	else:
		confidence = 0.90

	# caricamento array
	elements = loadtxt("Times_1.txt", comments="#", delimiter="\n", unpack=False)
	print(elements)
	plt = plotGaussian(elements, 'Times 1 probability distribution - confidence ' + str(confidence), confidence)



	# caricamento array
	elements = loadtxt("Times_2.txt", comments="#", delimiter="\n", unpack=False)
	print(elements)
	plt = plotGaussian(elements, 'Times 2 probability distribution - confidence ' + str(confidence), confidence)

	plt.show()

	os.system("pause")



