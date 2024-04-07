import requests
import pandas as pd
from dataclasses import dataclass
from enum import Enum, auto
import math
import selenium
from selenium import webdriver
import selenium.common
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import openfoodfacts

def download_menus(links: list[str]) -> list[str | None]:
	''' @param links The links to the menus
@return The filenames of the menus 
	'''

	xlsx_filenames = []

	for link in links:
		r = requests.get(link)



		if r.status_code != 200:
			print(f"Couldn't grab location: {location_name}")
			continue

		menu_location_in_link = link.find("menus/")
		end_of_url = link[menu_location_in_link+6:]
		pos = end_of_url.find("/")
		location_name = end_of_url[:pos]

		filename = location_name + ".xlsx"
		
		with open(filename, "wb") as f:
			f.write(r.content)
		
		xlsx_filenames.append(filename)
	return xlsx_filenames

def open_dfs_from_xlsx_filenames(filenames: list[str]) -> list[pd.DataFrame]:
	dfs = []
	for filename in filenames:
		dfs.append(pd.read_excel(filename, skiprows=3))
	return dfs

# data format: location,ingredients,protein,fat,carbohydates,cals

class ServingTime(Enum):
	Breakfast = 0,
	Lunch = auto(),
	Dinner = auto(),
	All_Day = auto()

class ServingDay(Enum):
	Monday = 0,
	Tuesday = auto(),
	Wednesday = auto(),
	Thursday = auto(),
	Friday = auto(),
	Saturday = auto(),
	Sunday = auto(),
	All_Week = auto()

@dataclass
class Ingredient():
	name: str
	percent: int


@dataclass
class FoodItem():
	location: str
	serving_time: ServingTime
	serving_day: ServingDay
	name: str
	ingredients: list[Ingredient] = None
	calories: int = None
	protein: float = None
	fats: float = None
	carbs: float = None
	total_grams: float = None


def get_all_menu_items(df: pd.DataFrame) -> list[FoodItem]:

	current_location = None
	i = 0
	food_items: list[FoodItem] = []
	
	for row in df.iterrows():
		values = row[1].values # access series
		
		serving_time = ServingTime.All_Day


		#location or nan

		if isinstance(values[0], str):
			location = values[0].lower()
			if "dinner" in location:
				pos = location.find("dinner")
				location = location[:pos]
			if "lunch" in location:
				pos = location.find("lunch")
				location = location[:pos]
			if "breakfast" in location:
				pos = location.find("breakfast")
				location = location[:pos]
			location = location.replace('/', '')
			location = location.replace('\n', ' ')
			location = location.strip()
			current_location = location
		
		# serving time
		serving_time = values[1]
		if isinstance(serving_time, str):
			if "breakfast" in values[1].lower():
				serving_time = ServingTime.Breakfast
			elif "dinner" in values[1].lower():
				serving_time = ServingTime.Dinner
			elif "lunch" in values[1].lower():
				serving_time = ServingTime.Lunch
		
		# monday

		monday_item = values[2]
		if isinstance(monday_item, str):
			monday_item = monday_item.lower()
			food_items.append(FoodItem(current_location, serving_time, ServingDay.Monday, name=monday_item))
		
		tuesday_item = values[3]
		if isinstance(tuesday_item, str):
			tuesday_item = tuesday_item.lower()
			food_items.append(FoodItem(current_location, serving_time, ServingDay.Tuesday, tuesday_item))

		wednesday_item = values[4]
		if isinstance(wednesday_item, str):
			wednesday_item = wednesday_item.lower()
			food_items.append(FoodItem(current_location, serving_time, ServingDay.Wednesday, wednesday_item))
		
		thursday_item = values[5]
		if isinstance(thursday_item, str):
			thursday_item = thursday_item.lower()
			food_items.append(FoodItem(current_location, serving_time, ServingDay.Thursday, thursday_item))
		
		friday_item = values[6]
		if isinstance(friday_item, str):
			friday_item = friday_item.lower()
			food_items.append(FoodItem(current_location, serving_time, ServingDay.Friday, friday_item))

		saturday_item = values[7]
		if isinstance(saturday_item, str):
			saturday_item = saturday_item.lower()
			food_items.append(FoodItem(current_location, serving_time, ServingDay.Saturday, saturday_item))

		sunday_item = values[8]
		if isinstance(sunday_item, str):
			sunday_item = sunday_item.lower()
			food_items.append(FoodItem(current_location, serving_time, ServingDay.Sunday, sunday_item))
			
	return food_items

def cleanup_menu_items(items: list[FoodItem]):
	for item in items:

		name = item.name
		if (isinstance(name, float)):
			print(item)
		name = name.replace('\n', ' ')
		name = name.replace('/', '')
		pos = name.find('(')
		name = name[:pos]
		name = name.strip()
		name = name.replace("&", 'and')
		if "oatmea" in name:
			item.name = "oatmeal"
			continue
		if "waffles" in name:
			item.name = "waffles"
			continue
		if "roseda" in name:
			item.name = "burger"
			continue
		if "walking" in name:
			item.name = "tacos"
			continue
		if "quesadilla" in name:
			item.name = "chicken quesadilla"
			continue
		if "catfish" in name:
			item.name = "catfish"
			continue
		if "beef burger" in name:
			item.name = "burger"
			continue
		if "omelets" in name:
			item.name = "omelets"
			continue
		if "corned" in name:
			item.name = "beef brisket"
			continue
		if "pizz" in name:
			item.name = name.replace("pizz", "pizza")
			continue
		if "pulled" in name:
			item.name = "pulled pork"



		item.name = name
	


def get_menu_items_nutrition_info(items: list[FoodItem]):
	api = openfoodfacts.API(user_agent="loyola_student_project/1.0")


	for item in items:

		info = api.product.text_search(item.name, page_size=1)
		try:
			info = info['products'][0]
			item.total_grams = info['product_quantity']
			item.calories = info['nutriments']['energy-kcal']
			item.fats = info['nutriments']['fat']
			item.protein = info['nutriments']['proteins']
			item.ingredients = []
			for ingredient_info in info['ingredients']:

				item.ingredients.append(Ingredient(ingredient_info['text'], ingredient_info['percent_estimate']))
			print(f"Grabbed item: {item.name}")
		except Exception as e:
			with open ("sample_r.json", "a") as f:
				f.write(json.dumps(info))




# @dataclass
# class FoodItem():
# 	location: str
# 	serving_time: ServingTime
# 	serving_day: ServingDay
# 	name: str
# 	ingredients: list[Ingredient] = None
# 	calories: int = None
# 	protein: int = None
# 	fats: int = None
# 	carbs: int = None
def write_to_json(items: list[FoodItem]):
	json_data = {}

	def serving_time_to_string(serving_time: ServingTime):
		if serving_time == ServingTime.Breakfast:
			return "breakfast"
		if serving_time == ServingTime.Lunch:
			return "lunch"
		if serving_time == ServingTime.Dinner:
			return "dinner"
		if serving_time == ServingTime.All_Day:
			return "all_day"
	
	def serving_day_to_string(serving_day: ServingDay):
		if serving_day == ServingDay.Monday:
			return "monday"
		if serving_day == ServingDay.Tuesday:
			return "tuesday"
		if serving_day == ServingDay.Wednesday:
			return "wednesday"
		if serving_day == ServingDay.Thursday:
			return "thursday"
		if serving_day == ServingDay.Friday:
			return "friday"
		if serving_day == ServingDay.Saturday:
			return "saturday"
		if serving_day == ServingDay.Sunday:
			return "sunday"
		if serving_day == ServingDay.All_Week:
			return "all_week"
	for item in items:
		if item.ingredients is None:
			continue
		ingredients = {}
		for ingredient in item.ingredients:
			ingredients[ingredient.name] = {
				"name": ingredient.name,
				"percent": ingredient.percent,
			}

		json_data[item.name] = {
			"location": item.location,
			"time": serving_time_to_string(item.serving_time),
			"day": serving_day_to_string(item.serving_day),
			"ingredients": ingredients,
			"calories": item.calories,
			"protein": item.protein,
			"fat": item.fats,
			"carb": item.carbs
		}
	with open("menu_info.json", "w") as f:
		f.write(json.dumps(json_data))



def main():
	boulder2_link = "https://www.loyola.edu/-/media/department/dining/documents/menus/boulder2/boulder2_4,-d-,01,-d-,24.ashx?la=en"
	boulder_link = "https://www.loyola.edu/-/media/department/dining/documents/menus/boulder/boulder_4,-d-,01,-d-,24.ashx?la=en"
	menus = [boulder_link]
	
	filenames = download_menus(menus)
	print(filenames)
	dfs = open_dfs_from_xlsx_filenames(filenames)
	food_items = get_all_menu_items(dfs[0])
	cleanup_menu_items(food_items)
	get_menu_items_nutrition_info(food_items)
	write_to_json(food_items)




main()