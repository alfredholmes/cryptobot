import json, requests, exchange

class Currency:
	def __init__(self, difficulty, block_reward, name, alg):
		self.difficulty = difficulty
		self.block_reward = block_reward
		self.name = name
		self.alg

	def miningCalculator(self, speed, time):
		return (speed / self.difficulty) * time * self.block_reward

	def btcRate(self):
		return exchange.getBTCRate(self.name)

	def currencyFromStr(str):
		if(str == 'eth'):
			return Eth()
		if(str == 'etc'):
			return Etc()
		if(str == 'zec'):
			return Zec()
		if(str == 'zcl'):
			return Zec()
		if(str == 'dash'):
			return Dash()
		if(str == 'xmr'):
			return Xmr()



class Eth(Currency):
	def __init__(self):
		self.difficulty = json.loads(requests.get('https://etherchain.org/api/difficulty').text)['data'][0]['difficulty']
		self.block_reward = 5
		self.name = 'eth'
		self.alg = 20

class Etc(Currency):
	def __init__(self):
		self.network_rate = float(json.loads(requests.get('https://etcchain.com/api/v1/getIndex').text)['etc']['hash_rate']) *10**9
		self.blocktime = 14
		self.block_reward = 5
		self.name = 'etc'
		self.alg = 20

	def miningCalculator(self, speed, time):
		return (speed / self.network_rate) * self.block_reward * time / self.blocktime	


class Zec(Currency):
	def __init__(self):
		r = json.loads(requests.get('https://api.zcha.in/v1/mainnet/network').text)
		self.network_rate = r['hashrate'] 
		self.blocktime = r['meanBlockTime']
		self.block_reward = 10
		self.name = 'zec'
		self.alg = 24
	
	def miningCalculator(self, speed, time):
		return (speed / self.network_rate) * self.block_reward * time / self.blocktime

class Zcl(Currency):
	def __init__(self):
		r = json.loads(requests.get('https://classic.api.zcha.in/v1/mainnet/network').text)
		self.network_rate = r['hashrate'] 
		self.blocktime = r['meanBlockTime']
		self.block_reward = 12
		self.name = 'zcl'
		self.alg = 24

	def miningCalculator(self, speed, time):
		return (speed / self.network_rate) * self.block_reward * time / self.blocktime




class Xmr(Currency):
	def __init__(self):
		self.difficulty = float(json.loads(requests.get('http://moneroblocks.info/api/get_stats/').text)['difficulty'])
		#self.difficulty = 10**15
		self.block_reward = 8.82
		self.name = 'xmr'
		self.alg = 22

	