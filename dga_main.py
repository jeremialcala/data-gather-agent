# -*- coding: utf-8 -*-
import json
from datetime import datetime

from pymongo.errors import DuplicateKeyError

from utils import log, get_mongodb, get_ticker
import requests
ME = "DGA"


def get(url):
    try:
        get_result = requests.get(url)
    except requests.ConnectTimeout as e:
        log(str(e.message), "ERROR")
        get_result = "error"
        pass
    except requests.ConnectionError as e:
        print(str(e.message), "ERROR")
        get_result = "error"
        pass
    return get_result


def my_data(my_row):
    info = []
    for my_cell in my_row.split("</td>"):
        for data in my_cell.split(">"):
            if "<" not in data and ";" not in data and '\n' not in data:
                if "(" in data:
                    data = datetime.strptime(data.split("(")[0], "%y-%m-%d, %H:%M:%S ")
                info.append(data)
    return info


def update_workers_info():
	from bson import ObjectId
	users_wpools = db.user_pools.find()
	for pool in users_wpools:
		log(pool)
		pool_info = db.pools.find_one({"_id": ObjectId(pool['pool_id'])})
		if type(pool_info) is dict:
			email = db.users_email.find_one({"user_id": pool['user_id']})
			wallet_info = db.wallets.find({"user_id": pool["user_id"]})
			for wallet in wallet_info:
				if type(wallet) is dict:
					log("Query some workers: ")
					a_url = pool_info['url'] + pool_info['api_path']
					a_url = a_url.replace("$sym$", wallet['sym'])
					a_url = a_url.replace("$wallet_address$", wallet['address'])
					a_url = a_url.replace("$user_email$", email['address'])
					log(a_url)
					w_status = json.loads(get(a_url).text)
					# log(w_status.text)
					if w_status is not "error":
						for worker in w_status['workers']:
							w_status['workers'][worker]['address'] = wallet['address']
							w_status['workers'][worker]['dttimestamp'] = datetime.utcnow()
							db.worker_status.insert_one(w_status['workers'][worker])
						w_status.pop('workers')
						w_status['address'] = wallet['address']
						w_status['dttimestamp'] = datetime.utcnow()
						log("Wallet Stauts inserted " + str(db.wallet_status.insert_one(w_status)))
					
					w_url = pool_info['url'] + pool_info['w_path']
					w_url = w_url.replace("$sym$", wallet['sym'])
					w_url = w_url.replace("$wallet_address$", wallet['address'])
					log(w_url)
					content = get(w_url)
					if content is not "error":
						tables = content.text.split("Shares for last 24 hours")
						tables = tables[1].split("<tbody>")
						table = tables[1].split("</tbody>")
						for row in table[0].split("<tr>"):
							proc = my_data(row)
							if len(proc) > 0:
								if '*' not in proc[3]:
									data = {"address": wallet['address'], "date": proc[0], "submits": proc[1],
									        "%round": proc[2], "amount": proc[3]}
									try:
										log(db.wallet_production.insert_one(data))
									except DuplicateKeyError:
										pass


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
				# log(sym + " percentChange: " + str(resp.response[sym]['percentChange']), ME)
				if sym not in db_collections:
					log("Creating Collection " + sym, ME)
					db.create_collection(sym)
				result = db[sym].insert(resp.response[sym])
				# log("Saved data for " + sym + " " + str(db[sym].insert(resp.response[sym])), ME)
			log("Prices submitted", ME)
			
		log("_______________Saving Production Data_______________", ME)
		update_workers_info()
		# time.sleep(3)
	else:
		log("something is up", ME)
