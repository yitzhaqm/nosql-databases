# Put the use case you chose here. Then justify your database choice:
# 
#                                  BIKE APP
#
# I chose MongoDB for efficient data fetching and GeoSpatial Indexing capabilities. Mainly the
# latter since GeoSpatial Indexing  is hard to efficiently implement on other database types.
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
import pymongo
mongo = MongoClient()
db = mongo["bike-app"]

# Note: when I print, it generally means I am sending the info to the user.

# Note: the following series of actions isn't an exhaustive depiction of the actual
# user story. There are definitely some skipped actions.


# !!!IMPORTANT!!!
# Note: The following series of actions assume that mongod is running andcreate_objects.py has been run as well.
# !!!IMPORTANT!!!



# Action 1: User signs up for an account with name
users = db["users"]
name = "Abebe Bikila" #entered name

idd = users.count()
users.insert_one({
	"_id":idd,
	"name": name,
	"picture_url": "http://storage.bucket.stuff/",
	"age": 20,
	"shares": [],
	"location": {"type":"Point", "coordinates":[25, 36]},
	"journeys": [],
	"stations": [],
	"credit_card": "xxxxxxxxxxxxxxxx",
})
stats = db["stats"]
stats.update_one(
	{},
	{
		"$inc":{"users":1}
	}
)
print("Welcome to Bike-App, "+name+"!")

# Action 2: App requests data on nearby bike stations to show the user
stations = db["stations"]
uid = idd #requesting user database id
us = users.find({"_id":{"$eq":uid}})
print("\n>>>>>>>>>>>>>")
print(us[0])
print(">>>>>>>>>>>>>")

stations.create_index([("location", pymongo.GEOSPHERE)])
near = stations.find(
	{
		"location":
			{
				"$near":
				{
				"$geometry":us[0]["location"],
				"$minDistance":0,
				"$maxDistance":10000
				}
			}
	}
)
print("\nHere are a few suggestions on stations: ")
print(">>>>>>>>>>>>>")
for some in near:
	print(some)
print(">>>>>>>>>>>>>>")
# Action 3: User picks the nearest station from the provided list and we send the user more information about the station
picked = 3 # picked station id normally gotten from the request

found = stations.find({"_id": {"$eq":picked}})[0]
print("\nGo to station "+str(found["_id"])+" and get your preferred bike!") # should be a single one for current purposes

# Action 4: The user now picks a bike, destination and the app send the nearest station to the biker's destination
bike = 0 # as provided by the user
print("\nYou have chosen bike "+str(bike)+".")
destination = {"type":"Point", "coordinates":[25,36]} # as provided by the user
destination_station = stations.find({
	"location":
	{
		"$near":
		{
		"$geometry":destination,
		"$minDistance":0,
		"$maxDistance":3610
		}
	}	
})[0]
print("\nYour destination station is station "+str(destination_station["_id"])+".")

users.update({"_id":{"$eq":uid}},
		     {"$push":{"bikes":bike}})
shares = db["shares"]
s = shares.count()
shares.insert_one({
	"_id":s,
	"sharer":uid,
	"bike":bike,
	"journey": -1
})
users.update(
	{"_id":uid},
	{"$push":{"shares":s}}
)
bikes = db["bikes"]
bikes.update_one({"_id":bike}, {"$push":{"ridden_by":uid}})
journeys = db["journeys"]
j = journeys.count()
journeys.insert_one({
	"_id":j,
	"start_station":found,
	"end_station":destination_station["_id"],
	"departure_time":"",
	"arrival_time":"",
	"distance":0,
	"path":[]
})
journeys.update_one({"_id":{"$eq":j}}, 
{"$currentDate":{"departure_time":{"$type":"timestamp"}}})
print("\nJourney officially started! Have a safe trip!")
# Action 5: sense change in streets(perhaps using google api) and add to the journey

# journey to update received from request
# we use already recorded one for now
street = 3 #received from request
streets = db["streets"]
str = streets.find({"_id":{"$eq":street}})[0]

# queries could be merged into one
journeys.update(
	{"_id":j},
	{"$push":{"path":street}},
	upsert=True
)

#journeys.update({
#	{"_id":j},
#	{"$inc":{"distance":str["length"]}}
#})

print("Your are currently on "+str["street_name"].encode("ascii", "ignore")+".") # send street info to user


# Action 6: Upon reaching destination station area, signal backend to check for available spots to put the bike
st = stations.find({"_id":{"$eq":destination_station["_id"]}})
slots = db["slots"]
free=None  
for sl in st[0]["slots"]:
	sll = slots.find({"_id":{"$eq":sl}})[0]
	if(sll["status"]=="free"):
		print("Slot "+str(sl)+" is free.")
		free=sl
		break
if(free!=None):
	print("\nPut your bike on slot "+str(free)+".") #send to user

# Action 7: put bike at the available slot
print("\nRegistering your bike return...")
slots.update_one({"_id":free},{"$set":{"status":"taken"}})
stats.update_one({},{"$inc":{"journeys":1}})


# Action 8: pay and complete journey
print("\nCompleting Journey and payments...")
journeys.update(
	{"_id":j},
	{"$currentDate":{"arrival_time":{"$type":"timestamp"}}}
)

shares.update_one({"_id":{"$eq":s}},{"$set":{"journey":j}})

bikes.update_one({"_id":{"$eq":bike}},{"$addToSet":{"journeys":j}})
users.update_one({"_id":{"$eq":uid}}, {"$addToSet":{"journeys":j}})
print("\nThanks for using Bike-App!")
print("\n======================Journey Complete======================")
print("\nYour profile now: ")
now = users.find({"_id":{"$eq":uid}})[0]
print(">>>>>>>>>>>>>")
print(now)
print(">>>>>>>>>>>>>")
# payment process has been skipped
# user's location also constantly gets updates


# End of Final Project
