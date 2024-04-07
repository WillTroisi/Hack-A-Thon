from flask import Flask
from flask import render_template

app = Flask(__name__)

html_page = 'template_tables.html'

@app.route("/")
def landing_page():
	return render_template('../website/front_end.html')

@app.route("/sunday")
def sunday_page():
	return render_template(html_page) 

@app.route("/monday")
def monday_page():
	return render_template(html_page)

@app.route("/tuesday")
def tuesday_page():
	return render_template(html_page)

@app.route("/wednesday")
def wednesday_page():
	return render_template(html_page)

@app.route("/thursday")
def thursday_page():
	return render_template(html_page)

@app.route("/friday")
def friday_page():
	return render_template(html_page)

@app.route("/saturday")
def saturday_page():
	return render_template(html_page)