import requests
import pandas as pd
from dataclasses import dataclass
from enum import Enum, auto
import math

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
	Thursdday = auto(),
	Friday = auto(),
	Saturday = auto(),
	Sunday = auto(),
	All_Week = auto()

@dataclass
class FoodItem():
	location: str
	serving_time: ServingTime
	serving_day: ServingDay
	name: str
	ingredients: str = None
	calories: int = None
	protein: int = None
	fats: int = None
	carbs: int = None


def get_all_menu_items(df: pd.DataFrame) -> list[FoodItem]:

	current_location = None
	i = 0
	food_items: list[FoodItem] = []
	
	for row in df.iterrows():
		values = row[1].values # access series
		
		serving_time = ServingTime.All_Day


		#location or nan

		if isinstance(values[0], str):
			current_location = values[0]
		
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
			food_items.append(FoodItem(current_location, serving_time, ServingDay.Monday, monday_item))
		
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
			food_items.append(FoodItem(current_location, serving_time, ServingDay.Thursdday, thursday_item))
		
		friday_item = values[6]
		if isinstance(friday_item, str):
			friday_item = friday_item.lower()
			food_items.append(FoodItem(current_location, serving_time, ServingDay.Friday, tuesday_item))

		saturday_item = values[7]
		if isinstance(saturday_item, str):
			saturday_item = saturday_item.lower()
			food_items.append(FoodItem(current_location, serving_time, ServingDay.Saturday, saturday_item))

		sunday_item = values[8]
		if isinstance(sunday_item, str):
			sunday_item = sunday_item.lower()
			food_items.append(FoodItem(current_location, serving_time, ServingDay.Sunday, sunday_item))
			
	return food_items


def main():
	boulder2_link = "https://www.loyola.edu/-/media/department/dining/documents/menus/boulder2/boulder2_4,-d-,01,-d-,24.ashx?la=en"
	boulder_link = "https://www.loyola.edu/-/media/department/dining/documents/menus/boulder/boulder_4,-d-,01,-d-,24.ashx?la=en"
	menus = [boulder_link]
	
	filenames = download_menus(menus)
	print(filenames)
	dfs = open_dfs_from_xlsx_filenames(filenames)
	food_items = get_all_menu_items(dfs[0])
	for item in food_items:
		print(item)




main()