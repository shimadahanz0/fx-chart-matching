from datetime import timedelta, datetime
import pandas as pd

def range_hours(start, end):
     '''指定区間のdatetimeリスト'''
     period = end - start
     num_of_hour = period.days * 24 + int(period.seconds / 60 / 60) + 24 # 日数*24 + 秒数/60/60 + endの日分
     return [start + timedelta(hours=i) for i in range(num_of_hour)]

def now():
     '''UTCでの現在時間(時間で丸めている)'''
     return pd.Series([datetime.now()]).dt.round('H')[0] - timedelta(hours=9)
