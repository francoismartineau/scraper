import os

def purge_non_numeric(s):
	res = ""
	for c in s:
		if c.isdigit():
			res += c
	return res

def string_strip(s, unwanted_chars):
    translation_table = {ord(char): None for char in unwanted_chars}
    return s.translate(translation_table)	
	# for c in unwanted_chars:
	# 	s.replace(c, "")
	# return s
def has_method(cls, func_name):
	func = getattr(cls, func_name, None)
	return callable(func)

# -- file ----
def increment_file_name(path):
	def _num(i):
		return f"_{i:03d}"
	i = 0
	while os.path.exists(path):
		name, ext = path.rsplit(".")
		if i:
			name = name[:-len(_num(i))]
		i += 1
		path = f"{name}{_num(i)}.{ext}"
	return path

def write_file(path, content):
	path = increment_file_name(path)
	with open(path, 'w', encoding='utf8') as f:
		f.write(content)
# --

if __name__ == "__main__":
	write_file(r"C:\Users\ffran\Desktop\test.txt", "test")