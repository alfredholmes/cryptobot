import requests, json

class Miner:
	def cost(alg):
		#returns lowest cost of alg in H/s/BTC/Day
		pass

	def order(alg, cost):
		#opens a new order with alg algorithm costing cost btc
		pass

	def getOrders():
		#returns dictionary of order dictionarys
		pass

	def getOrder(alg):
		#returns order information dictionary
		pass

	def getBalance():
		#returns available btc balance
		pass


class Nicehash(Miner):
	def __init__(self, api_id, api_key, pools):
		self.api_id = api_id
		self.api_key = api_key
		self.pools = pools
		r = json.loads(requests.get('https://www.nicehash.com/api?method=buy.info').text)['result']['algorithms']
		self.alg_data = {}
		for i in r:
			prefix = {'H': 10*0, 'kH': 10**3, 'mH': 10**6, 'gH': 10**9, 'tH': 10**12, 'pH': 10**15, 'KH': 10**3, 'MH': 10**6, 'GH': 10**9, 'TH': 10**12, 'PH': 10**15, 'kSol': 10**3, 'KSol': 10**3}

			self.alg_data[int(i['algo'])] = { 'name': i['name'], 'prefix': prefix[i['speed_text']]}



	def cost(self, alg):
		r = json.loads(requests.get('https://www.nicehash.com/api?method=orders.get&location=0&algo=' + str(alg)).text)['result']
		lowest = -1
		for i in r['orders']:
			if (lowest > float(i['price']) or lowest < 0) and int(i['type']) == 0 and int(i['workers']) > 0:
				lowest = float(i['price'])

		return lowest / self.alg_data[alg]['prefix']

	def order(self, alg, price, size, pool, speed):
		r = json.loads(requests.get('https://www.nicehash.com/api?method=orders.create&id=' + str(self.api_id) + '&key=' + str(self.api_key) + '&location=0&algo=' + str(alg) + '&amount=' + str(size) +'&price=' + str(price) + '&limit=' + str(speed) + '&pool_host=' + self.pools[pool]['host'] + '&pool_port=' + str(self.pools[pool]['port']) + '&pool_user=' + self.pools[pool]['user'] + '&pool_pass=' + self.pools[pool]['password']).text)
		print(r)

	def getOrders():
		pass
 