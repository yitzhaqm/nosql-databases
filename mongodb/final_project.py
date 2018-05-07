# Put the use case you chose here. Then justify your database choice:
#
#                                  BIKE-APP
#
# # # I chose MongoDB for efficient data fetching and GeoSpatial Indexing capabilities. Mainly the
#     latter since GeoSpatial Indexing  is hard to efficiently implement on other database types.

# Explain what will happen if coffee is spilled on one of the servers in your cluster, causing it to go down.
# # # In a Mongo Database, since the master server has copies, if coffee is ever spilled on one of
#     the servers, one of the identical copies of the server will take the now-down server's place# and do its job without the outside clients seeing any interruption.
#
# What data is it not ok to lose in your app? What can you do in your commands to mitigate the risk of lost data?
# # # Most of the data is important, but data like user profile for logging in, passwords, names,
#     credit card information and as such require special attention as their loss could have unwan# ted consequences with the client. To mitigate the risk, I would increase atomization of data# storing and fetching in order to make sure the maximum amount of fetches and sets are
#     successful and data loss is averted. I can also alternatively handle loss of data by
#     repeated string with verification. Perhaps a simple handshake protocol to make sure gets and# sets have happened without any losses.
################################################################################

from pymongo import MongoClient
import pymongo
mongo = MongoClient()
mongo.drop_database("bike-app") # You can comment this out for more testing
db = mongo["bike-app"]

################################################################################
#Data Load Starts Here

userc = db["users"]
bikec = db["bikes"]
sharec = db["shares"]
stationc = db["stations"]
slotc = db["slots"]
statc = db["stats"]
journeyc = db["journeys"] # this could be embedded, but is referenced for
			  # the sake of stats
streetc = db["streets"]

stats = {
            "_id":0,
            "users":3,
            "bikes":5,
            "shares":4,
            "stations":4,
            "slots":7,
            "journeys":4,
            "streets":9
	}
statc.insert_one(stats)

users = [
{
"_id": 0,
"name":  "Bekele Shemsu",
"picture_url": "http://storage.bucket.stuff/",
"age": 19,
"shares": [0],
"location":{"type":"Point", "coordinates":[23.8, 34.7]},
"journeys": [2],
"stations": [0,1],
"credit_card": "xxxxxxxxxxxxxxxx"
},{
"_id": 1,
"name":  "Eyobel Nabelew",
"picture_url": "http://storage.bucket.stuff/",
"age": 25,
"shares": [1,2],
"location":{"type": "Point", "coordinates":[23.9, 35]},
"journeys": [0,3],
"stations": [2,3],
"credit_card": "xxxxxxxxxxxxxxxx"
},{
"_id": 2,
"name":  "Sebe'atu Lemlem",
"picture_url": "http://storage.bucket.stuff/",
"age": 39,
"shares": [3],
"location":{"type":"Point", "coordinates":[24, 35.2]},
"journeys": [1],
"stations": [1,3],
"credit_card": "xxxxxxxxxxxxxxxx"
}]


userc.insert_many(users)

bikes=[
{
"_id": 0,
"l_plate": 123450,
"age": 3,
"journeys":[1],
"ridden_by":[3],
"slots":[3],
},{
"_id": 1,
"l_plate": 123451,
"age": 2,
"journeys":[0],
"ridden_by":[2],
"slots":[4,7],
},{
"_id": 2,
"l_plate": 123452,
"age": 2,
"journeys":[2],
"ridden_by":[0],
"slots":[1,6],
},{
"_id": 3,
"l_plate": 123453,
"age": 2,
"journeys":[3],
"ridden_by":[2],
"slots":[2,8],
},{
"_id": 4,
"l_plate": 123454,
"age": 1,
"journeys":[],
"ridden_by":[],
"slots":[0,5],
}]

bikec.insert_many(bikes)

shares = [
{
"_id": 0,
"sharer":3,
"bike":3,
"journey": 3,
},{
"_id": 1,
"sharer": 0,
"bike": 2,
"journey": 2,
},{
"_id": 2,
"sharer":2,
"bike": 1,
"journey": 0,
},{
"_id": 3,
"sharer": 3,
"bike": 0,
"journey": 1,
}]

sharec.insert_many(shares)

stations = [
{
"_id": 0,
"location":{"type":"Point", "coordinates": [23, 34]},
"slots": [0,1],
"users": [0],
},{
"_id": 1,
"location":{"type":"Point", "coordinates": [25, 34]},
"slots": [2],
"users": [0,2],
},{
"_id": 2,
"location":{"type":"Point", "coordinates": [23, 36]},
"slots": [3,6],
"users": [1],
},{
"_id": 3,
"location":{"type":"Point", "coordinates": [25, 36]},
"slots": [4,5],
"users": [1,2],
}]

stationc.insert_many(stations)

slots = [
{
"_id": 0,
"station":0,
"status": "free",
},{
"_id": 1,
"station":0,
"status": "free",
},{
"_id": 2,
"station":1,
"status": "free",
},{
"_id": 3,
"station":2,
"status": "free",
},{
"_id": 4,
"station":3,
"status": "free",
},{
"_id": 5,
"station":3,
"status": "free",
},{
"_id": 6,
"station":2,
"status": "free",
}]

slotc.insert_many(slots)

journeys = [
{
"_id": 0,
"start_station":1,
"end_station": 3,
"departure_time": "",
"arrival_time": "",
"distance": 300,
"path": [3,7,8]
},{
"_id": 1,
"start_station":0,
"end_station": 3,
"departure_time": "",
"arrival_time": "",
"distance": 350,
"path": [4,5,6]
},{
"_id": 2,
"start_station":1,
"end_station": 4,
"departure_time": "",
"arrival_time": "",
"distance": 437,
"path": [1,2,3]
},{
"_id": 3,
"start_station":3,
"end_station": 0,
"departure_time": "",
"arrival_time": "",
"distance": 561,
"path": [0,1,2]
}]

journeyc.insert_many(journeys)

# streets haven't been well thought our for a real life application
# with regards to coordinates, length and names

streets = [
{
"_id": 0,
"start_coordinates": [24, 34.8],
"end_coordinates": [24.2, 34.8],
"street_name":"Damtew Street"
},{
"_id": 1,
"start_coordinates": [24.2, 34.8],
"end_coordinates": [24.2, 35],
"street_name":"Duniyana Street"
},{
"_id": 2,
"start_coordinates": [24.2, 35],
"end_coordinates": [24.4, 35],
"street_name":"Chala Street"
},{
"_id": 3,
"start_coordinates": [24.4, 35],
"end_coordinates": [24.4, 35.2],
"street_name":"Tsibuk Street"
},{
"_id": 4,
"start_coordinates": [24.4, 35.2],
"end_coordinates": [24.6, 35.2],
"street_name":"Nevir Mento Street"
},{
"_id": 5,
"start_coordinates": [24, 34.8],
"end_coordinates": [24, 35],
"street_name":"Some other Street"
},{
"_id": 6,
"start_coordinates": [23, 34.3],
"end_coordinates": [23, 34.5],
"street_name":"Chala Chube Street"
},{
"_id": 7,
"start_coordinates": [23.3, 34.7],
"end_coordinates": [23.5, 34.7],
"street_name":"C.H. Street"
},{
"_id": 8,
"start_coordinates": [23.5, 34],
"end_coordinates": [23.5, 34.2],
"street_name":"Chala Chube II Street"
}]

streetc.insert_many(streets)

# running the above script should dump the above data and collections into a database called "bike-app"
# End of data loading
################################################################################

################################################################################
#Actions Start Here


# Note: when I print, it generally means I am sending the info to the user.

# Note: the following series of actions isn't an exhaustive depiction of an actual
# user story. There are definitely some skipped actions.

# (Python 2.7)



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
        {"_id":0},
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
users.update({"_id":uid}, {"$push":{"stations":destination_station["_id"]}})
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
strd = streets.find({"_id":{"$eq":street}})[0]

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

print("Your are currently on "+strd["street_name"].encode("ascii", "ignore")+".") # send street info to user


# Action 6: Upon reaching destination station area, signal backend to check for available spots to put the bike
st = stations.find({"_id":{"$eq":destination_station["_id"]}})
slots = db["slots"]
free=-1
for sl in st[0]["slots"]:
	sll = slots.find({"_id":{"$eq":sl}})[0]
	if(sll["status"]=="free"):
		print("Slot "+str(sl)+" is free.")
		free=sl
		break
if(not free is None):
	print("\nPut your bike on slot "+str(free)+".") #send to user

# Action 7: put bike at the available slot
print("\nRegistering your bike return...")
slots.update_one({"_id":free},{"$set":{"status":"taken"}})
stats.update_one({"_id":0},{"$inc":{"journeys":1}})


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
