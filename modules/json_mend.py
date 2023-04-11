import f_util

def load_scrape(directory: str, extension: str) -> dict:
	_d = {}
	for file in os.listdir(directory):
		if file.endswith(extension):
			_d[file.split(".")[0]] = f_util.json_to_dict(f"{directory}/{file}")
	return _d


def merge_scrape(data):
	merge = {}
	for k,v in data.items():
		for kk, vv in v.items():
			merge[kk] = vv
	f_util.write_respose_to_file("merge.json", merge)


def string_to_list(_string: str, _delimiter: str, _replace_substrings: list = []) -> list:
	print(type(_string))
	for _s in _replace_substrings:
		_string = _string.replace(_s, "")
	print(type(_string))
	return  _string.split(_delimiter)


def find_missing_metadata(data: dict) -> dict:
	_data = {}
	for k,v in data.items():
		game_data = {}
		game_data['name'] = v['name']
		game_data['missing'] = []
		for kk,vv in v.items():
			if len(vv) == 0:
				game_data['missing'].append(kk)
		if len(game_data['missing']) > 0:
			_data[k] = game_data
	return _data


def replace_links_with_local_path(data: dict, base_path) -> dict:
	_data = {}
	for k,v in data.items():
		game_path = f"{base_path}/{k}"
		game_data = v.copy()
		if len(v['cover']) > 0:
			game_data['cover'] = f"{game_path}/cover.jpg"

		number_of_screenshots = len(v['screenshots'])
		if number_of_screenshots > 0:
			game_data['screenshots'] = []
			for index in range(0, number_of_screenshots):
				game_data['screenshots'].append(f"{game_path}/screenshot{index + 1}.jpg")

		_data[k] = game_data
	return _data
