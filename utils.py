import numpy as np

def flattenList(multList):
	return np.array([item for sublist in multList for item in sublist])