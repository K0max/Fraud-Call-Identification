import numpy as np

def cal_sensitivity(lr, clip, dataset_size):
    return 2 * lr * clip / dataset_size

def cal_sensitivity_MA(lr, clip, dataset_size):
    return lr * clip / dataset_size


def Laplace(epsilon):
    return 1 / epsilon


def Gaussian(epsilon, delta):
    return np.sqrt(2 * np.log(1.25 / delta)) / epsilon