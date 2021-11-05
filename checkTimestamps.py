import faunadb as f
import pandas as pd
import numpy as np

df = pd.read_csv('UserMatrix.csv')
df['UID'] = df.columns.values
df = df.set_index('UID')
df.columns = df.columns.map(str)
df.index = df.index.map(str)
df2 = pd.read_csv('UserMatrix.csv')
print(df2)

def checkInactiveWeekly():

    for i in range(0, len(df.columns)):
        if (True):#f.Get(f.Ref(f.Collection('users'), '181388642088911360').timestamp is more than a week old)
            df2.loc[str(len(df2.index.values)), 'Users'] = df.columns[i]
            df[str(df.columns[i])] = -1
    df2.to_csv('InactiveUsers.csv', index=False)
    df.to_csv('UserMatrix.csv', index=False)





#Not Done, need to work on with Desi



    


