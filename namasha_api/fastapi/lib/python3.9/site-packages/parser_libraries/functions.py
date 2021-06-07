import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as options
import time

#######################################################################
#         В случае изменения файла - внести поправки в документацию
#                              Документация
#  1) HEADERS - эмуляция браузера пользователя
#
#  2) get_html(ссылка) - возвращает цельный html файл сайта, html.text - текст
#  кода, который принимает BeautifulSoup
#
#  3) get_dig_date(строка с датой рождения, режим):
#     режим 1:
#         Строка представлена в виде день_месяц_год
#     режим 2:
#         Строка представлена в виде год_месяц_день
#     dict - словарь для перевода месяца в численную форму
#     Функция возвращает словарь day, month, year
#
#  4) get_work(строка, режим):
#      режим в зависимости от должности:
#      В строке находится ключевое слово, возвращается значение
#      position_id
#
#  5) split_name(строка, режим)
#      Режим 1:
#          Строка типа ИвановИванИванович разделяется в Иванов Иван Иванович
#      Режим 2:
#          Строка типа ИВАНОВИванИванович разделяется в Иванов Иван Иванович
#      Возвращается массив строк из фамилии, имени, отчества (все в нижнем регистре)
#
#  6) get_name(строка)
#      Возвращается массив строк из фамилии, имени, отчества (все в нижнем регистре)
#
#######################################################################

HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0)   Gecko/20100101 Firefox/69.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru,en-US;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
}


def get_selenium_html(url, driver=None, chromium=None, params=None):
    chromedriver = driver
    if params == "True":
        option = options()
        option.binary_location = chromium
        option.add_argument("-headless")
    else:
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
    browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=option)
    browser.get(url)
    time.sleep(6)
    res = browser.page_source
    browser.quit()
    return res


def get_html(url, params=None):
    return requests.get(url, headers=HEADERS, params=params, verify = False)


def get_dig_date(str, mode=1):
    dict = {'января': 1, 'янв': 1, 'jan': 1, 'january': 1, '1': 1, '01': 1,
            'февраля': 2, 'фев': 2, 'feb': 2, 'february': 2, '2': 2, '02': 2,
            'марта': 3, 'march': 3, '3': 3, '03': 3,
            'апреля': 4, 'april': 4, '4': 4, '04': 4,
            'мая': 5, 'may': 5, '5': 5, '05': 5,
            'июня': 6, 'june': 6, '6': 6, '06': 6,
            'июля': 7, 'july': 7, '7': 7, '07': 7,
            'августа': 8, 'august': 8, '8': 8, '08': 8,
            'сентября': 9, 'september': 9, '9': 9, '09': 9,
            'октября': 10, 'october': 10, '10': 10,
            'ноября': 11, 'november': 11, '11': 11,
            'декабря': 12, 'december': 12, '12': 12,
    }
    str = str.replace('-', ' ')
    str = str.replace('\n', ' ')
    list = str.split()
    ind_d = 0
    ind_m = 1
    ind_y = 2
    if mode == 2:
        ind_d = 2
        ind_m = 1
        ind_y = 0

    try:
        lst = {'day': int(list[ind_d]), 'month': dict[list[ind_m]], 'year': int(list[ind_y])}
    except:
        return -1
    return lst


def get_work(str, mode=1):
    str = str.lower()
    ind = str.find('председатель')
    ind_2 = str.find('заместитель')
    ind_3 = str.find('секретарь')
    if mode == 1:
        if str.find('президент') != -1:
            return 1
    if mode == 16:
        if ind_2 != -1:
            return 17
        if ind != -1:
            return 16
        return 18
    if mode == 19:
        if ind != -1 or ind_2 != -1:
            return 19
        return 20
    if mode == 21:
        if ind != -1:
            return 21
        if ind_2 != -1:
            return 22
        return 23
    if mode == 24:
        if ind_2 != -1:
            return 25
        return 24
    if mode == 29:
        if ind_2 != -1:
            return 30
        return 29
    if mode == 34:
        if ind != -1:
            return 34
        if str.find('Заместитель Председателя'.lower()) != -1:
            return 35
        if str.find('аудитор') != -1:
            return 36
        return -1
    if mode == 38:
        if ind_3 != -1:
            return 40
        elif ind_2 != -1:
            return 39
        elif ind != -1:
            return 38
        return 41
    if mode == 42:
        if str.find('председатель суда') != -1:
            return 42
        if ind_2 != -1:
            return 43
        return 44
    if str.find('Уполномоченный по правам человека'.lower()) != -1:
        return 31
    if str.find('Уполномоченный по защите прав предпринимателей в России'.lower()) != -1:
        return 32
    if str.find('Руководитель Аппарата Правительства'.lower()) != -1:
        return [6, 8]
    if str.find('полномочный представитель Президента'.lower()) != -1:
        return 4
    if str.find('Председатель Правительства Российской Федерации'.lower()) != -1:
        return 2
    if str.find('первый заместитель') != -1:
        return 3
    if str.find('Заместитель Председателя Правительства'.lower()) != -1:
        return 5
    if str.find('министр') != -1:
        return 9
    if str.find('генеральный прокурор российской федерации') != -1:
        return 27


def split_name(str, mode=1):
    if mode == 1:
        str = str.replace('\n', '')
        for st in str:
           if st.isupper():
               str = str.replace(st, (' ' + st))
        str = str.replace('  ', ' ')
    else:
        ind = -1
        for i in range(0, len(str)):
            if str[i].isupper() and str[i+1].islower():
                ind = i
                break
        str = str[0:i] + ' ' + str[i:len(str)]
    return get_name(str.lower())


def get_name(str):
    return str.split()


def get_base(num, base):
    dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F'}
    res = ''
    while num > 0:
        mod = num % base
        if mod > 9:
            mod -= 10;
            mod = dict[mod]
        res = str(mod) + res
        num //= base
    return res


def get_dec(num, base):
    res = 0
    power = 0
    while num > 0:
        res += (num % 10)*(base**power)
        power += 1
        num //= 10
    return res
