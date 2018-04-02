import httplib
import json

def makeRequest():
	ren = httplib.HTTPSConnection(host="api.nasa.gov", port=None)
	req = ren.request(method="GET", url="/planetary/apod?date=2017-08-19&api_key=z0cVI1CIPWs4oceOoy4DlApuWtVfV5BN7d8MWEmw")
	res = ren.getresponse()
	obj = json.load(res)
	print(obj["url"])

makeRequest()
