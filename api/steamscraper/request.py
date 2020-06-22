import json, asyncio, logging
from bs4 import BeautifulSoup
from marshmallow import ValidationError
from aiohttp import ClientSession, ClientTimeout

from api.steamscraper.parser import parse_tree
from api.db import db, model


async def run_requests():
    timeout = ClientTimeout(total=120)

    async with ClientSession(timeout=timeout) as session:
        async with session.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/') as steam_api_results:
            steam_api_results_text = await steam_api_results.text()
            steam_api_result_list = json.loads(steam_api_results_text)['applist']['apps']
            ids = list(map(lambda obj: obj['appid'], steam_api_result_list))

            url = 'https://store.steampowered.com/app/{}'
            semaphore = asyncio.Semaphore(1000)
            tasks = []

            for game_id in ids:
                task = asyncio.create_task(bound_steam_request(semaphore, url.format(game_id), session))
                tasks.append(task)

            await asyncio.gather(*tasks)


async def bound_steam_request(sem, url, session):
    async with sem:
        await steam_request(url, session)


async def steam_request(url, session):
    game = {}
    try:
        async with session.get(url) as steam_page:
            steam_page_text = await steam_page.text()
            soup = BeautifulSoup(steam_page_text, 'html.parser')
            parse_tree(soup, game)

            if 'name' in game and game['name']:
                try:
                    game_schema = model.GameSchema()
                    game_obj = game_schema.load(game)
                    db.insert_game(game_obj)
                except ValidationError as err:
                    logging.warning(err.messages)
                    logging.warning(err.valid_data)
    except asyncio.CancelledError as cerr:
        raise
    except Exception:
        logging.warning('An error in the request has occurred')



