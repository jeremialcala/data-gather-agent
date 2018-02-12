# -*- coding: utf-8 -*-
from utils import log, get_mongodb
from datetime import datetime, timedelta


def get_price_range(start=datetime.utcnow(), finish=datetime.utcnow()-timedelta(days=1), symbol='USDT_BTC'):
	# {"dttimestamp":{$gte: ISODate("2018-02-10T00:00:00.000Z"), $lt: ISODate("2018-02-11T15:59:59.000Z")}}
	# {"dttimestamp": {"$gte": start, "$lt": finish}}
	db = get_mongodb()
	price_range = db.get_collection(symbol).find({"dttimestamp": {"$gte": start}})
	log("Records found:" + str(price_range.count()), "CURRENCY")
	return price_range
