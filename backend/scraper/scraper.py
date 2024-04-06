import requests
import pandas as pd


def download_menus(links: list[str]) -> list[str | None]:
	''' @param links The links to the menus
@return The filenames of the menus 
	'''

	xlsx_filenames = [[]]

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


def main():
	boulder2_link = "https://www.loyola.edu/-/media/department/dining/documents/menus/boulder2/boulder2_4,-d-,01,-d-,24.ashx?la=en"
	boulder_link = "https://www.loyola.edu/-/media/department/dining/documents/menus/boulder/boulder_4,-d-,01,-d-,24.ashx?la=en"
	menus = [boulder_link]
	
	filenames = download_menus(menus)

main()