# -*- coding: utf-8 -*-
import sys
import pymongo
import json
# from hashlib import blake2b
from datetime import datetime, time
from os import environ
from requests import get as _get
from flask import Response
from random import choice

AUTH_SIZE = 16
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
alpha_numeric = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def get_timestamp(component='CORE'):
	return datetime.fromtimestamp(time.time()).strftime('[%Y.%m.%d %H:%M:%S.%f')[:-3] + '][' + component + ']'


def log(message, component='CORE'):
	print('[' + component + '] ' + str(message))
	sys.stdout.flush()


def get_mongodb():
	try:
		db = None
		uri_mdb_dev = environ.get("MONGO_HOST")
		_dev = pymongo.MongoClient(uri_mdb_dev, replicaSet=environ.get("REPLICASET_MONGO"))
		db = _dev[environ.get("SCHEMA")]
	except Exception as e:
		log("Error: " + str(e.args), 'utils')
	return db


def get_random_key(size=32, only_alpha=False):
	key = ""
	for x in range(0, size):
		if only_alpha:
			key += choice(alphabet)
		else:
			key += str(choice(alpha_numeric))
	# log("key generated: " + key, "UTIL")
		
	return key


# POLONIEX SIDE OF THINGS
def get_ticker():
	resp = _get(environ.get('POLONIEX_URL') + environ.get('POLONIEX_PUBLIC') + 'returnTicker')
	return Response(json.loads(resp.text), resp.status_code, mimetype='application/json')
