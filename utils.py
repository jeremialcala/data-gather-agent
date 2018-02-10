# -*- coding: utf-8 -*-
import sys
import pymongo
import json
from datetime import datetime, time
from os import environ
from requests import get as _get
from flask import Response


def get_timestamp(component='CORE'):
	return datetime.fromtimestamp(time.time()).strftime('[%Y.%m.%d %H:%M:%S.%f')[:-3] + '][' + component + ']'


def log(message, component='CORE'):
	print('[' + component + '] ' + message)
	sys.stdout.flush()


def get_mongodb():
	try:
		db = None
		# log(environ.get("MONGO_HOST"))
		uri_mdb_dev = environ.get("MONGO_HOST")
		_dev = pymongo.MongoClient(uri_mdb_dev)
		db = _dev[environ.get("SCHEMA")]
		
	except Exception as e:
		log("Error: " + str(e.args), 'utils')
	# log(str(db.list_collection_names()))
	return db


# POLONIEX SIDE OF THINGS

def get_ticker():
	resp = _get(environ.get('POLONIEX_URL') + environ.get('POLONIEX_PUBLIC') + 'returnTicker')
	return Response(json.loads(resp.text), resp.status_code, mimetype='application/json')
