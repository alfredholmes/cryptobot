import requests, json, calendar, time

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

			self.alg_data[int(i['algo'])] = { 'name': i['name'], 'prefix': prefix[i['speed_text']], 'decrease_amount': float(i['down_step'])}
		self.orders = {}
		self.getOrders(True)


	def cost(self, alg):
		r = json.loads(requests.get('https://www.nicehash.com/api?method=orders.get&location=0&algo=' + str(alg)).text)['result']
		lowest = -1

		for i in r['orders']:
			if (lowest > float(i['price']) or lowest < 0) and int(i['type']) == 0 and int(i['workers']) > 0:
				lowest = float(i['price'])

		return lowest / self.alg_data[alg]['prefix']


	def getOrders(self, refresh):

		if refresh == True:
			for i in range(0, 25):
				o = json.loads(requests.get('https://www.nicehash.com/api?method=orders.get&my&id=' + self.api_id + '&key=' + self.api_key + '&location=0&algo=' + str(i)).text)['result']['orders']
				for x in o:
					if x['id'] in self.orders:
						
						self.orders[int(x['id'])] = {'price': x['price'], 'btc_remaining': x['btc_avail'], 'btc_spent': x['btc_paid'] , 'last_decrease': self.orders[int(x['id'])]['last_decrease'], 'alg': str(i), 'speed': x['accepted_speed']}
					else:
						self.orders[int(x['id'])] = {'price': x['price'], 'btc_remaining': x['btc_avail'], 'btc_spent': x['btc_paid'] , 'last_decrease': 0, 'alg': str(i), 'speed': x['accepted_speed']}
		return self.orders

	def getDecreaseAmount(self, alg):
		return abs(float(self.alg_data[alg]['decrease_amount'])) / self.alg_data[alg]['prefix']

	def decreaseOrder(self, oid):
		if self.orders[oid]['last_decrease'] + (10 * 60) < calendar.timegm(time.gmtime()): 
			r = json.loads(requests.get('https://www.nicehash.com/api?method=orders.set.price.decrease&id=' + self.api_id + '&key=' + self.api_key +'&location=0&algo=' + self.orders[oid]['alg'] + '&order=' + str(oid)).text)['result']
			if 'success' in r:
				self.orders[oid]['last_decrease'] = calendar.timegm(time.gmtime())
			return 'success' in r
		else:
			return false

	def increaseOrder(self, oid, price):
		r = json.loads(requests.get('https://www.nicehash.com/api?method=orders.set.price&id=' + self.api_id + '&key=' + self.api_key + '&algo=' + self.orders[oid] + '&location=0&order=' + str(oid) + '&price=' +str(price)).text)

	def createOrder(self, algo, currency, price, btcamount, speed):
		pool = self.pools[algo][currency]
		r = json.loads(requests.get('https://www.nicehash.com/api?method=orders.create&id=' + self.api_id +'&key=' + self.api_key + '&location=0&algo=' + str(algo) + '&amount=' + str(btcamount) + '&price=' + str(price) + '&limit=' + str(speed) + '&pool_host=' + pool['host'] + '&pool_port=' + pool['port'] + '&pool_user=' + pool['user'] + '&pool_pass=' + pool['pass']).text)['result']
		print(r)
		print(price)
		return 'success' in r

	def getAccountBalance(self):
		r = json.loads(requests.get('https://www.nicehash.com/api?method=balance&id=' + self.api_id + '&key=' + self.api_key).text)['result']['balance_confirmed']
		return float(r)

	def getAmountInOrders(self):
		total = 0.0
		for order in self.orders:
			total = total + float(order['btc_remaining'])
 