import time, playwright, f_util
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

def dump_games(platform_id: int, platform_name: str, base_url: str, api_key: str) -> dict:
	new_data = {}
	_limit   = 100
	_uri     = f"{base_url}/games?api_key={api_key}&platform={platform_id}&limit={_limit}"
	with sync_playwright() as p:
		print(f'initializing playwright virtual browser...')
		browser = p.chromium.launch()
		page    = browser.new_page()
		stealth_sync(page)
		print(f'playwright virtual browser ready!')
		for index in range(0,3):
			_start  = time.time()
			_offset = index * _limit
			print(f"\tscraping {_offset} to {(index + 1) * _limit} for {platform_name}")
			_full = f"{_uri}&offset={_offset}"
			_json = page.goto(_full, wait_until="load").json()
			try:
				for game_data in _json['games']:
					new_data[game_data['moby_url'].split("/")[-2]] = game_data
			except Exception as e:
				print(_json)
				break
			if len(_json['games']) < 1:
				print(f"no more games to find on {platform_name}!")
				break
			duration = time.time() - _start
			if duration < 1.2:
				time.sleep(1.3 - duration)
	return new_data