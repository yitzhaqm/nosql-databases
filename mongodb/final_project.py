# Put the use case you chose here. Then justify your database choice:
# 
#                                  BIKE APP
#
# I chose MongoDB for efficient data fetching and GeoSpatial Indexing capabilities. Mainly the
# latter since that is hard to efficiently implement on other database types.

# Explain what will happen if coffee is spilled on one of the servers in your cluster, causing it to go down.
# In a Mongo Database, since the master server has copies, if coffee is ever spilled on one of
# the servers, one of the identical copies of the server will take the now-down server's place# and do its job without the outside clients seeing any interruption.
#
# What data is it not ok to lose in your app? What can you do in your commands to mitigate the risk of lost data?
# Most of the data is important, but data like user profile for logging in, passwords, names, 
# credit card information and as such require special attention as their loss could have unwan# ted consequences with the client. To mitigate the risk, I would increase atomization of data# storing and fetching in order to make sure the maximum amount of fetches and sets are 
# successful and data loss is averted. I can also alternatively handle loss of data by 
# repeated string with verification. Perhaps a simple handshake protocol to make sure gets and# sets have happened without any losses.
#############################################################################################

from pymongo import MongoClient
mongo = MongoClient()
db = mongo["bike-app"]

# Note: when I print, it generally means I am sending the info to the user.

# Note: the following series of actions isn't an exhaustive depiction of the actual
# user story. There are definitely some skipped actions.

# Action 1: User signs up for an account with name
users = db["users"]
name = "Abebe Bikila" #entered name

users.insert_one({
	"_id":users.stats()["count"],
	"name": name,
	"picture_url": "http://storage.bucket.stuff/",
	"age": 20,
	"shares": [],
	"location": {"type":"Point", "coordinates":[24, 34]},
	"journeys": [],
	"stations": [],
	"credit_card": "xxxxxxxxxxxxxxxx",
})
stats = db["stats"]
stats.update_one({
	"users":
	{
		"$inc":1
	}
})
# Action 2: App requests data on nearby bike stations to show the user
stations = db["stations"]
uid = users.stats()["count"] #requesting user database id
us = users.find({"_id":{"$eq":uid}})
stations.createIndex({location:"2dsphere"})
near = stations.find(
	{
		"locations":
			{
				"$near":
				{
				"$geometry":us[0]["location"],
				"$minDistance":0,
				"$maxDistance":1610
				}
			}
	}
)

for some in near:
	print(some)

# Action 3: User picks the nearest station from the provided list and we send the user more information about the station
picked = 3 # picked station id

found = stations.find({"_id": {"$eq":picked}})
for name in found:
	print(name) # should be a single one for current purposes

# Action 4: The user now picks a bike, destination/respective station
bike = 0
destination = {"type":"Point", "coordinates":[25,35]}
destination_station = stations.find({
	"locations":
	{
		"$near":
		{
		"$geometry":destination,
		"$minDistance":0,
		"$maxDistance":1610
		}
	}	
})[0]

users.find_and_modify({"query":{"_id":{"$eq":uid}},
		     "update":{"$push":{"bikes":bike}}
})
shares = db["shares"]
s = shares.stats()["count"]
shares.insert_one({
	"_id":s,
	"sharer":uid,
	"bike":bike,
	"journey": -1
})
users.findAndModify({
	"query":{"_id":uid},
	"update":{"$push":{"shares":s}}
})
bikes = db["bikes"]
bikes.update_one({"_id":bike}, {"$push":{"ridden_by":uid}})
journeys = db["journeys"]
j = journeys.stats()["count"]
journeys.insert_one({
	"_id":j,
	"start_station":near,
	"end_station":destination_station,
	"departure_time":"",
	"arrival_time":"",
	"distance":0,
	"path":[]
})
journeys.update_one({"_id":{"$eq":j}}, 
{"$currentDate":{"departure_time":{"$type":"timestamp"}}})

# Action 5: sense change in streets(perhaps using google api) and add to the journey

# journey to update received from request
# we use already recorded one for now
street = 3 #received from request
streets = db["streets"]
str = streets.find({"_id":{"$eq":street}})[0]

# queries could be merged into one
journeys.find_and_modify({
	"query":{"_id":j},
	"update":{"$push":{"path":street}}
	"upsert":True,
})
journeys.find_and_modify({
	"query":{"_id":j},
	"update":{"$inc":{"distance":str["length"]}}
})

print(str) #send street info to user

# Action 6: Upon reaching destination station area, signal backend to check for available spots
st = stations.find({"_id":{"$eq":destination_station}})
slots = db["slots"]
free=None  
for sl in st[0]["slots"]:
	sll = slots.find({"_id":{"$eq":sl}})[0]
	if(sll["status"]=="available"):
		free=sl

print(free) #send to user

# Action 7: put bike at the available slot
slots.update_one({"_id":{"$eq":free}},{"$set":{"status":"taken"}})
stats.update_one({"$inc":{"journeys":1}})
# Action 8: pay and complete journey
journeys.find_and_modify({
	"query":{"_id":j},
	"update":{"$currentDate":{"arrival_time":{"$type":"timestamp"}}}
})

shares.update_one({"_id":{"$eq":s}},{"$set":{"journey":j}})

bikes.update_one({"_id":{"$eq":bike}},{"$push":{"journeys":j}})

# payment process has been skipped
# user's location also constantly gets updates
#End of Final Project
