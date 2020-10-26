from module.chartfetch import ChartFetch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns #importするだけでスタイルがSeabornになる


def normalize(array, max, min):
     return (array - array.min()) / (array.max() - array.min()) * (max - min) + min

if __name__ == "__main__":
     chartfetch = ChartFetch()
     sns.set_style("whitegrid")
     granularity, instrument, col = 'H1', 'USD_JPY', 'c'

     current = chartfetch.fetch_current(granularity, instrument, col).values
     compare = pd.read_csv('data/compare-20130324-20201017.csv.zip').values

     compare = np.apply_along_axis(normalize, 1, compare, current.max(), current.min())
     compare = np.round(compare, decimals=3)

     crr_list = [np.corrcoef(current, i)[0, 1] for i in compare[:, : len(current)]]

     max_crr_value, max_crr_index = np.max(crr_list), np.argmax(crr_list)
     matched = compare[max_crr_index]

     print(round(max_crr_value*100, 2))

     #xticks = ['Sun-22:00', 'Mon-00:00', 'Tue-00:00', 'Wed-00:00', 'Thu-00:00', 'Fri-00:00', 'Fri-20:00']
     rcParams['font.family'] = 'DejaVu Sans Mono'
     plt.plot(np.arange(0, len(matched)), matched, label='Matched')
     plt.plot(np.arange(0, len(current)), current, label='Current')
     plt.xlabel('Time [hour]')
     plt.ylabel('USD_JPY [yen/$]')
     #plt.xticks([0, 2, 26, 60, 84, 108, 120], xticks, rotation=90)
     plt.legend()
     plt.savefig("matching.png", dpi=500)
