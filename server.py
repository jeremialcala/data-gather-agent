from os import environ
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
	return render_template("index.html")


if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
    	app.run(host='0.0.0.0', port=port)
