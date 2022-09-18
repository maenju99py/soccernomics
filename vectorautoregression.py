import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import Statsmodels
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from statsmodels.tools.eval_measures import rmse, aic

filepath = 'db/paraguay/data.csv'
df = pd.read_csv(filepath, index_col='league_date', sep=';')
print(df.shape)  # (123, 8)
df.tail()
