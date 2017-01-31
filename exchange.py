import requests, json


def getBTCRate(currency):
	result = json.loads(requests.get("http://shapeshift.io/marketinfo/" + str(currency) + "_btc").text)
	r = 0
	try:
		r = result['rate']		
	except KeyError:
		r = 0
	return r