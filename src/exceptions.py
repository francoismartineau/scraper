import traceback
import mail, debug

def error(ctx, exception, item=None):
	def get_line():
		tb = str(traceback.format_exc()).split('\n')
		nth = 0
		for i, line in enumerate(tb):
			if "^^" in line:
				nth = i
		return "\n".join(tb[nth-2:nth+1])	
	err = f"{ctx}: {exception}"
	print("Error:", f"{err}\n{get_line()}")
	if item:
		debug.render_item(item)
	mail.send_error(err)

class GetItemException(Exception):
	def __init__(self, site, item=None):
		error(site.__name__, type(self).__name__, item)
class GetItemsError(GetItemException):
	def __init__(self, site, item=None):
		error(site.__name__, type(self).__name__, item)
class GetLinkError(GetItemException):
	def __init__(self, site, item=None):
		error(site.__name__, type(self).__name__, item)
class GetPriceError(GetItemException):
	def __init__(self, site, item=None):
		error(site.__name__, type(self).__name__, item)	
class ConvertPriceError(GetPriceError):
	def __init__(self, site, item=None):
		print(f"item text: |{item.text}|")
		error(site.__name__, type(self).__name__, item)		
class GetNameError(GetItemException):
	def __init__(self, site, item=None):
		error(site.__name__, type(self).__name__, item)			
class GetImageError(GetItemException):
	def __init__(self, site, item=None):
		error(site.__name__, type(self).__name__, item)			
