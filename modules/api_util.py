import f_util, time, requests

def dump_genres(base_url: str, api_key: str):
	_uri     = f"{base_url}/genres?api_key={api_key}"
	response = requests.get(_uri).json()
	new_data = {}
	for genre in response["genres"]:
		new_data[genre['genre_id']] = genre['genre_name'].lower()
	f_util.write_respose_to_file("config/genres-lower.json", new_data)

def dump_platforms(base_url: str, api_key: str):
	_uri     = f"{base_url}/platforms?api_key={api_key}"
	response = requests.get(_uri).json()
	new_data = {}
	for platform in response['platforms']:
		new_data[platform['platform_name'].lower()] = platform['platform_id']
	f_util.write_respose_to_file("config/platforms.json", new_data)

def load_platforms(base_url: str, api_key: str) -> dict:
	try:
		platforms = f_util.json_to_dict("config/platforms.json")
	except Exception as e:
		f_util.check_directory("config")
		dump_platforms(base_url, api_key)
		platforms = f_util.json_to_dict("config/platforms.json")
	return platforms