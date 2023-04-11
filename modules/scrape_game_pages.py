import f_util, playwright
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

WAIT_LOW = {"timeout": 500}

def get_game_name(playwright_page) -> str:
	game_name = page.locator(".mb-0").all()[0].inner_text(timeout=500)
	return game_name

def get_cover_url(playwright_page) -> str:
	cover_url = ""
	try:
		cover_url = page.locator("#cover", WAIT_LOW).get_attribute("href")
	except Exception:
		errors.append(f"get cover for {game_slug}")
	return cover_url


def get_release_data(playwright_page) -> dict:
	data = {"release": "", "publisher": [], "developer": []}
	try:
		dev_pub_meta = page.locator(".info-release", WAIT_LOW)
		data["release"] = (dev_pub_meta.locator("a").all())[0].inner_text().strip()
		pub = dev_pub_meta.locator("#publisherLinks", WAIT_LOW).locator("li").all()
		for item in pub:
			data["publisher"].append(item.inner_text())
		dev = dev_pub_meta.locator("#developerLinks", WAIT_LOW).locator("li").all()
		for item in dev:
			data["developer"].append(item.inner_text())
	except Exception:
		errors.append(f"get release for {game_slug}")
	return data


def get_genre_data(playwright_page) -> dict:
	data = {}
	try:
		genre_meta = page.locator(".info-genres", WAIT_LOW)
		genre_keys = genre_meta.locator("dt", WAIT_LOW).all()
		genre_data = genre_meta.locator("dd", WAIT_LOW).all()
		for index in range(0, len(genre_keys) - 1):
			_key = genre_keys[index].inner_text().lower()
			data[_key] = []
			for link in genre_data[index].locator("a", WAIT_LOW).all():
				data[_key].append(link.inner_text().lower().strip())
	except Exception:
		errors.append(f"get genre for {game_slug}")
	return data


def get_description(playwright_page) -> str:
	description = ""
	try:
		description_paragraphs = page.locator("#description-text", WAIT_LOW).locator('p', WAIT_LOW).all()
		description = ""
		for item in description_paragraphs:
			description += f"{item.inner_text()}\n\n"
	except Exception:

		errors.append(f"get description for {game_slug}")
	return description.strip()


def get_screenshot_links(playwright_page) -> list:
	screenshot_links = []
	try:
		screenshot_elements = page.locator("#gameShots", WAIT_LOW).locator("a", WAIT_LOW).all()
		for item in screenshot_elements:
			screenshot_links.append(item.get_attribute('href'))
	except Exception:
		errors.append(f"get screenshot for {game_slug}")
	return screenshot_links


def get_promo_picture_links(playwright_page) -> list:
	promo_links = []
	try:
		promo_elements = page.locator("#gamePromoImages", WAIT_LOW).locator("a", WAIT_LOW).all()
		for item in promo_elements:
			promo_links.append(item.get_attribute('href'))
	except Exception:
		errors.append(f"get promos for {game_slug}")
	return promo_links


def get_trivia_content(playwright_page) -> str:
	trivial_content = ""
	try:
		trivial_content = page.locator("#gameTrivia").inner_text()
	except Exception:
		errors.append(f"get trivia for {game_slug}")
	return trivial_content


if __name__ == "__main__":
	new_data = {}
	json_data = f_util.json_to_dict("scrape/sorted-d.json")
	time_track = time.time()
	with sync_playwright() as p:
		browser = p.chromium.launch()
		page = browser.new_page()
		stealth_sync(page)
		for k,v in json_data.items():
			start = time.time()
			game_slug = k
			game_data = {}
			print(f"scraping {game_slug}")
			page.goto(v, wait_until="networkidle")
			game_data['name'] = get_game_name(page)
			game_data['link'] = v
			game_data.update(get_release_data(page))
			game_data["tags"] = get_genre_data(page)
			game_data["cover"] = get_cover_url(page)
			game_data["description"] = get_description(page)
			game_data["screenshots"] = get_screenshot_links(page)
			game_data["promo_pictures"] = get_promo_picture_links(page)
			game_data["trivia"] = get_trivia_content(page)
			new_data[game_slug] = game_data
			duration = time.time() - start
			if duration < 1:
				_wait = 1 - duration
				time.sleep(_wait)
		page.close()
		browser.close()
	print(time.time() - time_track)
	f_util.write_respose_to_file("game-names.json", new_data)
	with open(f"./log/2000to2003-errors-{time.time()}", 'w+', encoding="utf-8") as f:
		for i in errors:
			f.write(f"{i}\n")
	f.close()

