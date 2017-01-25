import miners, exchange, currency


def getProfitRatio(currency):
	a = miners.Nicehash('0', '0', 0)
	speed = a.cost(currency.alg)**(-1)
	return currency.miningcalculator(speed, 24*60*60) * exchange.getBTCRate(currency.name)


def main():
	currencies = [ currency.Zec(), currency.Eth(), currency.Etc(), currency.Dash(), currency.Xmr()]

	for i in currencies:
		print(i.name + ": " + str(getProfitRatio(i)))

	



if __name__=='__main__':
	main()