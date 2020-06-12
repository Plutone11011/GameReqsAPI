from bs4 import BeautifulSoup

def parse_tree(soup, game):
    try:
        game['name'] = soup.find(class_='apphub_AppName').string
        game['description'] = soup.find(class_='game_description_snippet').string.strip('\r\t\n')
        game['developer'] = soup.find('div', attrs={'id': 'developers_list'}).a.string
    except AttributeError:
        print('Couldn\'t parse name, description or developer')

    right_div_requirements = soup.find('div', class_='game_area_sys_req_rightCol')
    left_div_requirements = soup.find('div', class_='game_area_sys_req_leftCol')

    _parse_requirements(right_div_requirements, game)
    _parse_requirements(left_div_requirements, game)
    # some games do not have left and right div for minimum
    # and recommended requirements respectively
    if 'ram_min' not in game and 'ram_rec' not in game:
        div_requirements = soup.find('div', class_='game_area_sys_req_full')
        _parse_requirements(div_requirements, game)


def _parse_requirements(div_requirements: str, game):

    if str(div_requirements).find('Minimum') != -1:
        requirements = {'Memory': 'ram_min', 'Processor': 'cpu_min', 'Graphics': 'gpu_min', 'OS': 'OS_min',
                        'Storage': 'storage_min'}
        _parse_li(requirements, div_requirements, game)
    elif str(div_requirements).find('Recommended') != -1:
        requirements = {'Memory': 'ram_rec', 'Processor': 'cpu_rec', 'Graphics': 'gpu_rec', 'OS': 'OS_rec',
                        'Storage': 'storage_rec'}
        _parse_li(requirements, div_requirements, game)
    else:
        print('No mininum or recommended?')


def _parse_li(requirements: dict, div_requirements: str, game):
    ul = div_requirements.find('ul', class_='bb_ul')
    try:
        reqs_li = ul.find_all('li')
        req_keys = requirements.keys()
        for li in reqs_li:
            for k in req_keys:
                if str(li).find(k) != -1:
                    # adds current li child if it's one of the requirements
                    game[requirements[k]] = _parse_text(li)
    except AttributeError:
        print('No li in unordered list')


def _parse_text(li_item):
    try:
        li_item.strong.extract()
        li_item.br.extract()
    except AttributeError:
        print('There was no br or strong tag')
    return li_item.string