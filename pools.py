pools = {
#	alg: {'currency': { host': 'https://www.pool.org' 'port': '666', 'user': 'x' 'pass': 'x'}}
#	reccomend first configuring on nicehash to ensure connection
	 0: {},
	 1: {},
	 2: {},
	 3: {},
	 4: {},
	 5: {},
	 6: {},
	 7: {},
	 8: {},
	 9: {},
	10: {},
	11: {},
	12: {},
	13: {},
	14: {},
	15: {},
	16: {},
	17: {},
	18: {},
	19: {},
	20: {'etc': {'host': 'etc-eu1.nanopool.org', 'port': '19999', 'user': '0xb6b5b6c08096996a180f5ff636d5ecc1fb7d3f5c', 'pass': 'x'}, 'eth': {'host': 'eth-eu1.nanopool.org', 'port': '9999', 'user': '0xe64e2c51df1959bcae28ed5c5614f14f647276ae', 'pass': 'x'}},
	21: {},
	22: {'xmr': {'host': 'xmr.suprnova.cc', 'port': '5223', 'user': 'alfredholmes.nh', 'pass': 'd=20000'}},
	23: {},
	24: {'zec': {'host': 'zec-eu.suprnova.cc', 'port': '2143', 'user': 'alfredholmes.nh', 'pass': 'd=1024'}},

}

def getCurrencyFromPool(alg, pool):
	for i in pools[alg].items():
		if i[1]['host'] == pool:
			return i[0]
	return 0
