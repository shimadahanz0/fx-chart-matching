from .chartfetch import ChartFetch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns #importするだけでスタイルがSeabornになる


def normalize(array, max, min):
	return (array - array.min()) / (array.max() - array.min()) * (max - min) + min

def compare(num):
	chartfetch = ChartFetch()
	sns.set_style("whitegrid")
	granularity, instrument, col = 'H1', 'USD_JPY', 'c'

	current = chartfetch.fetch_current(granularity, instrument, col).values
	compare = pd.read_csv('data/compare-20130324-20201017.csv.zip').values

	compare = np.apply_along_axis(normalize, 1, compare, current.max(), current.min())
	compare = np.round(compare, decimals=3)

	crr_list = [np.corrcoef(current, i)[0, 1] for i in compare[:, : len(current)]]

	crr_argsort = np.argsort(crr_list)[::-1]
	crr_score = np.round(np.sort(crr_list)[::-1]*100, decimals=2)[:num]
	matched = [compare[index] for index in crr_argsort[:num]]

	'''
	rcParams['font.family'] = 'DejaVu Sans Mono'
	plt.plot(np.arange(0, len(matched[0])), matched[0], label='Matched_1')
	plt.plot(np.arange(0, len(matched[1])), matched[1], label='Matched_2')
	plt.plot(np.arange(0, len(matched[2])), matched[2], label='Matched_3')
	plt.plot(np.arange(0, len(current)), current, label='Current')
	plt.xlabel('Time [hour]')
	plt.ylabel('USD_JPY [yen/$]')
	plt.legend()
	plt.savefig("matching.png", dpi=500)
	'''
