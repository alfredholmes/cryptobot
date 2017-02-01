import miners, exchange, currency, pools, collections, time


def getProfitRatio(currency, miner):
	speed = ((miner.cost(currency.alg) + miner.getDecreaseAmount(currency.alg)) * 1.03)**(-1)
	return currency.miningcalculator(speed, 24*60*60) * exchange.getBTCRate(currency.name)

def getProfitRatioP(price, currency, miner):
	speed = (price * 1.03)**(-1)
	return currency.miningcalculator(speed, 24*60*60) * exchange.getBTCRate(currency.name)


#to do make main function smaller functions


def main():
	#try:
	#initialise nicehash connection
	

	minimumProfitRatio = 1.2

	#target number of orders
	n_orders = 5
	refresh_time = 30

	#currency objects to mine
	currencies = [currency.Zec(), currency.Eth(), currency.Etc(), currency.Xmr()]

	while True:
		try:
			nh = miners.Nicehash('xxx', 'xxx', pools.pools)
			balance = nh.getAccountBalance()
			orders = nh.getOrders(False)
			if len(orders) > 0:
				print('Current Orders:')
			
			for i in orders.items():
				print('Order id: ' + str(i[0]))
				print(i[1])
			


			#to do currency matching in profit equations
			for i in orders.items():
				
				alg = int(i[1]['alg'])
				prefix = float(nh.alg_data[alg]['prefix'])
				price = float(i[1]['price'])
				nhPrice = nh.cost(alg) * prefix
				decrease = nh.getDecreaseAmount(alg) * prefix

				pool = i[1]['pool']

				c = ''

				for x in pools.pools[alg].items():
					if x[1]['host'] == pool:
						c = x[0]
				for x in currencies:
					if x.name == c:
						c = x

				if price < nhPrice and getProfitRatioP((nhPrice + decrease) / prefix, c, nh) > minimumProfitRatio:
					print('Increasing order ' + str(i[0]))
					nh.increaseOrder(i[0], nhPrice + decrease)
				
				if price > nhPrice + decrease * 1:
					print('Decreasing order ' + str(i[0]))
					nh.decreaseOrder(i[0])

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
				if balance >= 0.01:
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
		except:
			pass
	



if __name__=='__main__':
	main()