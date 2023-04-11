import sys
sys.path.insert(1, './modules/')
import f_util, process_tags, process_scrape, api_util
# "api_key": "https://www.mobygames.com/info/api/#authorization",
# add a valid mobygames api key here, and look up your platform id in config/platforms.json
# if your desired platform is not in config/platforms.json BUT mobygames has updated to include it, you can delete config/platforms.json and run modules/api_util.dump_platforms()
class Platform_Cleaner(object):
	def __init__(self, config):
		self.config            = config
		self.normalize_for_mgp = config['magical_game_picker_normalization']
		self.description_clean = config['description_clean']
		self.compress_tags     = config['compress_tags']
		self.cleanup_data      = f_util.json_to_dict("config/genre-clean.json")
		self.platforms         = api_util.load_platforms(config['base_url'], config['api_key'])
		self.platform_name     = config['platform']
		self.platform_id       = self.platforms[config['platform']]
		self.platform_path     = f"json/{self.platform_name}"
		self.web_file_out      = f"{self.platform_path}/moby-web-paths.json"
		self.local_file_out    = f"{self.platform_path}/moby-local-paths.json"
		self.genre_json_path   = f"{self.platform_path}/genres.json"
		self.genres_path       = f"{self.platform_path}/genres"

	def convert_genres_to_tags(self):
		data = f_util.json_to_dict(self.web_file_out)
		if self.normalize_for_mgp:
			data = process_scrape.normalize_for_magic_game_picker(data, self.platform_id, self.description_clean)

		try:
			data = process_tags.flatten_genres_to_tags(data)
		except Exception:
			pass

		if self.compress_tags:
			data = process_tags.cull(data, self.cleanup_data['cull'])			
			data = process_tags.replace(data, self.cleanup_data['replace'])
		f_util.backup_file(self.web_file_out)
		f_util.write_respose_to_file(self.web_file_out, data)			

	def tune_tags(self):
		genres   = f_util.json_to_dict(self.genre_json_path)
		culled   = process_tags.cull_naive_genres(genres["tags"], self.cleanup_data["cull"])
		replaced = process_tags.replace_naive_genres(culled, self.cleanup_data["replace"])
		f_util.backup_file(self.genre_json_path)
		f_util.write_respose_to_file(self.genre_json_path, {"tags":replaced})

if __name__ == "__main__":
	_cleaner = Platform_Cleaner()
	_cleaner.convert_genres_to_tags()
