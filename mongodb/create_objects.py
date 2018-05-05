from pymongo import MongoClient
import pprint

mongo = MongoClient()

db = mongo["bike-app"]

userc = db["users"]
bikec = db["bikes"]
sharec = db["shares"]
stationc = db["stations"]
slotc = db["slots"]
statc = db["stats"]
journeyc = db["journeys"] # this could be embedded, but is referenced for
			  # the sake of stats
streetc = db["streets"]


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



#running this script should dump the above data and collections into a database called "bike-app"


