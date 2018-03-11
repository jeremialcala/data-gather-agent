# -*- coding: utf-8 -*-
from utils import get_mongodb


def get_pools():
	db = get_mongodb()
	cursor = db.pools.find()
	pools = []
	for pool in cursor:
		if type(pool) is dict:
			pool['_id'] = str(pool['_id'])
			pools.append(pool)
	return pools


def add_user_worker(user_id, wallet_addres, pool_id, w_type="worker", sym="eth"):
	result = {"rc": 200, "MSG": "User information saved!"}
	try:
		db = get_mongodb()
		db.user_pools.insert_one({"user_id": user_id, "pool_id": pool_id})
		db.wallets.insert_one({"user_id": user_id, "address": wallet_addres, "type": w_type, "sym": sym})
		
	except Exception as e:
		result['rc'] = 500
		result['MSG'] = str(e.args)
	
	return result
