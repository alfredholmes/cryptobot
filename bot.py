import miners, exchange, currency, pools, collections, time


def getProfitRatio(currency, miner):
	speed = ((miner.cost(currency.alg) + miner.getDecreaseAmount(currency.alg)) * 1.03)**(-1)
	return currency.miningcalculator(speed, 24*60*60) * exchange.getBTCRate(currency.name)

def getProfitRatioP(price, currency, miner):
	speed = (price * 1.03)**(-1)
	return currency.miningcalculator(speed, 24*60*60) * exchange.getBTCRate(currency.name)

def sort(data):
	pivot = len(data) / 2


def main():
	#try:
	#initialise nicehash connection
	nh = miners.Nicehash('xxx', 'xxx', pools.pools)
	#nh = miners.Nicehash('xxx', 'xxx', pools.pools)
	balance = nh.getAccountBalance()
	minimumProfitRatio = 1.2

	#target number of orders
	n_orders = 5
	refresh_time = 30

	#currency objects to mine
	currencies = [currency.Zec(), currency.Eth(), currency.Etc(), currency.Xmr()]

	while True:
		
		orders = nh.getOrders(True)
		if len(orders) > 0:
			print('Current Orders:')
		
		for i in orders.items():
			print('Order id: ' + str(i[0]))
			print(i[1])
		


		#to do currency matching in profit equations
		for i in orders.items():
			#print(i)
			if float(i[1]['price']) > nh.cost(int(i[1]['alg'])) * nh.alg_data[int(i[1]['alg'])]['prefix'] + nh.getDecreaseAmount(int(i[1]['alg'])) * nh.alg_data[int(i[1]['alg'])]['prefix']:
				nh.decreaseOrder(i[0])
				print('Decreasing order: ' + str(i[0]) + ' by ' + str(nh.alg_data[int(i[1]['alg'])]['decrease_amount']))
			if float(i[1]['price']) < nh.cost(int(i[1]['alg'])):
				if getProfitRatioP(nh.cost(int(i[1]['alg'])) + nh.getDecreaseAmount(int(i[1]['alg'])), list(pools[int(i[1]['alg'])])[0], nh) > minimumProfitRatio:
					nh.increaseOrder(self, x, nh.cost((int(i[1]['alg'])) + nh.getDecreaseAmount(int(i[1]['alg']))) * nh.alg_data[int(i[1]['alg'])]['prefix'])
					print('Increasing order' + str(i[0]) + ' to ' + str(nh.cost(int(i[1]['alg'])) / nh.alg_data[int(i[1]['alg'])]['prefix'] + nh.alg_data[int(i[1]['alg'])]['decrease_amount']))
			#check if order still profitable

		#get prices for the algrithms
		initialprofits = {}
		prices = []

		for i in currencies:
			prices.append(round(getProfitRatio(i, nh), 5))
			initialprofits[round(getProfitRatio(i, nh), 5)] = i
		
		#create an orderedDict of rate: currency with the best rate at the start 
		prices.sort(reverse=True)
		profits = collections.OrderedDict()
		
		print(prices)

		for rate in prices:
			if rate > minimumProfitRatio:
				profits[rate] = initialprofits[rate]

		#print(profits)
	
			

		for i in profits.items():
			if balance >= 0.0:
				openOrder = False
				for o in orders.items():
					if int(o[1]['alg']) == int(i[1].alg):
						openOrder = True
				if openOrder == False:
					orderTotal = 0
					if balance / n_orders > 0.01:
						orderTotal = balance / n_orders
					else:
						orderTotal = 0.01
					speed = (orderTotal * (2 * i[0]) / nh.cost(i[1].alg)) / nh.alg_data[i[1].alg]['prefix']
					price = round((nh.cost(i[1].alg) + nh.getDecreaseAmount(i[1].alg)) * nh.alg_data[i[1].alg]['prefix'], 4)
					#print(price)
					if nh.createOrder(int(i[1].alg), i[1].name, price, orderTotal, speed):
						print('creating order for ' + i[1].name + ' with speed: ' + str(speed) + ' and value: ' + str(orderTotal))
					else:
						print('failed to create order')

		#delay for 30 seconds
		print('Waiting ' + str(refresh_time) + ' seconds...')
		time.sleep(refresh_time)
	#except:
		#pass
	



if __name__=='__main__':
	main()