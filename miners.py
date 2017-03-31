import requests, json, time, currency, exchange, pools

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

class Controller:
	def refresh(self):
		#refresh service data
		pass
	def updateOrders(self):
		#run logic to update orders
		pass

class NHController(Controller):
	#cri: currency refresh interval
	def __init__(self, api_id, api_key, pools, cri, target_rate, order_time, number):
		self.nh = Nicehash(api_id, api_key, pools)
		self.cri = cri
		self.orders = self.nh.orders
		#{str: {currency.Currency(): btc_rate}}
		self.currency_cache = {}
		self.last_cache = 0
		self.currency_data = self.getCurrencyData()
		self.target_rate = target_rate
		self.order_time = order_time
		self.order_number = number

	def refresh(self):
		self.nh.refreshOrderBook()
		self.orders = self.nh.getOrders(True)
		self.currency_data = self.getCurrencyData()

	def update(self):
		if self.nh.getAccountBalance() > 0.01:
			for i in self.currency_data.items():
				#get rate
				algorithm = list(i[1].keys)
				rate = list(i[1].keys)[1]
				currency = i[0]
				if rate > self.target_rate:
					openOrder = False
					for x in self.orders.items():
						if pools.getCurrencyFromPool(int(x[1]['alg']), x[1]['pool']) == currency:
							openOrder = True
					if not openOrder:
						#calculate order speed
						orderTotal = 0
						if self.nh.getAccountBalance() / self.order_number > 0.01:
							orderTotal = self.nh.getAccountBalance() / self.order_number
						else:
							orderTotal = 0.01
						
						speed = (orderTotal * (2 * i[0]) / nh.cost(i[1].alg)) / nh.alg_data[i[1]]['prefix']

	def getCurrencyData(self):
		#{currency: rate}
		
		update_cache = (self.last_cache + self.cri < int(time.time()))

		currency_data = {}
		for i in self.nh.pools.items():
			for c in list(i[1].keys()):
				if(len(i[1]) > 0):
					#currency object from pools
					
					#get btc price of currency
					btc_rate = 0
					if update_cache:
						co = currency.Currency.currencyFromStr(c)
						btc_rate = co.btcRate()
						if btc_rate > 0:
							self.currency_cache[c] = {co: btc_rate}
						else:
							btc_rate = self.currency_cache[c][co]
						self.last_cache = int(time.time())
					else:
						btc_rate = self.currency_cache[c]

					#pretend investment is 1 btc
					rate = (self.nh.cost(i[0]))**(-1) *.97
					#get currency object
					co = list(self.currency_cache[c].keys())[0]
					#currency mined in 1 day
					profit = co.miningCalculator(rate, 24*60*60) * self.currency_cache[c][co]

					currency_data[c] = profit
					
		return currency_data					






class Nicehash(Miner):
	def __init__(self, api_id, api_key, pools):
		self.api_id = api_id
		self.api_key = api_key
		self.pools = pools
		self.alg_data = {}
		self.alg_data = self.refreshOrderBook()
		self.orders = {}
		self.orders = self.getOrders(True)


	def refreshOrderBook(self):
		r = json.loads(requests.get('https://www.nicehash.com/api?method=buy.info').text)['result']['algorithms']
		data = {}
		for i in r:
			prefix = {'H': 10*0, 'kH': 10**3, 'mH': 10**6, 'gH': 10**9, 'tH': 10**12, 'pH': 10**15, 'KH': 10**3, 'MH': 10**6, 'GH': 10**9, 'TH': 10**12, 'PH': 10**15, 'kSol': 10**3, 'KSol': 10**3, 'MSol': 10**6}

			data[int(i['algo'])] = { 'name': i['name'], 'prefix': prefix[i['speed_text']], 'decrease_amount': float(i['down_step'])}
		self.alg_data = data
		return data


	def cost(self, alg):
		r = json.loads(requests.get('https://www.nicehash.com/api?method=orders.get&location=0&algo=' + str(alg)).text)['result']
		lowest = -1

		for i in r['orders']:
			if (lowest > float(i['price']) or lowest < 0) and int(i['type']) == 0 and int(i['workers']) > 0:
				lowest = float(i['price'])

		return lowest / self.alg_data[alg]['prefix']


	def getOrders(self, refresh):
		if refresh:
			orders = {}
			for i in range(0, 25):
				o = json.loads(requests.get('https://www.nicehash.com/api?method=orders.get&my&id=' + self.api_id + '&key=' + self.api_key + '&location=0&algo=' + str(i)).text)['result']['orders']
				for x in o:
					if x['id'] in self.orders:
						
						orders[int(x['id'])] = {'price': x['price'], 'btc_remaining': x['btc_avail'], 'btc_spent': x['btc_paid'] , 'last_decrease': self.orders[int(x['id'])]['last_decrease'], 'alg': str(i), 'speed': x['accepted_speed'], 'pool': x['pool_host']}
					else:
						orders[int(x['id'])] = {'price': x['price'], 'btc_remaining': x['btc_avail'], 'btc_spent': x['btc_paid'] , 'last_decrease': 0, 'alg': str(i), 'speed': x['accepted_speed'], 'pool': x['pool_host']}
			return orders
		else:
			return self.orders

	def getDecreaseAmount(self, alg):
		return abs(float(self.alg_data[alg]['decrease_amount'])) / self.alg_data[alg]['prefix']

	def decreaseOrder(self, oid):
		if self.orders[oid]['last_decrease'] + (10 * 60) < int(time.time()): 
			r = json.loads(requests.get('https://www.nicehash.com/api?method=orders.set.price.decrease&id=' + self.api_id + '&key=' + self.api_key +'&location=0&algo=' + self.orders[oid]['alg'] + '&order=' + str(oid)).text)['result']
			if 'success' in r:
				self.orders[oid]['last_decrease'] = int(time.time())
			return 'success' in r
		else:
			return False

	def increaseOrder(self, oid, price):
		r = json.loads(requests.get('https://www.nicehash.com/api?method=orders.set.price&id=' + self.api_id + '&key=' + self.api_key + '&algo=' + str(self.orders[oid]['alg']) + '&location=0&order=' + str(oid) + '&price=' +str(price)).text)

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

	def getPrefix(self, alg):
		return self.alg_data[alg]['prefix']
 

