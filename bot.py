import miners, exchange, currency, pools


def getProfitRatio(currency, miner):
	a = miner
	speed = (a.cost(currency.alg) * 1.03)**(-1)
	return currency.miningcalculator(speed, 24*60*60) * exchange.getBTCRate(currency.name)


def main():
	#try:
	nh = miners.Nicehash('8', '5', pools.pools)
	
	currencies = [ currency.Zec(), currency.Eth(), currency.Etc(), currency.Xmr()]

	for i in currencies:
		print(i.name + ": " + str(getProfitRatio(i, nh)))
	

	print(nh.getOrders(False))
	print(nh.getAccountBalance())
	#print(nh.createOrder(20, 'etc', 0.03, 0.01, 0.1))
#except:
		#pass
	



if __name__=='__main__':
	main()