# -*- coding: utf-8 -*-
import os
from os import environ
from flask import Flask, render_template, request, session, make_response, Response, abort, redirect
import json
from utils import log, get_random_key
from model.currencies import get_price_range
from datetime import datetime, timedelta
from flask_login import LoginManager, UserMixin, \
	login_required, login_user, logout_user
from controller.User import verify_user
from model.User import User, user

app = Flask(__name__)
app.secret_key = environ.get('APPKEY')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "session_adm"


@app.route('/', methods=['GET'])
@login_required
def index():
	if 'X-Session' not in request.headers:
		session['X-Session'] = get_random_key()
	# session['User-agent'] = request.headers['User-Agent']
	# log(str(request.headers['Cookie']), "SERVER")
	log(str(session), "SERVER")
	resp = make_response(render_template("index.html"))
	# resp.headers["X-Session"] = session['X-Session']
	return resp


@app.route('/session', methods=['GET', 'POST'])
def session_adm():
	if request.method == 'POST':
		username = request.form['email']
		password = request.form['password']
		log(username + " " + password, "SERVER")
		user_verification = {"email": request.form['email'], "password": request.form['password']}
		resp = verify_user(user_verification)
		
		if resp['rc'] is 200:
			user_json = json.loads(resp['user'])
			user = User(**user_json)
			login_user(user)
			resp = make_response(render_template("index.html"))
		else:
			return abort(401)
	else:
		resp = make_response(render_template("signin.html"))
	return resp


@app.route('/prices', methods=['GET'])
@login_required
def get_prices():
	# obtain 24 hs of USDT_BTC
	data = {"rc": 0, "msg": "Process OK"}
	
	price_range_btc = get_price_range(datetime.utcnow()-timedelta(hours=6), None, 'USDT_BTC')
	price_range_eth = get_price_range(datetime.utcnow()-timedelta(hours=6), None, 'USDT_ETH')
	
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


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
	logout_user()
	return render_template("signin.html")


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
	return user(userid)


if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
