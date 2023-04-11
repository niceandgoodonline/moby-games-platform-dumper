import time, playwright
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import f_util

def get_cover_image(link_page, image_page, url: str) -> str:
	start = time.time()

	image_url = get_image_url(link_page, url)
	extension = (image_url.split('.'))[-1]
	download_path = f"{game_path}/cover.{extension}"
	download_image(image_page, image_url, download_path)

	duration = time.time() - start
	if duration < 1:
		time.sleep(1 - duration)
	return image_url

def get_screenshots(link_page, image_page, urls: list) -> list:
	screenshot_paths = []
	for url in urls:
		start = time.time()
		image_url = get_image_url(link_page, url)
		extension = (image_url.split('.'))[-1]
		download_path = f"{game_path}/screenshot{count}.{extension}"
		download_image(image_page, image_url, download_path)

		duration = time.time() - start
		if duration < 1:
			time.sleep(1 - duration)
		screenshot_paths.append(image_url)
	return screenshot_paths

def get_image_url(link_page, url: str) -> str:
	link_page.goto(url, wait_until='load')
	raw_img_url = link_page.locator('.img-fluid').get_attribute('src', timeout=300)
	return raw_img_url

def download_image(image_page, image_url: str, download_path: str):
	_bytes = image_page.goto(image_url, wait_until="load").body()
	with open(download_path, "wb+") as image_f:
		image_f.write(_bytes)
	image_f.close()

def get_list_of_image(link_page, image_page, urls: list):
	result = []
	for url in urls:
		result.append(get_image_url(link_page, url))
	return result

if __name__ == "__main__":
	missing = {}
	collection = f_util.json_to_dict("pre_image_scrape.json")
	new_data = {}
	with sync_playwright() as p:
		start_init = time.time()
		browser = p.chromium.launch()
		link_grab_page = browser.new_page()
		image_grab_page = browser.new_page()
		stealth_sync(link_grab_page)
		stealth_sync(image_grab_page)
		print(f"init playwright took {(time.time() - start_init)}")
		for k,v in collection.items():
			missing_data = []
			game_slug = k
			game_data = v.copy()
			game_data['screenshots'] = []
			game_data.pop('promo_pictures')
			screenshots = []
			start_scrape = time.time()
			game_path = f"Data/image/{platform}/{game_slug}"

			if f_util.check_directory(game_path):
				print(f"already scraped images for {game_slug}")

			if len(v['cover']) == 0:
				missing_data.append('cover')
			else:
				print(f"getting cover image for {game_slug}...")
				game_data['cover'] = get_cover_image(link_grab_page, image_grab_page, v['cover'])

			if len(v['screenshots']) != 0:
				print(f"getting screenshots for {game_slug}...")
				screenshots += v['screenshots']
			
			if len(v['promo_pictures']) != 0:
				print(f"getting promos for {game_slug}...")
				screenshots += v['promo_pictures']

			if len(screenshots) > 0:
				game_data['screenshots'] += get_screenshots(link_grab_page, image_grab_page, screenshots)
			else:
				missing_data.append('screenshots')

			if len(missing_data) > 0:
				missing[game_slug] = missing_data

			full_duration = time.time() - start_scrape
			if full_duration < 1:
				print(f"request for {game_slug} took: {full_duration}")
			
			new_data[game_slug] = game_data

	f_util.write_respose_to_file("missing_images.json", missing)
	f_util.write_respose_to_file("post_image_scrape.json", new_data)
