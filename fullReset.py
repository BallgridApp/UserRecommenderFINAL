import pandas as pd
import numpy as np
import UpdateWeights as UW

df = pd.read_csv('UserMatrix.csv')
df['UID'] = df.columns.values
df = df.set_index('UID')
df.columns = df.columns.map(str)
df.index = df.index.map(str)

def fullReset():
    for i in range(0, df.shape[0]):
       UW.updateWeights(df.index.values[i])

fullReset()

# File Done
