import f_util

def new_game_data():
	new_game_data = {}
	new_game_data['cover'] = ""
	new_game_data['name'] = ""
	new_game_data['moby-id'] = ""
	new_game_data['moby-link'] = ""
	new_game_data['release'] = ""
	new_game_data['developer'] = []
	new_game_data['publisher'] = []
	new_game_data['description'] = []
	new_game_data['screenshots'] = []
	new_game_data['tags'] = []
	new_game_data['trivia'] = []
	return new_game_data

def get_name(data: dict) -> str:
	_name = game_slug
	keys  = data.keys()
	if 'name' in keys:
		return data['name']
	elif 'title' in keys:
		_name = data['title']
	return _name

def get_name(data: dict) -> str:
	_cover = ""
	keys   = data.keys()
	if 'cover' in keys:
		return data['cover']
	elif 'sample_cover' in key:
		try:
			_cover = data['sample_cover']['image']
		except Exception:
			pass
	return _cover

def get_id(data: dict) -> str:
	_id  = ""
	keys = data.keys()
	if 'moby-id' in keys:
		return data['moby-id']
	elif 'game_id' in keys:
		_id = data['game_id']
	elif 'moby_url' in keys:
		_id = data['moby_url'].split('/')[-3]
	return _id

def get_moby_link(data: dict) -> str:
	_link = ""
	keys  = data.keys()
	if 'moby_url' in keys:
		return data['moby_url']
	elif 'moby_url' in keys:
		_link = data['moby_url']
	return _link

def get_release_date(data: dict, id: int) -> str:
	_release_date = ""
	keys          = data.keys()
	if 'release' in keys:
		return data['release']
	elif 'platforms' in keys:
		for platform in data['platforms']:
			if platform['platform_id'] == id:
				_release_date = platform['first_release_date']
	return _release_date

def get_description(data: dict, description_clean: list) -> list:
	_description = []
	keys         = data.keys()
	if isinstance(data['description'], list):
		return data['description']
	elif 'description' in keys:
		_clean = data['description']
		if _clean == None:
			return []
		for item in description_clean:
			_clean = _clean.replace(item, "")
		_list = _clean.split("<p>")
		if _list[0] == "":
			_list.pop(0)
		return _list
	return _description

def get_genres(data: dict) -> list:
	_genres_list = []
	keys         = data.keys()
	if 'tags'in keys:
		return data['tags']
	elif 'genres' in keys:
		for genre in data['genres']:
			_genres_list.append(genre['genre_name'].lower())
	return _genres_list

def get_screenshots(data: dict) -> list:
	_screenshots = []
	keys         = data.keys()
	if 'screenshots' in keys:
		return data['screenshots']
	elif 'sample_screenshots' in data.keys():
		for screenshot in data['sample_screenshots']:
			_screenshots.append(screenshot['image'])
	return _screenshots

def normalize_for_magic_game_picker(data: dict, platform_id: int, description_clean: list = []):
	new_data = {}
	for k,v in data.items():
		game_slug                = k
		game_data                = new_game_data()
		game_data['name']        = get_name(v)
		game_data['cover']       = get_name(v)
		game_data['moby-id']     = get_id(v)
		game_data['moby-link']   = get_moby_link(v)
		game_data['release']     = get_release_date(v, platform_id)
		game_data['description'] = get_description(v, description_clean)
		game_data['tags']        = get_genres(v)
		game_data['screenshots'] = get_screenshots(v)
		new_data[k]              = game_data
	return new_data