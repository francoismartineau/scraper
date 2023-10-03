from data import Data

def link_filter(link):
	return not Data.already_seen(link)

# --
def van(col, vals):
	def price_filter(price):
		return price == "" or (price < 10000 and price > 1000)
	def name_filter(name):
		name = name.lower()
		for word in ["campeur", "f-", "f150", "f250", "f350", "450", "cube", "box", "moteur"]:
			if word in name:
				return False
		if "ford" not in name:
			return False
		if "econoline" in name or \
			"van" in name or \
			("e" in name and "50" in name):
			return True
		return False
	def kilo_filter(kilo):
		return not isinstance(kilo, int) or kilo < 200000
	def default(_):
		return True
	return {'price': price_filter,
		 'name': name_filter,
		 'kilo': kilo_filter,
		 'link': link_filter,
		 }.get(col, default)(vals[col])

def nv200(col, vals):
	def price_filter(price):
		return price == "" or (price < 16000 and price > 1000)
	def name_filter(name):
		name = name.lower()
		return "nv" in name and "nissan" in name
	def kilo_filter(kilo):
		return not isinstance(kilo, int) or kilo < 200000
	def default(_):
		return True
	return {'price': price_filter,
		 'name': name_filter,
		 'kilo': kilo_filter,
		 'link': link_filter,
		 }.get(col, default)(vals[col])

# --
def decks(col, vals):
	def price_filter(price):
		if price == "" or price <= 58:
			return True
		for brand in ["element"]:
			if brand in vals['name'].lower() and price <= 80:
				return True
		return False
	def name_filter(name):
		for brand in ["orloge simard", "123 punk"]:
			if brand in name.lower():
				return False
		return True
	def default(_):
		return True	
	return {'price': price_filter,
		 'name': name_filter,
		 'link': link_filter,
		 }.get(col, default)(vals[col])	

def shoes(col, vals):
	def name_filter(name):
		return "wino g6 slip-on" in name.lower()
	def price_filter(price):
		return price == "" or price <= 65
	def default(_):
		return True	
	return {'price': price_filter,
		 'name': name_filter,
		 'link': link_filter,
		 }.get(col, default)(vals[col])		

# --
def projecteurs(col, vals):
	def name_filter(name):
		name = name.lower()
		return "projecteur" in name \
			and "diapo" not in name
	def price_filter(price):
		return price == "" or (price > 20 and price <= 200)
	def default(_):
		return True
	return {'price': price_filter,
		 'name': name_filter,
		 'link': link_filter,
		 }.get(col, default)(vals[col])
	
def lave_vaisselle(col, vals):
	def name_filter(name):
		name = name.lower()
		return "vaisselle" in name \
			and "laveuse" not in name
	def price_filter(price):
		return price == "" or price <= 200
	def default(_):
		return True
	return {'price': price_filter,
		 'name': name_filter,
		 'link': link_filter,
		 }.get(col, default)(vals[col])
	
def boxers(col, vals):
	def price_filter(price):
		return price == "" or price <= 20
	def default(_):
		return True
	return {'price': price_filter,
		 'link': link_filter,
		 }.get(col, default)(vals[col])