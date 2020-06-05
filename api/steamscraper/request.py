import http3
from bs4 import BeautifulSoup


async def steamstore_request(id):
    url = 'https://store.steampowered.com/app/' + id
    game = {}

    client = http3.AsyncClient()
    page = await client.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    _parse_tree(soup, game)


def _parse_tree(soup, game):
    try:
        game['name'] = soup.find(class_='apphub_AppName').string
        game['description'] = soup.find(class_='game_description_snippet').string.strip('\r\t\n')
        game['developer'] = soup.find('div', attrs={'id': 'developers_list'}).a.string
    except AttributeError as a:
        print('Couldn\'t parse correctly')

    right_div_requirements = soup.find('div', class_='game_area_sys_req_rightCol')
    left_div_requirements = soup.find('div', class_='game_area_sys_req_leftCol')
    _parse_requirements(right_div_requirements, game)
    _parse_requirements(left_div_requirements, game)
    print(game)


def _parse_requirements(div_requirements: str, game):
    print(type(div_requirements))
    if str(div_requirements).find('Minimum') != -1:
        print('entered minimum')
        requirements = {'Memory': 'ram_min', 'Processor': 'cpu_min', 'Graphics': 'gpu_min', 'OS': 'OS_min',
                        'Storage': 'storage_min'}
        _parse_li(requirements, div_requirements, game)
    elif str(div_requirements).find('Recommended') != -1:
        print('entered recommended')
        requirements = {'Memory': 'ram_rec', 'Processor': 'cpu_rec', 'Graphics': 'gpu_rec', 'OS': 'OS_rec',
                        'Storage': 'storage_rec'}
        _parse_li(requirements, div_requirements, game)
    else:
        print('No mininum or recommended?')


def _parse_li(requirements: dict, div_requirements: str, game):
    ul = div_requirements.find('ul', class_='bb_ul')
    reqs_li = ul.find_all('li')
    req_keys = requirements.keys()
    for li in reqs_li:
        for k in req_keys:
            if li.find(k) != -1:
                #adds current li child if it's one of the requirements
                game[requirements[k]] = _parse_soup(li)


def _parse_soup(li_item):
    try:
        li_item.strong.extract()
        li_item.br.extract()
    except AttributeError:
        print('There was no br or strong tag')
    return li_item.string