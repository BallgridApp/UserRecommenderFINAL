import faunadb as f
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import pandas as pd
import numpy as np
import datetime, time
from dateutil import parser
import threading

adminClient = FaunaClient(secret="fnAEVsNsPPACRXKB1RCH6UmlMwHCCEwut1rBXlEo")

df = pd.read_csv('UserMatrix.csv')
df['UID'] = df.columns.values
df = df.set_index('UID')
df.columns = df.columns.map(str)
df.index = df.index.map(str)
df2 = pd.read_csv('InactiveUsers.csv')

def checkInactiveWeekly():

    for i in range(0, len(df.index.values)): 
        flag = True
        fauna_response = adminClient.query(q.get(q.ref(q.collection("Posts"), df.index.values[i])))
        lastLoggedIn = parser.parse(fauna_response['data']['lastLogin'])
        delta = datetime.datetime.now() - lastLoggedIn
        if delta > datetime.timedelta(days=7):
            for x in df2['Users']:
                if str(x) == df.columns.values[i]:
                    flag = False
            if flag==True:
                print('Hey I\'m Kevin Xue. A novice UI developer. And I just want to let you know this string is not older than 7 days')
                df2.loc[len(df2.index)] = df.columns.values[i]

    df.to_csv('UserMatrix.csv', index=False)
    df2.to_csv('InactiveUsers.csv', index=False)

def checkActiveWeekly():
    df2 = pd.read_csv('InactiveUsers.csv')
    r = len(df2['Users'])
    for i in range(0, r): 
        fauna_response = adminClient.query(q.get(q.ref(q.collection("Posts"), str(df2['Users'][i]))))
        lastLoggedIn = parser.parse(fauna_response['data']['lastLogin'])
        print(lastLoggedIn)
        delta = datetime.datetime.now() - lastLoggedIn
        if delta < datetime.timedelta(days=7):
            print('Hey I\'m Kevin Xue. A novice UI developer. And I just want to let you know this string is younger than 7 days')
            print(list(df2['Users']))
            df2 = df2.drop(labels=i)
            r = r-1

    df.to_csv('UserMatrix.csv', index=False)
    df2.to_csv('InactiveUsers.csv', index=False)

threads = []
#print(type(list(df2['Users'])[1]))
#print(type(int(df2['Users'][0])))
#print(type(df.columns.values[0]))

def whileLoop():
    checkActiveWeekly()
    #checkInactiveWeekly()
    while True:
        time.sleep(604800)
        checkInactiveWeekly()
        checkActiveWeekly()

if __name__ == "__main__":
    x = threading.Thread(target=whileLoop, args=())
    threads.append(x)
    x.start()
    



#Done


    


