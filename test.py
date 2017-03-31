import miners, pools

def main():
	a = miners.NHController('83980', '8be1ac20-7d09-400b-9bd8-f6625bf517e3', pools.pools, 10*60, 1.2, 12*60*60, 3)
	a.refresh()
	print(a.getCurrencyData())

if __name__=="__main__":
	main()