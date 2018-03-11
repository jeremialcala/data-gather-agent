# -*- coding: utf-8 -*-
import os
from os import environ
from flask import Flask, render_template, request, session, make_response, Response, abort, redirect, g
import json
from utils import log, get_random_key
from model.currencies import get_price_range
from datetime import datetime, timedelta
from flask_login import LoginManager, UserMixin, \
    login_required, login_user, logout_user, current_user
from controller.User import verify_user
import controller
from model.User import User, user, Email

app = Flask(__name__)
app.secret_key = environ.get('APPKEY')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "session_adm"


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)
    session.modified = True
    g.user = current_user


@app.route('/', methods=['GET'])
@login_required
def index():
    log(str(session['_id']), "SERVER")
    log(str(session['user_id']), "SERVER")

    resp = make_response(render_template("index.html"))

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
            new_user = User(**user_json)
            login_user(new_user)
            # resp = make_response(render_template("index.html"))
            resp = redirect("/")
        else:
            return abort(resp['rc'])
    else:
        resp = make_response(render_template("signin.html"))
    return resp


@app.route('/verify', methods=['POST'])
def verify():
    json_req = request.get_json()
    log(json_req)
    if 'email' in json_req:
        email = Email("", json_req['email'])
        resp = email.get_user_info()
        log(resp, "SERVER")
        data = {"rc": resp.get('rc'), "MSG": resp.get('MSG')}
        return Response(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')),
                        resp.get('rc'), mimetype='application/json')
    if 'nid' in json_req:
        user = User("", json_req['nid'], "", "", "", "")
        user = user.get_user_info()
        data = {"rc": 200, "MSG": "Process OK"}
        if user.id == "":
            return Response(user.to_json(), 404, mimetype='application/json')
        else:
            return Response(user.to_json(), 200, mimetype='application/json')

    data = {"rc": 401, "msg": "Bad Request"}
    return Response(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')),
                    401, mimetype='application/json')


@app.route('/pools', methods=['GET'])
@login_required
def get_pools():
    from controller.Pools import get_pools
    data = {"rc": 401, "MGS": "Bad Request"}
    pools = get_pools()
    if len(pools) > 0:
        data['rc'] = 200
        data['MSG'] = "Process OK"
        data['pools'] = pools
    else:
        data['rc'] = 404
        data['MSG'] = "No records founds"

    return Response(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')),
                    data['rc'], mimetype='application/json')


@app.route('/pool', methods=['POST'])
@login_required
def add_worker():
    data = {"rc": 401, "MGS": "Bad Request"}
    this_user = user(str(session['user_id']))
    user_id = this_user.user_id
    wallet = request.form("wallet")
    w_type = request.form("type")
    pool_id = request.form("pool_id")

    return Response(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')),
                    data['rc'], mimetype='application/json')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    resp = make_response(render_template('signup.html'))
    if request.method == 'POST':
        user_registration = {"email": [], "password": ""}
        dob = datetime.strptime(str(request.form['dob']), '%Y-%m-%d')
        age = datetime.utcnow() - dob
        if (age.days / 365) < 18:
            log("Minor " + str(age.days / 365), "SERVER")
            resp = make_response(render_template("/signup.html"))
        else:
            full_name = request.form["full_name"].split()
            first_name = full_name[0]
            if len(full_name) > 2:
                last_name = full_name[len(full_name) - 2] + " " + full_name[len(full_name) - 1]
            else:
                last_name = full_name[len(full_name) - 1]

            log(str(request.form['full_name']), "SERVER")
            log(str(request.form['nid']), "SERVER")
            log(str(request.form['dob']), "SERVER")
            log(str(request.form['email']), "SERVER")
            log(str(request.form['password']), "SERVER")

            user_registration['password'] = request.form['password']
            user_registration['email'].append({"address": request.form['email']})
            new_user = User("", request.form['nid'], first_name, last_name, request.form['dob'], "")

            user_registration['user'] = json.loads(new_user.to_json())
            log(user_registration, 'SERVER')
            create_resp = controller.User.create_user(user_registration)
            log(create_resp, "SERVER")
            if create_resp['rc'] != 200:
                resp = make_response(render_template("/signup.html"))
            else:
                new_user.id = create_resp['_id']
                login_user(new_user)
                resp = redirect("/")

    return resp


@app.route('/prices', methods=['GET'])
def get_prices():
    # obtain 24 hs of USDT_BTC
    data = {"rc": 0, "msg": "Process OK"}
    timeframe = 12
    price_range_btc = get_price_range(datetime.utcnow() - timedelta(hours=timeframe), None, 'USDT_BTC')
    price_range_eth = get_price_range(datetime.utcnow() - timedelta(hours=timeframe), None, 'USDT_ETH')

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

    data['data'] = {"labels": price_label,
                    'datasets': [{"label": "Bitcoin", "data": {"price": price_btc, "change": chang_btc}},
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
