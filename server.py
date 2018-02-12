# -*- coding: utf-8 -*-
import os
from os import environ
from flask import Flask, render_template, request, session, make_response, Response, json
from utils import log, get_session_id
from model.currencies import get_price_range
from datetime import datetime, timedelta

session_opts = {
	'session.type': 'ext:memcached',
	'session.url': '127.0.0.1:11211',
	'session.data_dir': './cache',
}

app = Flask(__name__)
app.secret_key = environ.get('APPKEY')
SESSION_TYPE = 'redis'
app.config.from_object(__name__)


@app.route('/', methods=['GET'])
def verify():
	if 'X-Session' not in request.headers:
		session['X-Session'] = get_session_id()
	session['User-agent'] = request.headers['User-Agent']
	log(str(session), "SERVER")
	resp = make_response(render_template("index.html"))
	resp.headers["X-Session"]= session['X-Session']
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
	price_range = get_price_range(datetime.utcnow()-timedelta(hours=2), 'USDT_BTC')
	price_data = []
	price_label = []
	for price in price_range:
		price_data.append(price['last'])
		price_label.append(price['dttimestamp'].strftime("%m-%d %H:%M:%S"))
	
	data['data'] = {"labels": price_label, 'dataset': price_data}
	
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
