# -*- coding: utf-8 -*-
from utils import log, get_mongodb, get_ticker
from datetime import datetime
import time


ME = "DGA"
if __name__ == '__main__':
	log("Hello World", ME)
	db = get_mongodb()
	if type(db) is not None:
		log("We Have DB", ME)
		db_collections = db.collection_names(False)
		now = datetime.now()
		resp = get_ticker()
		if resp.status_code == 200:
			for sym in resp.response:
				resp.response[sym]['dttimestamp'] = now
				log(sym + " percentChange: " + str(resp.response[sym]['percentChange']), ME)
				if sym not in db_collections:
					log("Creating Collection " + sym, ME)
					db.create_collection(sym)
				log("Saved data for " + sym + " " + str(db[sym].insert(resp.response[sym])), ME)
			log("Prices submitted", ME)
		time.sleep(3)
	else:
		log("something is up", ME)
