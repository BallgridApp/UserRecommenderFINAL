import pandas as pd
import numpy as np
from pandas.core.construction import array
import faunadb as f

df = pd.read_csv('SampleUserMatrix.csv')
df['UID'] = df.columns.values
df = df.set_index('UID')
df.columns = df.columns.map(str)
df.index = df.index.map(str)

user = '201583'

print(df)

def giveRecommendation(user):
    arrayRecommendations = []
    dfUser = df.loc[user]
    recommendations = dfUser.to_numpy()
    for i in range(0, len(recommendations)):
        arrayRecommendations.append((recommendations[i], df.columns[i]))
    arrayRecommendations.sort(reverse=True)
    print(arrayRecommendations)
    Users = []
    for x in range(0, len(arrayRecommendations)):
        Users.append(arrayRecommendations[x][1])
    #friends = f.Get(f.Ref(f.Collection('users'), '181388642088911360').friends) or whatever bullshit fauna does to access UIDs
    # for p in friends:
        # Users.remove(p)
    UserRecommended = Users[0]
    print(Users)
    return UserRecommended

def rejection(user, target):
    df.loc[user, target] = df.loc[user, target] - 0.2
    if (df.loc[user, target] < 0.0):
        df.loc[user, target] = 0
# This will cause an eventual list of 0s for recommendation weights at which recommendations could be random, but if they're actively rejecting someone, this is just because we dont have enough users.
# Current solution is to update weekly and when the values fall below a certain threshold

rejection(user, '294835')

df.to_csv('SampleUserMatrix.csv', index=False)


giveRecommendation(user)
