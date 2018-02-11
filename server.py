from os import environ
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
	return render_template("index.html")


if __name__ == '__main__':
	app.run(debug=False)
