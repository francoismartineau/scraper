import mail

def error(ctx, exception):
	print(f"Error: {ctx}: {exception}")
	mail.send_error(exception)

class GetItemException(Exception):
	def __init__(self, site):
		error(type(site).__name__, type(self).__name__)
class GetItemsError(GetItemException):
	def __init__(self, site):
		error(type(site).__name__, type(self).__name__)
class GetLinkError(GetItemException):
	def __init__(self, site):
		error(type(site).__name__, type(self).__name__)
class GetPriceError(GetItemException):
	def __init__(self, site):
		error(type(site).__name__, type(self).__name__)	
class ConvertPriceError(GetPriceError):
	def __init__(self, site, text):
		print(f"item text: |{text}|")
		error(type(site).__name__, type(self).__name__)		
class GetNameError(GetItemException):
	def __init__(self, site):
		error(type(site).__name__, type(self).__name__)			
class GetImageError(GetItemException):
	def __init__(self, site):
		error(type(site).__name__, type(self).__name__)			
