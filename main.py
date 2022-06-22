import vk_api
import requests
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from config import user_token, comm_token, offset
from random import randrange
import json
from pprint import pprint
from database import *



vk = vk_api.VkApi(token=comm_token)  # Авторизуемся как сообщество
longpoll = VkLongPoll(vk)  # Работа с сообщениями

def write_msg(user_id, message):  # метод для отправки сообщения
    vk.method('messages.send', {'user_id': user_id,
                                'message': message,
                                'random_id': randrange(10 ** 7)})

# ПОЛУЧЕНИЕ ИМЕНИ ПОЛЬЗОВАТЕЛЯ, КОТОРЫЙ НАПИСАЛ БОТУ
def name(user_id):
    url = f'https://api.vk.com/method/users.get'
    params = {'access_token': user_token,
              'user_ids': user_id,
              'v': '5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    information_dict = response['response']
    for i in information_dict:
        for key, value in i.items():
            first_name = i.get('first_name')
            last_name = i.get('last_name')
            return first_name

# ПОЛУЧЕНИЕ ПОЛА ПОЛЬЗОВАТЕЛЯ, МЕНЯЕТ НА ПРОТИВОПОЛОЖНЫЙ
def get_sex(user_id):
    url = f'https://api.vk.com/method/users.get'
    params = {'access_token':user_token,
              'user_ids':user_id,
              'fields':'sex',
              'v':'5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    information_list = response['response']
    for i in information_list:
        if i.get('sex') == 2:
            find_sex = 1
            return find_sex
        elif i.get('sex') == 1:
            find_sex = 2
            return find_sex

# ПОЛУЧЕНИЕ ВОЗРАСТА ПОЛЬЗОВАТЕЛЯ
def get_age(user_id):
    url = url = f'https://api.vk.com/method/users.get?fields=bdate'
    params = {'access_token':user_token,
              'user_ids': user_id,
              'fields': 'bdate',
              'v': '5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    information_list = response['response']
    for i in information_list:
        date = i.get('bdate')  # Mehod is complited
        date_list = date.split('.')
        try:
            year = int(date_list[2])
            year_now = int(datetime.date.today().year)
            return year_now - year
        except IndexError:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    write_msg(user_id, 'Введите ваш возраст: ')
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            age = event.text
                            if age == None or age == '':
                                break
                            else:
                                return age
                            # if age != '' or age != None:
                            #     return int(age)
                            # else:
                            #     break


def cities(user_id, city_name):
    url = url = f'https://api.vk.com/method/database.getCities'
    params = {'access_token': user_token,
              'country_id': 1,
              'q' : f'{city_name}',
              'need_all': 0,
              'count': 1000,
              'v': '5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    information_list = response['response']
    list_cities = information_list['items']
    for i in list_cities:
        found_city_name = i.get('title')
        if found_city_name == city_name:
            found_city_id = i.get('id')
            return int(found_city_id)


#print(cities('342034365', 'Брянск'))

# ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ГОРОДЕ ПОЛЬЗОВАТЕЛЯ
def find_city(user_id):
    #global id_city
    url = f'https://api.vk.com/method/users.get?fields=city'
    params = {'access_token': user_token,
              'user_ids': user_id,
              'v': '5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    information_dict = response['response']
    #return information_dict
    for i in information_dict:
        if 'city' in i:
            city = i.get('city')
            id = str(city.get('id'))
            return id
        elif 'city' not in i:
            write_msg(user_id, 'Ошибка получения города')
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    write_msg(user_id, 'Введите название вашего города: ')
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            city_name = event.text
                            id_city = cities(user_id, city_name)
                            if id_city != '' or id_city != None:
                                return str(id_city)
                            else:
                                break





find_city('342034365')
        # for key, value in i.items():
        #     if key == 'city':

        #         try:
        #             return id_city
        #         except UnboundLocalError:
        #             write_msg(user_id, 'Ошибка получения города')
        #             for event in longpoll.listen():
        #                 if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        #                     write_msg(user_id, 'Введите название вашего города: ')
        #                     for event in longpoll.listen():
        #                         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        #                             city_name = event.text
        #                             #global id_city
        #                             id_city = cities(user_id, city_name)
        #                             if id_city != '' or id_city != None:
        #                                 return str(id_city)
        #                             else:
        #                                 break

# ПОЛУЧЕНИЕ ID ГОРОДА ИЗ find_city()
# def city_id(user_id):  # SEARCHING ID CITY
#     dict = find_city(user_id)
#     try:
#         return str(dict.get('id'))
#     except AttributeError:
#         return find_city(user_id)



# ПОИСК ЧЕЛОВЕКА ПО ПОЛУЧЕННЫМ ДАННЫМ
def find_user(user_id):
    url = f'https://api.vk.com/method/users.search'
    params = {'access_token': user_token,
              'v': '5.131', 'sex': get_sex(user_id),
              'age_from': get_age(user_id),
              'age_to': get_age(user_id),
              'city': find_city(user_id),
              #'city': id_city,
              'fields': 'is_closed',
              'fields':'id',
              'fields': 'first_name',
              'fields': 'last_name',
              'status': '1' or '6',
              'count': 100}
    resp = requests.get(url, params=params)
    resp_json = resp.json()
    dict_1 = resp_json['response']
    list_1 = dict_1['items']
    information = []
    drop_users()
    drop_seen_users()
    create_table_users()
    create_table_seen_users()
    for person_dict in list_1:
        if person_dict.get('is_closed') == False:
            first_name = person_dict.get('first_name')
            last_name = person_dict.get('last_name')
            vk_id = str(person_dict.get('id'))
            vk_link = 'vk.com/id' + str(person_dict.get('id'))
            insert_data_users(first_name, last_name, vk_id, vk_link)
        else:
            continue
    return f'Поиск завершён'

# ПОЛУЧЕНИЕ ВСЕХ ID ФОТОГРАФИЙ ПОЛЬЗОВАТЕЛЯ
# СОРТИРОВКА ID ПО КОЛИЧЕСТВУ ЛАЙКОВ В ОБРАТНОМ ПОРЯДКЕ
def get_photos_id(user_id):
    url = 'https://api.vk.com/method/photos.getAll'
    params = {'access_token': user_token,
              'type':'album',
              'owner_id':user_id,
              'extended':1,
              'count':25,
              'v':'5.131'}
    resp = requests.get(url, params=params)
    dict_photos = dict()
    resp_json = resp.json()
    dict_1 = resp_json['response']
    list_1 = dict_1['items']
    for i in list_1:
        photo_id = str(i.get('id'))
        i_likes = i.get('likes')
        if i_likes.get('count'):
            likes = i_likes.get('count')
            dict_photos[likes] = photo_id
    list_of_ids = sorted(dict_photos.items(), reverse=True)
    return list_of_ids

# ПОЛУЧЕНИЕ ID ФОТОГРАФИИ, ИДЕНТИЧЕН 2 И 3 МЕТОДАМ
def get_photo_1(user_id):
    list = get_photos_id(user_id)
    count = 0
    for i in list:
        count += 1
        if count == 1:
            return i[1]

def get_photo_2(user_id):
    list = get_photos_id(user_id)
    count = 0
    for i in list:
        count += 1
        if count == 2:
            return i[1]

def get_photo_3(user_id):
    list = get_photos_id(user_id)
    count = 0
    for i in list:
        count += 1
        if count == 3:
            return i[1]


def found_person_info(offset):
    tuple = select(offset)
    list = []
    for i in tuple:
        list.append(i)
    return f'{list[0]} {list[1]}, ссылка - {list[3]}'

def found_vk_id(offset):
    tuple = select(offset)
    list = []
    for i in tuple:
        list.append(i)
    return f'{list[2]}'

def person_id(offset):
    tuple = select(offset)
    list = []
    for i in tuple:
        list.append(i)
    return str(list[2])
