import json, os, time, shutil

def check_file_exists(_file_name):
	return os.path.exists(_file_name)

def check_directory(_directory: str):
	if not os.path.exists(_directory):
		os.mkdir(_directory)
		return False
	else:
		return True

def backup_file(_file_name):
	if (check_file_exists):
		shutil.move(_file_name, f"{_file_name}.{time.time()}")

def json_to_dict(_file_name):
	_f = {}
	with open(_file_name, encoding="utf-8") as _json_file:
			_f = json.load(_json_file)
	_json_file.close()
	return _f

def write_respose_to_file(_file_name: str, _json: dict, _indent: int = 4, _seperators: tuple = (", ", ": "), _sort_keys: bool = True):
	_t = ".json"
	if check_file_exists(_file_name):
		_t = f".{time.time()}.json"
		print(f"file already exists for {_file_name}. saving as {_file_name.replace('.json', _t)}")
	_file_name = f"{_file_name.replace('.json', _t)}"
	with open(_file_name, 'w+') as f:
		json.dump(_json, f, indent=_indent, separators=_seperators, sort_keys=_sort_keys)
	f.close()
