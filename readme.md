# Scrapes for items on the web

An item will generally have a picture, name, price and link, but qualities can be anything, as long as the specified website's class implements functions to scrape these.

Filters are then responsible to choose items of their respective category.

Items are listed in a Google Sheets document.
![sheets](https://i.postimg.cc/rmz6m0HP/screenshot.png)

User is notified by an email linking to the sheets document.

.src/sites.py specifies how to get qualities of items from a site

.src/filters.py gets qualities from an items and decides if the item is interesting. Qualities that are likely to eliminate an item are scraped first. The order is specified in topics/*.json "cols":[[ "quality", nth_scraped ], ...]

.src/exceptions.py ensures an error will be clearly identified as coming from scraping which quality in which site

.src/data.py loads the topic and saves seen items ids to a .pickle file. This way, an item will never be found twice. The user can then delete unwanted results once and forever.

Requirements:
.env file with EMAIL_PASSWORD=... your gmail api password 
credentials.json file in order to connect with the sheets api
