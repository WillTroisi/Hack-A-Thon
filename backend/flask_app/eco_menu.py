from flask import Flask
from flask import render_template
import json
from dataclasses import dataclass
import operator

# faux main

@dataclass
class FoodItem:
	day: str
	meal: str
	calories: float
	protein: float
	fat: float
	carb: float
	ranking: float
	score: float

html_page = 'template_tables.html'

info = None

with open("output.json", "r") as f:
	info = json.loads(''.join(f.readlines()))

def make_food_item_from_json(item_json: dict) -> FoodItem:
	day = item_json['day']
	meal = item_json['meal']
	calories = item_json['calories']
	fat = item_json['fat']
	carb = item_json['carb']
	protein = item_json['protein']
	ranking = item_json['Overall Rating']
	score = item_json['Emission Rating']

	return FoodItem(day, meal, calories, protein, fat, carb, ranking, score)

day_to_index = {
	"monday": 0,
	"tuesday": 1,
	"wednesday": 2,
	"thursday": 3,
	"friday": 4,
	"saturday": 5,
	"sunday": 6,
}

def split_food_item_into_days() -> tuple[7, tuple[FoodItem]]: # seven tuples, each is a day. Monday is 0
	week = [[], [], [], [], [], [], []]
	for item_info in info:

		food_item = make_food_item_from_json(item_info)
		index = day_to_index[food_item.day]
		week[index].append(food_item)
	return week
		

def get_top_three(week, day: str) -> tuple[FoodItem, FoodItem, FoodItem]:
	index = day_to_index[day]
	items = week[index]
	return sorted(items, key=operator.attrgetter('ranking'))[-3:]

week = split_food_item_into_days()

# end faux main

app = Flask(__name__)

@app.route("/")
def landing_page():
	return render_template('front_end.html')

@app.route("/sunday")
def sunday_page():
	day = "sunday"
	third, second, first = get_top_three(week, day)
	return render_template(html_page, 
						day=day,
						item1_name=first.meal,
						item1_carbon_emissions=first.score,
						item1_calories=first.calories,
						item1_protein=first.protein,
						item1_fat=first.fat,
						item1_carbs=first.carb,

						item2_name=second.meal,
						item2_carbon_emissions=second.score,
						item2_calories=second.calories,
						item2_protein=second.protein,
						item2_fat=second.fat,
						item2_carbs=second.carb,

						item3_name=third.meal,
						item3_carbon_emissions=third.score,
						item3_calories=third.calories,
						item3_protein=third.protein,
						item3_fat=third.fat,
						item3_carbs=third.carb,
						) 

@app.route("/monday")
def monday_page():
	day = "monday"
	third, second, first = get_top_three(week, day)
	return render_template(html_page, 
						day=day,
						item1_name=first.meal,
						item1_carbon_emissions=first.score,
						item1_calories=first.calories,
						item1_protein=first.protein,
						item1_fat=first.fat,
						item1_carbs=first.carb,

						item2_name=second.meal,
						item2_carbon_emissions=second.score,
						item2_calories=second.calories,
						item2_protein=second.protein,
						item2_fat=second.fat,
						item2_carbs=second.carb,

						item3_name=third.meal,
						item3_carbon_emissions=third.score,
						item3_calories=third.calories,
						item3_protein=third.protein,
						item3_fat=third.fat,
						item3_carbs=third.carb,
						) 


@app.route("/tuesday")
def tuesday_page():
	day = "tuesday"
	third, second, first = get_top_three(week, day)
	return render_template(html_page, 
						day=day,
						item1_name=first.meal,
						item1_carbon_emissions=first.score,
						item1_calories=first.calories,
						item1_protein=first.protein,
						item1_fat=first.fat,
						item1_carbs=first.carb,

						item2_name=second.meal,
						item2_carbon_emissions=second.score,
						item2_calories=second.calories,
						item2_protein=second.protein,
						item2_fat=second.fat,
						item2_carbs=second.carb,

						item3_name=third.meal,
						item3_carbon_emissions=third.score,
						item3_calories=third.calories,
						item3_protein=third.protein,
						item3_fat=third.fat,
						item3_carbs=third.carb,
						) 


@app.route("/wednesday")
def wednesday_page():
	day = "wednesday"
	third, second, first = get_top_three(week, day)
	return render_template(html_page, 
						day=day,
						item1_name=first.meal,
						item1_carbon_emissions=first.score,
						item1_calories=first.calories,
						item1_protein=first.protein,
						item1_fat=first.fat,
						item1_carbs=first.carb,

						item2_name=second.meal,
						item2_carbon_emissions=second.score,
						item2_calories=second.calories,
						item2_protein=second.protein,
						item2_fat=second.fat,
						item2_carbs=second.carb,

						item3_name=third.meal,
						item3_carbon_emissions=third.score,
						item3_calories=third.calories,
						item3_protein=third.protein,
						item3_fat=third.fat,
						item3_carbs=third.carb,
						) 


@app.route("/thursday")
def thursday_page():
	day = "thursday"
	third, second, first = get_top_three(week, day)
	return render_template(html_page, 
						day=day,
						item1_name=first.meal,
						item1_carbon_emissions=first.score,
						item1_calories=first.calories,
						item1_protein=first.protein,
						item1_fat=first.fat,
						item1_carbs=first.carb,

						item2_name=second.meal,
						item2_carbon_emissions=second.score,
						item2_calories=second.calories,
						item2_protein=second.protein,
						item2_fat=second.fat,
						item2_carbs=second.carb,

						item3_name=third.meal,
						item3_carbon_emissions=third.score,
						item3_calories=third.calories,
						item3_protein=third.protein,
						item3_fat=third.fat,
						item3_carbs=third.carb,
						) 


@app.route("/friday")
def friday_page():
	day = "friday"
	third, second, first = get_top_three(week, day)
	return render_template(html_page, 
						day=day,
						item1_name=first.meal,
						item1_carbon_emissions=first.score,
						item1_calories=first.calories,
						item1_protein=first.protein,
						item1_fat=first.fat,
						item1_carbs=first.carb,

						item2_name=second.meal,
						item2_carbon_emissions=second.score,
						item2_calories=second.calories,
						item2_protein=second.protein,
						item2_fat=second.fat,
						item2_carbs=second.carb,

						item3_name=third.meal,
						item3_carbon_emissions=third.score,
						item3_calories=third.calories,
						item3_protein=third.protein,
						item3_fat=third.fat,
						item3_carbs=third.carb,
						) 


@app.route("/saturday")
def saturday_page():
	day = "saturday"
	third, second, first = get_top_three(week, day)
	return render_template(html_page, 
						day=day,
						item1_name=first.meal,
						item1_carbon_emissions=first.score,
						item1_calories=first.calories,
						item1_protein=first.protein,
						item1_fat=first.fat,
						item1_carbs=first.carb,

						item2_name=second.meal,
						item2_carbon_emissions=second.score,
						item2_calories=second.calories,
						item2_protein=second.protein,
						item2_fat=second.fat,
						item2_carbs=second.carb,

						item3_name=third.meal,
						item3_carbon_emissions=third.score,
						item3_calories=third.calories,
						item3_protein=third.protein,
						item3_fat=third.fat,
						item3_carbs=third.carb,
						) 