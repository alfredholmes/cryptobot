import requests, json


def getBTCRate(currency):
	
	r = 0
	try:
		result = json.loads(requests.get("http://shapeshift.io/marketinfo/" + str(currency) + "_btc").text)
		r = result['rate']		
	except:
		r = 0
	return r