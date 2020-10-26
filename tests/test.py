from module.chartfetch import ChartFetch
from module import datehour
from datetime import datetime, timedelta
import pandas as pd
import tqdm
import numpy as np
from pprint import pprint

chartfetch = ChartFetch()
granularity, instrument, col = 'H1', 'USD_JPY', 't'

current = chartfetch.fetch_current(granularity, instrument, col)

print(current.head(3))
print(current.tail(3))
