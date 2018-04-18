from pymongo import MongoClient
import pprint #for pretty printing

mongo = MongoClient()
#below are a combination of
#precreated database, homework-3, 
#and collection, mongo-collection
db = mongo["homework-3"]

mcollect = db["mongo-collection"]

#A
mcollect.update_many({"rated":"NOT RATED"},{"$set":{"rated":"Pending rating"}})

#B
movie = {
	"title":"Thor: Ragnarok (2017)",
	"year":2017,
	"countries":["USA"],
	"genres":["Comedy", "Sci-Fi", "Adventure", "Action", "Fantasy"],
	"directors":["Taika Waititi"],
	"imdb":{
		"id":13,
		"rating":7.9,
		"votes":298656
	}
}
if(mcollect.find_one({"title":"Thor: Ragnarok (2017)"}) == None):
	print("\nInserted Thor: Ragnarok with ID: "+mcollect.insert_one(movie).inserted_id+"\n")

#C
result = mcollect.aggregate([
			{"$match":{"genres":{"$in":["Comedy"]}}},
			{"$group":{"_id":"Comedy","count":{"$sum":1}}}
		])
print("\nCounting for movies in my genre, Comedy, from the given data set:\n")
for doc in result:
	pprint.pprint(doc)

#D
result2 = mcollect.aggregate([
		{"$match":{"$and":[{"countries":{"$in":["Ethiopia"]}},{"rated":"Pending rating"}]}},
		{"$group":{"_id":{"country":"Ethiopia","rated":"$rated"},"count":{"$sum":1}}}
	])

print("\nCounting for movies set in my country of birth and growth, Ethiopia:\n")
for doc in result2:
	pprint.pprint(doc)

#E

#Note: data below is extremely subjective
ndata=[{"name": "Java",
	"famous_for":"Android",
	"awesomeness_r": 95.3},

	{"name": "Python",
	"famous_for":"Data stuff",
	"awesomeness": 98.7},

	{"name": "Javascript",
	"famous_for":"WEB",
	"awesomeness_r":94.9},

	{"name": "PhP",
	"famous_for":"Facebook",
	"awesomeness":68.13}]

odata=[{"name": "English",
	"famous_for":"Communication",
	"awesomeness":94.1},
	
	{"name": "Amharic",
	"famous_for":"Historic Presence",
	"awesomeness":95.3},
	
	{"name": "French",
	"famous_for":"Got Nothing",
	"awesomeness":94.9}]

ncollect = db["ncollect"]
ocollect = db["ocollect"]

ncollect.remove({})
ocollect.remove({})

ncollect.insert_many(ndata)
ocollect.insert_many(odata)

result3 = ncollect.aggregate([
	{
		"$lookup":
		{
			"from":"ocollect",
			"localField":"awesomeness_r",
			"foreignField":"awesomeness",
			"as":"as_awesome_as"
		}
	}
]) 

print("\nAggregate resulting after lookup:\n")
for doc in result3:
	if(doc["as_awesome_as"]!=[]):
		print("\n")
		pprint.pprint(doc)
		print("\n")

#End of homework




