import pymongo as pm
import json

# this auth.json file contains credentials
with open('auth.json') as f :
    auth = json.load(f)
user = auth['user']
pswd = auth['password']
host = auth['host']

# have to fix this to be able to analyze from local
conn = pm.MongoClient('mongodb://{}:{}@127.0.0.1'.format(user, pswd))
db = conn['bayesian-persuasion']
stim_coll = conn['stimuli']

for stick1 in range(.6, 1.1, .1) :
    for stick2 in range(0, .5, 0.1) :
        packet = {'stick1' : stick1, 'stick2' : stick2, 'games_already_used' : []}
        stim_coll.insert_one(packet)
