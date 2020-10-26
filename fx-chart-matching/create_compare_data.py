from module.chartfetch import ChartFetch
from module import datehour
from datetime import datetime, timedelta
import pandas as pd
import tqdm
import numpy as np
from pprint import pprint


if __name__ == "__main__":
     chartfetch = ChartFetch()
     granularity, instrument, col = 'H1', 'USD_JPY', ['t', 'c']
     start, end = datetime(2013, 3, 24), datetime(2020, 10, 17)
     path = './data/compare-' + start.strftime('%Y%m%d') + '-' + end.strftime('%Y%m%d') + '.csv.zip'

     past_data = chartfetch.fetch_range(start, end, granularity, instrument, col)
     dh_list = pd.Series([str(h) for h in datehour.datehour_list(start, end)], name='t')

     merged = pd.merge(dh_list, past_data, on='t', how='left')
     merged_c = merged['c'].values
     weeks = pd.DataFrame([merged_c[i-120:i] for i in range(120, len(merged_c)) if not np.isnan(merged_c[i-120:i]).any()])
     weeks.to_csv(path, index=False, compression='zip')
     merged.to_csv('merged.csv', index=False)

     print(weeks.shape)
