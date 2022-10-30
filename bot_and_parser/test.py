import datetime
from collections import namedtuple

import bs4
import requests


class MyhomeParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

    def get_page(self, params, page: int = None):
        if page and page > 1:
            params['p'] = page

        url = 'https://www.myhome.ge/ru/s'
        r = self.session.get(url, params=params)
        return r.text

    def get_blocks(self, params):
        text = self.get_page(params, page=2)
        soup = bs4.BeautifulSoup(text, 'lxml')

        container = soup.select('div.statement-card')
        for item in container:
            block = self.parse_block(item=item)

    def parse_block(self, item):
        url_block = item.select_one('a.card-container')
        if url_block != None:
            href = url_block.get('href')
            url = href
            print(href)
            print()
        title_block = item.select_one('h5.card-title')
        if title_block != None:
            title = title_block.string.strip()
            print(title)
            print()
        price_block = item.select_one('b.item-price-gel')
        price_block2 = item.select_one('b.item-price-usd')
        if price_block != None and price_block2 != None:
            priceD = price_block.string.strip() + ' GEL'
            priceL = price_block2.string.strip() + ' $'
            print(priceD)
            print(priceL)
        date_block = item.select_one('div.statement-date')
        if date_block != None:
            date = date_block.string.strip()
            print(date)


class data:
    def __init__(self):
        self.city = {'Тбилиси':
                         ['Тбилиси', 1996871],
                     'Батуми':
                         ['Батуми', 874215],
                     'Кутаиси':
                         ['Кутаиси', 8742174],
                     'Рустави':
                         ['Рустави', 5997314]
                     }
        self.regions = {'Тбилиси':
                            {'Глдани': 687578743,
                             'Дидубе': 687611312,
                             'Ваке': 687611312,
                             'Исани': 688350922,
                             'Крцанисский': 689701920,
                             'Мтанцминда': 689678147,
                             'Надзаладеви': 688137211,
                             'Сабуртало': 687602533,
                             'Самгори': 688330506,
                             'Чугурети': 687618311
                             }
                        }
        self.type_s = {'Продажа': 1, 'Аренда': 3, 'Аренда посуточно': 7}
        self.type_s_towr = {'Квартиры': 1, 'Дома и дачи': 2, 'Коммерческая площадь': 3}
        self.OwnerTypeID = {'Собственник': 1, 'Нет': None}

    def formats(self, city_inp, regions_inp, type_s_inp, types_towr_inp, owner_inp, sort=3):
        cityID_last = self.city[city_inp][1]
        cityNAME_last = self.city[city_inp][0]
        region_last = self.regions[city_inp][regions_inp]
        owner_inp = self.OwnerTypeID[owner_inp]
        type_s_last = self.type_s[type_s_inp]
        type_towr_last = self.type_s_towr[types_towr_inp]
        return data.lastForm(self,
                             [cityID_last, cityNAME_last, region_last, owner_inp, type_s_last, type_towr_last, sort])

    def lastForm(self, prelast):
        last_form = {
            'Keyword': prelast[1],
            'cities': prelast[0],
            'AdTypeID': prelast[4],
            'PrTypeID%5B%5D': prelast[5],
            'regions': prelast[2],
            'fullregions': prelast[2],
            'OwnerTypeID': prelast[3]
        }
        return last_form


InnerBlock = namedtuple('Block', 'title,price,curresy,date,url')


class Block(InnerBlock):

    def ___str___(self):
        return f'{self.title}\t{self.price}\t{self.currency}\t{self.date}\t{self.url}'


def main():
    x = data()
    params = x.formats(input('Введите город поиска'), input('Введите регион поиска'), input('Введите тип объявлений'),
                       input('Введите тип собственности'), input('Собственник'))
    p = MyhomeParser()
    p.get_blocks(params)


if __name__ == '__main__':
    main()