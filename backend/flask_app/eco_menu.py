from flask import Flask

app = Flask(__name__)

@app.route("/")
def landing_page():
	return "<p>landing</p>"

@app.route("/sunday")
def landing_page():
	return "<p>landing</p>"


@app.route("/monday")
def landing_page():
	return "<p>landing</p>"

@app.route("/tuesday")
def landing_page():
	return "<p>landing</p>"

@app.route("/wednesday")
def landing_page():
	return "<p>landing</p>"

@app.route("/thursday")
def landing_page():
	return "<p>landing</p>"

@app.route("/friday")
def landing_page():
	return "<p>landing</p>"

@app.route("/saturday")
def landing_page():
	return "<p>landing</p>"