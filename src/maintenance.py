import os
from sheets_api import SheetsApi
from topic import Topic

#TODO: reprendre l'image d'un item si elle n'existe plus

if __name__ == "__main__":
	os.remove("token.json")
	SheetsApi.connect()
	SheetsApi.purge_deprecated_links(Topic.pages)
