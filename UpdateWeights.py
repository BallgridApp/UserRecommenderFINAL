import pandas as pd
import numpy as np
from pandas.core.algorithms import value_counts
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import json
import math

from pandas.core.frame import DataFrame

adminClient = FaunaClient(secret="fnAEVsNsPPACRXKB1RCH6UmlMwHCCEwut1rBXlEo")




def pullPost(ref, type):
    profile = adminClient.query(q.get(q.ref(q.collection("Posts"), ref)))
    profile = profile['data'][type]
    print(profile)
    #value = list(profile.keys())
    return profile


df = pd.read_csv('UserMatrix.csv')
df['UID'] = df.columns.values
df = df.set_index('UID')
df.columns = df.columns.map(str)
df.index = df.index.map(str)
#print(df)
df2 = pd.read_csv('InactiveUsers.csv')
inactiveUsers = df2['Users']
#print(df.loc['111111'])



def updateWeights(user):
    friendsuser = list(pullPost(user, 'friends'))
    for i in range(len(df.loc[user])):
        value = 0
        value = generateWeight(df.columns.values[i], user)
        if df.columns[i] in inactiveUsers: #fix this
            value = -1
        for x in range(len(friendsuser)):
            if df.columns[i] == str(friendsuser[x]):
                value = -1
      #  if df.columns[i] in friendsuser: #fix this
           # value = -1
        if df.columns[i] == str(user):
            value = -1
        df.loc[user, df.columns.values[i]] = value
    df.to_csv('UserMatrix.csv', index=False)


def generateWeight(target, user): #Call this
    value = 0
    value = value + favoriteSports(target, user)
    value = value + levelOfCompetition(target, user)
    value = value + Friends(target, user)
    value = value + Location(target, user)
    return value

def favoriteSports(target, user):
    s = 0
    sportsuser = list(pullPost(user, 'interests').keys()) # >>>>>
    sportstarget = list(pullPost(target, 'interests').keys()) #GET THESE USING JSON
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
    LOCUser = pullPost(user, 'interests')
    LOCTarget = pullPost(target, 'interests')
    #LOCUser = [('Tennis', 0.3), ('Football', 0.5), ('Softball', 0.9)]
    #LOCTarget = [('Tennis', 0.5), ('Trigonometry', 0.5), ('PlayingLeague', 0.9)]
    for m in range(0, len(list(LOCUser.keys()))):
        for d in range(0, len(list(LOCTarget.keys()))):
            if list(LOCUser.keys())[m] == list(LOCTarget.keys())[d]:
                l = l + abs(list(LOCUser.values())[0][1]-list(LOCTarget.values())[1][1])
                l = l/2
    
    l = l * 0.10
    return l

def Friends(target, user):
    f = 0
    friendsuser = list(pullPost(user, 'friends'))
    friendstarget = list(pullPost(target, 'friends'))
    #friendsuser = ['396383', '135246', '136583']
    #friendstarget = ['396383', '135246', '357082', '648294', '346042']
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

def Location(target, user):
    fl = 0
    fluser = pullPost(user, 'location')
    fltarget = pullPost(target, 'location')
    latUser = list(fluser.values())[0]
    longUser = list(fluser.values())[1]
    latTarget = list(fltarget.values())[0]
    longTarget = list(fltarget.values())[1]
    distance = math.pow(math.pow(abs(latUser-latTarget), 2) + math.pow(abs(longUser-longTarget), 2), 0.5)
    #fluser = ['39638314', '13524651', '13658335']
    #fltarget = ['39638325', '13524663', '35708216', '64829432', '34604267']
    if (distance < 5000):
        return 0.2
    if (distance < 50000):
        return 0.1
    else:
        return -0.2 # modifiable

def createUser(ref):
    df = pd.read_csv('UserMatrix.csv')
    df['UID'] = df.columns.values
    df = df.set_index('UID')
    df.columns = df.columns.map(str)
    df.index = df.index.map(str)
    array = []
    for i in range(0, len(df.columns.values)):
        array.append(0)
    df.loc[ref] = array
    print(df)
    updateWeights(ref)
    df.to_csv('UserMatrix.csv', index=False)

#createUser('135646374345341349')
#updateWeights('314549764296278608')
#updateWeights('314549764296278608')
#updateWeights('313209076380074563')
#updateWeights('313209568100352579')
#updateWeights('313209725554524739')
#updateWeights('313209891782132292')
#updateWeights('313208911481012803')
#updateWeights('313210180948984387')
#updateWeights('313210336718094916')
#updateWeights('313210489732596291')


#test out pikachuuu