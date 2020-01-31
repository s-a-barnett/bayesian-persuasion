import pymongo as pm
import json

# this auth.json file contains credentials
with open('auth.json') as f :
    auth = json.load(f)
user = auth['user']
pswd = auth['password']
host = auth['host']

# initialize mongo connection
conn = pm.MongoClient('mongodb://{}:{}@127.0.0.1'.format(user, pswd))

# get database for this project
db = conn['bayesian-persuasion']

# get stimuli collection from this database
print('possible collections include: ', db.collection_names())
stim_coll = db['experiment1_stimuli']

# empty stimuli collection if already exists
# (note this destroys records of previous games)
if stim_coll.count() != 0 :
    stim_coll.drop()

# Loop through evidence and insert into collection
for stick1 in [.1, .2, .3, .4] :
    for stick2 in  [.7] : # Change this back for real experiment
        packet = {'agent1stick' : stick1, 'agent2stick' : stick2, 'numGames': 0, 'games' : []}
        stim_coll.insert_one(packet)

print('checking one of the docs in the collection...')
print(stim_coll.find_one())
