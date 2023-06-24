import sys
sys.path.insert(1, './modules/')
import f_util, api_util, process_scrape, process_tags, requests, time

# "api_key": "https://www.mobygames.com/info/api/#authorization",
# add a valid mobygames api key here, and look up your platform id in config/platforms.json
# if your desired platform is not in config/platforms.json BUT mobygames has updated to include it, you can delete config/platforms.json and run modules/api_util.dump_platforms()
class Api_Walker(object):
	def __init__(self, config):
		self.config  = config
		self.api_key = config['api_key']
		if self.api_key == False:
			print(f"no API key found, you need to create one. visit https://www.mobygames.com/info/api/ to learn more!")
			exit()
		self.base_url          = config['base_url']
		self.description_clean = config['description_clean']
		self.format            = config['format'] 		
		self.mgp_bool          = config['magical_game_picker_normalization']
		self.api_rate_limit    = config['api_rate_limit']
		self.platforms         = api_util.load_platforms(self.base_url, self.api_key)
		self.platform_name     = config['platform']
		self.platform_id       = self.platforms[config['platform']]
		self.platform_path     = f"json/{self.platform_name}"
		self.web_file_out      = f"{self.platform_path}/moby-web-paths.json"
		self.local_file_out    = f"{self.platform_path}/moby-local-paths.json"
		self.genre_json_path   = f"{self.platform_path}/genres.json"
		self.genres_path       = f"{self.platform_path}/genres"

	def main(self) -> dict:
		_start   = time.time()
		new_data = self.walk_api()
		f_util.check_directory("./json")
		if len(new_data) > 1:
			f_util.check_directory(self.platform_path)
		f_util.write_respose_to_file(f"{self.web_file_out}", new_data)

	def walk_api(self) -> dict:
		new_data   = {}
		parameters = {"api_key":self.api_key, "format": self.format, "limit":100, "platform": self.platform_id, "offset":0}
		for index in range(0, 1024):
			parameters["offset"] = index * parameters["limit"]
			response             = requests.get("https://api.mobygames.com/v1/games", params=parameters).json()
			if len(response["games"]) < 1:
				break
			for game in response["games"]:
				new_data[game["title"]] = game
			time.sleep(self.api_rate_limit)
		return new_data

if __name__ == "__main__":
	api_walker = Api_Walker(f_util("enduser-config.json"))
	api_walker.main()