# moby-games-platform-dumper
Dumps data from Moby Games API for specific video game platforms.

# Requirements
Python3.6 or possibly newer (written with 3.10)

# Installation
run `pip3 install -r requirements.pip` to install dependencies.

# Usage
run `gui.py` with python or create your own programatic scripts which leverage `api_walker.py` and `platform_cleaner.py`.

# Configuration
!!!YOU MUST ADD YOUR OWN API KEY TO `enduser-config.json`!!!

Recommendations for `enduser-config.json` and `config/`:
- DO NOT set `api_rate_limit` to 1 or lower.
- `magical_game_picker_normalization` and `compress_tags` will mutate the data from Moby Games in ways you may or may not need/appreciate.
- when `compress_tags` is `True` it will cull and replace based on `config/genre-clean.json` (you can modify any of the "rules" in there to compress genres to tags as you see fit)
- `platforms.json` contains a full list of all the platforms on MobyGames as of April 2023. You can delete these if they are overkill for your usecase.

# Web Scraping for Images and Extras
`modules/scrape_game_pages.py` and `modules/scrape_pictures.py` use `playwright` to directly scrape the Moby Games website for data that may not be available in the API. It is much slower than the API, and more expensive for Moby Games. For most usecases the API should fit.

# Junk Code
There is some junk code in here that I haven't gone back to refactor, removed or included in the GUI. 