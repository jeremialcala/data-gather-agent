# -*- coding: utf-8 -*-
import os
from os import environ
from flask import Flask, render_template, request, session, make_response, Response, json
from utils import log, get_random_key
from model.currencies import get_price_range
from datetime import datetime, timedelta
from flask_socketio import SocketIO, emit
from flask_login import current_user, logout_user


app = Flask(__name__)
app.secret_key = environ.get('APPKEY')
socket_io = SocketIO(app)
# session.permanent = True


@app.route('/', methods=['GET'])
def index():
	# if 'X-Session' not in request.headers:
		# session['X-Session'] = get_random_key()
	# session['User-agent'] = request.headers['User-Agent']
	
	log(str(session), "SERVER")
	resp = make_response(render_template("index.html"))
	# resp.headers["X-Session"] = session['X-Session']
	return resp


@app.route('/session', methods=['GET', 'POST'])
def session_adm():
	try:
		if request.method == 'POST':
			log(str(session), "SERVER")
		log(str(session), "SERVER")
	except Exception as e:
		log(str(e.args), "ERROR")
	
	return render_template("index.html")


@app.route('/prices', methods=['GET'])
def get_prices():
	# obtain 24 hs of USDT_BTC
	data = {"rc": 0, "msg": "Process OK"}
	
	price_range_btc = get_price_range(datetime.utcnow()-timedelta(hours=6), None, 'USDT_BTC')
	price_range_eth = get_price_range(datetime.utcnow() - timedelta(hours=6), None, 'USDT_ETH')
	
	price_btc = []
	chang_btc = []
	price_eth = []
	chang_eth = []
	
	price_label = []
	for price in price_range_eth:
		price_eth.append(price['last'])
		chang_eth.append(price['percentChange'])
		# price_eth.append({"percentChange": price['percentChange'], "last": price['last']})
		price_label.append(price['dttimestamp'].strftime("%H:%M"))
		
	for price in price_range_btc:
		price_btc.append(price['last'])
		chang_btc.append(price['percentChange'])
		# price_btc.append({"percentChange": price['percentChange'], "last": price['last']})
	
	data['data'] = {"labels": price_label, 'datasets': [{"label": "Bitcoin", "data": {"price": price_btc, "change": chang_btc}},
	                                                    {"label": "Ethereum", "data": {"price": price_eth, "change": chang_eth}}]}
	
	return Response(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')),
	                200, mimetype='application/json')


@app.route('/test_json', methods=['GET'])
def get_test_endpoint():
	data = {"rc": 0, "msg": "Process OK"}
	return Response(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')),
					200, mimetype='application/json')


if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
