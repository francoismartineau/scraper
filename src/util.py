def has_method(cls, func_name):
	func = getattr(cls, func_name, None)
	return callable(func)