import pandas as pd
import numpy as np
from pandas.core.algorithms import value_counts
import faunadb as f

df = pd.read_csv('SampleUserMatrix.csv')
df['UID'] = df.columns.values
df = df.set_index('UID')
df.columns = df.columns.map(str)
df.index = df.index.map(str)
df2 = pd.read_csv('InactiveUsers.csv')
inactiveUsers = df2['Users']

def updateWeights(user):
    for i in df.loc[user]:
        if df.columns[i] in inactiveUsers:
            continue
        value = generateWeight(df.columns[i], user)
        i = value
    df.to_csv('SampleUserMatrix.csv', index=False)

def generateWeight(target, user):
    value = 0
    value = value + favoriteSports(target, user)
    value = value + levelOfCompetition(target, user)
    value = value + Friends(target, user)
    value = value + FrequentLocations(target, user)
    return value

def favoriteSports(target, user):
    s = 0
    sportsuser = ['Tennis', 'Soccer', 'Football']
    sportstarget = ['Basketball', 'Tennis', 'Football', 'Rugby', 'Sped']
    #sportsuser = f.Get(f.Ref(f.Collection('users'), user).sports) or whatever bullshit fauna does to access UIDs
    #sportstarget = f.Get(f.Ref(f.Collection('users'), target).sports) or whatever bullshit fauna does to access UIDs
    for i in sportsuser:
        for x in sportstarget:
            if i == x:
                s = s + 1
    s = s/len(sportsuser) * 1.5 * 0.20
    if (s > 0.20):
        return 0.35
    else:
        return s

def levelOfCompetition(target, user):
    l = 0
    LOCUser = [('Tennis', 0.3), ('Football', 0.5), ('Softball', 0.9)]
    LOCTarget = [('Tennis', 0.5), ('Trigonometry', 0.5), ('PlayingLeague', 0.9)]
    #LOCUser = f.Get(f.Ref(f.Collection('users'), user).LOC) or whatever bullshit fauna does to access UIDs
    #LOCTarget = f.Get(f.Ref(f.Collection('users'), target).LOC) or whatever bullshit fauna does to access UIDs  
    for m in LOCUser:
        for d in LOCTarget:
            if m[0] == d[0]:
                l = l + abs(m[1]-d[1])
                l = l/2
    
    l = l * 0.10
    return l

def Friends(target, user):
    f = 0
    friendsuser = ['396383', '135246', '136583']
    friendstarget = ['396383', '135246', '357082', '648294', '346042']
    #friendsuser = f.Get(f.Ref(f.Collection('users'), user).friends) or whatever bullshit fauna does to access UIDs
    #friendstarget = f.Get(f.Ref(f.Collection('users'), target).friends) or whatever bullshit fauna does to access UIDs
    for i in friendsuser:
        for x in friendstarget:
            if i == x:
                f = f + 1
    f = f/len(friendsuser) * 5 * 0.20
    if (f > 0.2):
        return 0.35
    else:
        return f

def FrequentLocations(target, user):
    fl = 0
    fluser = ['39638314', '13524651', '13658335']
    fltarget = ['39638325', '13524663', '35708216', '64829432', '34604267']
    #fluser = f.Get(f.Ref(f.Collection('users'), user).frequentLocations) or whatever bullshit fauna does to access UIDs
    #fltarget = f.Get(f.Ref(f.Collection('users'), target).frequentLocations) or whatever bullshit fauna does to access UIDs
    for i in fluser:
        for x in fltarget:
            if i == x:
                fl = fl + 1
    fl = fl/len(fluser) * 1.5 * 0.2
    if (fl > 0.2):
        return 0.20
    else:
        return fl






#favoriteSports, levelOfCompetition, Friends, Location, FrequentLocations, Age, Gender)