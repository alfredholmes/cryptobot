import requests, json


def getBTCRate(currency):
	result = json.loads(requests.get("http://shapeshift.io/marketinfo/" + str(currency) + "_btc").text)
	return result['rate']