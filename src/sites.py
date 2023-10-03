import time
from selenium import webdriver
import selenium_options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from exceptions import GetItemException, GetItemsError, GetLinkError, GetPriceError, ConvertPriceError, GetNameError, GetImageError 
import util, debug

def scroll(driver):
	doc_height = int(driver.execute_script("return document.body.scrollHeight"))
	for i in range(1, doc_height, 5):
		driver.execute_script(f"window.scrollTo(0,{i})")
	print("scrolled")

def convert_price(price):
	price = price.rstrip(",. $")
	try:
		price = float(price)
	except ValueError:
		price = ""
	return price

class Site:
	@classmethod
	def get_items(cls, driver):
		return cls._get_items(driver)	
	@classmethod
	def get_kilo(cls, item):
		kilo_sites = [MarketPlace, Kijiji]
		if cls in kilo_sites:
			return cls._get_kilo(item)
		return ""
	@classmethod
	def get_link(cls, item):
		return cls._get_link(item)
	@classmethod
	def get_name(cls, item):
		return cls._get_name(item)
	@classmethod
	def get_price(cls, item):
		return cls._get_price(item)
	@classmethod
	def get_image(cls, item):
		return cls._get_image(item)	

	@classmethod
	def _get_items(cls, driver):
		items = []
		try:
			print("get items...")
			items = cls._get_items(driver)
		except WebDriverException:
			raise GetItemsError(site=cls)
		return items
	@classmethod
	def _get_kilo(cls, item):
		kilo = ""
		try:
			kilo = cls._get_kilo(item)
		except WebDriverException:
			raise GetLinkError(site=cls, item=item)
		return kilo			
	@classmethod
	def _get_link(cls, item):
		link = ""
		try:
			link = cls._get_link(item)
		except WebDriverException:
			raise GetLinkError(site=cls, item=item)
		return link
	@classmethod
	def _get_name(cls, item):
		name = ""
		try:
			name = cls._get_name(item)
		except WebDriverException:
			raise GetNameError(site=cls, item=item)
		return name
	@classmethod
	def _get_price(cls, item):
		price = ""
		try:
			price = cls._get_price(item)
		except WebDriverException:
			raise GetPriceError(site=cls, item=item)
		return price				
	@classmethod
	def _get_image(cls, item):
		image = ""
		try:
			image = cls._get_image(item)
		except WebDriverException:
			raise GetImageError(site=cls, item=item)
		return image	

class Kijiji(Site):
	@classmethod
	def get_items(cls, driver):
		return super()._get_items(driver)
	@classmethod
	def get_name(cls, item):
		return super()._get_name(item)
	@classmethod
	def get_link(cls, item):
		return super()._get_link(item)
	@classmethod
	def get_price(cls, item):
		return super()._get_price(item)
	@classmethod
	def get_image(cls, item):
		return super()._get_image(item)
	@classmethod
	def get_kilo(cls, item):
		return super()._get_kilo(item)
		
	@classmethod
	def _get_items(cls, driver):
		scroll(driver)
		items = WebDriverWait(driver, 3).until(lambda x: x.find_element(By.CSS_SELECTOR, 'ul[data-testid="srp-search-list"]'))
		items = WebDriverWait(driver, 3).until(lambda x: x.find_elements(By.CSS_SELECTOR, 'li'))
		def is_item(item):
			id = item.get_attribute("data-testid")
			return isinstance(id, str) and id.startswith("listing-card-list-item")
		items = list(filter(is_item, items))
		return items
	@classmethod
	def _get_link(cls, item):
		link = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
		return link
	@classmethod
	def _get_name(cls, item):
		name = item.find_element(By.CSS_SELECTOR, "a").text
		return name
	@classmethod
	def _get_price(cls, item):
		price = item.text
		pos = price.find("$")
		price = price[pos:]
		price = price[:price.find(".")]
		price = util.purge_non_numeric(price)
		try:
			price = float(price)
		except ValueError:
			price = ""
		return price
	@classmethod
	def _get_image(cls, item):
		image = WebDriverWait(item, 3).until(lambda x: x.find_element(By.CSS_SELECTOR, 'img'))
		src = image.get_attribute('src')
		return src
	@classmethod
	def _get_kilo(cls, item):
		tmp = item.text.lower()
		tmp = tmp[:tmp.rfind(" km")]
		kilo = ""
		for c in reversed(tmp):
			if c.isdigit():
				kilo = c + kilo
			elif not c.isdigit() and c not in [' ', ',']:
				break
		if kilo.isdigit():
			kilo = int(kilo)
		return kilo

class MarketPlace(Site):
	@classmethod
	def get_image(cls, item):
		return super()._get_image(item)
	@classmethod
	def get_link(cls, item):
		return super()._get_link(item)	
	@classmethod
	def get_items(cls, driver):
		return super()._get_items(driver)	
	@classmethod
	def get_name(cls, item):
		return super()._get_name(item)
	@classmethod
	def get_price(cls, item):
		return super()._get_price(item)
	
	@classmethod
	def _get_items(cls, driver):
		scroll(driver)
		xpath = '//*[contains(text(), "C$")]/../../../../../../..'
		items = WebDriverWait(driver, 6).until(lambda x: x.find_elements(By.XPATH, xpath))
		return items
	@classmethod
	def _get_link(cls, item):
		html = item.get_attribute('outerHTML')
		href = html[html.find("href=\"") + 6:]
		href = href[:href.find("\"")]
		href = "https://www.facebook.com" + href
		def trim_after_id(href):
			id_start = href.find("item/") + 5
			id_end = href[id_start:].find("/") + 1
			return href[:id_start+id_end]		
		return trim_after_id(href)
	@classmethod
	def _get_name(cls, item):
		return item.find_element(By.CSS_SELECTOR, "span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6").text
	@classmethod
	def _get_price(cls, item):
		price = item.text
		pos = price.find("$")
		price = price[pos:]
		price = price[:price.find("\n")]
		price = util.purge_non_numeric(price)
		try:
			price = float(price)
		except ValueError:
			price = ""
		return price
	@classmethod
	def _get_image(cls, item):
		image = item.find_element(By.CSS_SELECTOR, "img")
		src = image.get_attribute('src')
		return src
	@classmethod
	def _get_kilo(cls, item):
		tmp = item.text.lower()
		tmp = tmp[:tmp.find(" km")]
		tmp 
		kilo = ""
		for i, c in enumerate(reversed(tmp)):
			if c.isdigit():
				kilo = c + kilo
			elif c == 'k' and (i < len(tmp) and list(reversed(tmp))[i+1].isdigit()):
				kilo = "000" + kilo
			elif not c.isdigit() and c not in [' ', ',']:
				break
		if kilo.isdigit(): 
			kilo = int(kilo)
		return kilo		
	
class Exo(Site):
	@classmethod
	def _get_items(cls, driver):
		time.sleep(2)
		return driver.find_elements(By.CSS_SELECTOR, "a.c-card-product")
	@classmethod
	def _get_link(cls, item):
		return item.get_attribute('href')
	@classmethod
	def _get_name(cls, item):
		brand = item.find_element(By.CSS_SELECTOR, "h4.c-card-product__brand").text
		model = item.find_element(By.CSS_SELECTOR, "h3.c-card-product__title").text		
		return f"{brand} {model}" 
	@classmethod
	def _get_price(cls, item):
		discount = "span.o-price__discount"
		regular = "span.o-price.c-card-product__price"
		if len(item.find_elements(By.CSS_SELECTOR, discount)) > 0:
			price = item.find_element(By.CSS_SELECTOR, discount).text
		elif len(item.find_elements(By.CSS_SELECTOR, regular)) > 0:
			price = item.find_element(By.CSS_SELECTOR, regular).text
		price = float(price[1:])
		return price
	@classmethod
	def _get_image(cls, item):
		image = item.find_element(By.CSS_SELECTOR, "img")\
				.get_attribute('src')
		return image
	
class Empire(Site):
	@classmethod
	def _get_items(cls, driver):
		scroll(driver)
		time.sleep(4)
		items = driver.find_elements(By.CSS_SELECTOR, "div.ss__result.collection__item.grid__item.small--6.medium-up--3.ss__result--item")
		# for item in items:
			# print(item)
		return items
	@classmethod
	def _get_link(cls, item):
		return item.find_element(By.CSS_SELECTOR, "a.image-link").get_attribute('href')
	@classmethod
	def _get_name(cls, item):
		brand = item.find_element(By.CSS_SELECTOR, "h3").get_attribute('innerHTML')
		model = item.find_element(By.CSS_SELECTOR, "span.collection__item-title").get_attribute('innerHTML')
		name = f"{brand} {model}" 
		# print(name)
		return name

	@classmethod
	def _get_price(cls, item):
		def price_length(price):
			length = 0
			found_dot = False
			for c in price:
				if c.isdigit() or (not found_dot and c == "."):
					length += 1
				else:
					break
				if c == "." and not found_dot:
					found_dot = True
			return length
		price = item.find_element(By.CSS_SELECTOR, "p").get_attribute('innerHTML')
		price = price[1:]
		try:
			price = float(price[:price_length(price)])
		except ValueError:
			price = ""
		return price

	@classmethod
	def _get_image(cls, item):
		image = item.find_element(By.CSS_SELECTOR, "img")
		src = image.get_attribute('data-srcset')
		src = src[:src.find(" ")]
		return src
	
class FiveO(Site):
	@classmethod
	def _get_items(cls, driver):
		time.sleep(1)
		return driver.find_elements(By.CSS_SELECTOR, "form.card.oe_product_cart")
	@classmethod
	def _get_link(cls, item):
		return item.find_element(By.CSS_SELECTOR, "a.d-block.h-100").get_attribute('href')
	@classmethod
	def _get_name(cls, item):
		return item.find_element(By.CSS_SELECTOR, "a.product_name.te_2_line").text
	@classmethod
	def _get_price(cls, item):
		price = item.find_element(By.CSS_SELECTOR, "span.oe_currency_value").text
		try:
			price = float(price)
		except ValueError:
			price = ""
		return price
	@classmethod
	def _get_image(cls, item):
		image = item.find_element(By.CSS_SELECTOR, "img")\
				.get_attribute('src')
		return image

class Simons(Site):
	@classmethod
	def get_items(cls, driver):
		return super()._get_items(driver)
	@classmethod
	def get_name(cls, item):
		return super()._get_name(item)
	@classmethod
	def get_link(cls, item):
		return super()._get_link(item)
	@classmethod
	def get_price(cls, item):
		return super()._get_price(item)
	@classmethod
	def get_image(cls, item):
		return super()._get_image(item)
	@classmethod
	def get_kilo(cls, item):
		return super()._get_kilo(item)
		
	@classmethod
	def _get_items(cls, driver):
		scroll(driver)
		items = WebDriverWait(driver, 3).until(lambda x: x.find_element(By.XPATH, '//*[@id="pbody_wrapper"]/div/div/div/div/div[2]/div[2]/div[1]/div'))
		items = WebDriverWait(driver, 3).until(lambda x: x.find_elements(By.CSS_SELECTOR, 'a.productCard'))
		return items
	@classmethod
	def _get_link(cls, item):
		link = item.get_attribute('href')
		return link
	@classmethod
	def _get_name(cls, item):
		name = f"{item.find_element(By.CSS_SELECTOR, 'p.productCard-name').text}\n\
			{item.find_element(By.CSS_SELECTOR, 'p.productCard-brand').text}"
		return name
	@classmethod
	def _get_price(cls, item):
		txt = item.find_element(By.CSS_SELECTOR, 'div.productPrice').text
		try:
			price = txt[txt.rfind("$")+1:txt.rfind(".")+3]
			price = float(price)
		except ValueError:
			return ""
		if "for" in txt:
			pos = txt.rfind("for") - 2
			n = txt[pos:pos+1]
			if n.isdigit():
				price /= int(n)	
		return price	
	@classmethod
	def _get_image(cls, item):
		image = WebDriverWait(item, 3).until(lambda x: x.find_element(By.CSS_SELECTOR, 'img'))
		src = image.get_attribute('src')
		return src
