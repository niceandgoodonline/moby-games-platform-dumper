import f_util

parse_struct = ["cover",
	"description",
	"developer",
	"publisher",
	"release",
	"screenshots",
	"tags",
	"trivia"]

def generate_new_parse() -> dict:
	new_parse = {"cover": 0,
				"description": 0,
				"developer": 0,
				"publisher": 0,
				"release": 0,
				"screenshots": 0,
				"tags": 0,
				"trivia": 0}
	return new_parse

def display_data(data: dict):
	matches = parse.keys()
	for k,v in data.items():
		for item in v['missing']:
			if item in matches:
				parse[item] += 1

	for k,v in parse.items():
		print(f"{k}:{v}")

def compare_slugs(main_data: dict, merge_data: dict) -> dict:
	_data = {}
	matches = merge_data.keys()
	_data['matched'] = []
	_data['missing'] = []
	for k,v in main_data.items():
		if k in matches:
			_data['matched'].append(k)
		else:
			_data['missing'].append(k)
	return _data

def find_missing(data: dict):
	for k,v in collection.items():
		game_data = {}
		game_data['name'] = v['name']
		game_data['missing'] = []
		for kk, vv in v.items():
			if len(vv) == 0:
				game_data['missing'].append(kk)

		if len(game_data['missing']) > 0:
			new_data[k] = game_data

if __name__ == "__main__":
	# collection = f_util.json_to_dict("json/near-final.json")
	# merge_json = f_util.json_to_dict("json/slug-first-igdb-fulldump.json")
	# new_data = compare_slugs(collection, merge_json)
	# new_data = {"missing": []}
	# for key in collection_1:
	# 	if key not in collection_2.keys():
	# 		new_data['missing'].append(key)
	# f_util.write_respose_to_file("missing.json", new_data)