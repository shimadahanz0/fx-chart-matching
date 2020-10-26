import numpy as np


def correlation(array_0, array_1):
     '''ピアソンの積率相関係数(一次元)'''
     length = len(array_0)
     diff = [array_0 - np.average(array_0), array_1 - np.average(array_1)]
     covariance = np.sum(diff[0] * diff[1]) / length # 共分散
     sd = [np.sqrt(np.sum(s ** 2) / length) for s in diff] # 標準偏差
     return covariance / (sd[0] * sd[1])
