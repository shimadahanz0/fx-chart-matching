from oandapyV20 import API
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
import oandapyV20.endpoints.instruments as instruments
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import tqdm, os


class ChartFetch():
     def __init__(self):
          self.client = API(access_token='4f1a5dc04b44119b73a4434e3fb679b5-baa67c3b3ec9b51f16afaf5561f06c28')

     def align(self, df):
          df['t'] = pd.to_datetime(df['t']).dt.round('H')
          df = df.sort_values(['t']).reset_index(drop=True)
          return df


     def res_to_df(self, res):
          indicator = [[float(r['mid'][i]) for r in res] for i in ['o', 'h', 'l', 'c']]
          data = [[r['time'][:-11] for r in res], *indicator, [r['volume'] for r in res]]
          df = pd.DataFrame(columns=['t', 'o', 'h', 'l', 'c', 'v'])
          for i, v in enumerate(df):
               df[v] = data[i]
          return df


     def fetch_any(self, count, granularity, instrument, col):
          params = {
               "count":count,
               "granularity":granularity
          }
          res = []
          r = instruments.InstrumentsCandles(instrument=instrument, params=params)
          self.client.request(r)
          res.extend(r.response.get('candles'))
          df = self.res_to_df(res)
          df = self.align(df)
          return df[col]


     def fetch_range(self, start_day, end_day, granularity, instrument, col, save=True):
          path = './data/' + start_day.strftime('%Y%m%d') + '-' + end_day.strftime('%Y%m%d') + '-' + instrument + '.csv.zip'
          if os.path.exists(path):
               return pd.read_csv(path)
          nth, divider = 0, 100
          delta_day = (end_day - start_day)
          mod = timedelta(int(np.ceil(delta_day.days/divider)))
          bar = tqdm.tqdm(range(divider))
          res = []
          while start_day + mod * nth < end_day:
               start = datetime.strftime(start_day + mod * nth, '%Y-%m-%dT%H:%M:%SZ')
               end = datetime.strftime(min(start_day + mod * (nth + 1), end_day), '%Y-%m-%dT%H:%M:%SZ')
               params = {
                    "from": start,
                    "to": end,
                    "granularity": granularity
               }
               for r in InstrumentsCandlesFactory(instrument=instrument, params=params):
                    self.client.request(r)
                    res.extend(r.response.get('candles'))
               df = self.res_to_df(res)
               bar.update(1)
               nth += 1
          df = self.align(df)
          if save:
               df[col].to_csv(path, index=False, compression='zip')
          return df

     def fetch_current(self, granularity, instrument, col):
          utc_now = pd.Series([datetime.now()]).dt.round('H')[0] - timedelta(hours=9) # UTCでの現在の時間
          last_monday = utc_now - timedelta(days=utc_now.weekday(), hours=utc_now.hour+1) # 今週のはじめの取引時間
          diff = utc_now - last_monday
          hour_diff = diff.days * 24 + int(diff.seconds / 60 / 60)  # 週の初めから何時間か
          if hour_diff > 120:
               hour_diff = 120
          df = self.fetch_any(hour_diff, granularity, instrument, col)
          return df
