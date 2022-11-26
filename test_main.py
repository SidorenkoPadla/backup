import requests
import json
import os

class User():
    def __init__(self, polygon_token, vk_id):
        self.vk_id = vk_id
        self.headers = {
            'Authorization': polygon_token,
            'Content-Type': 'application/json'
        }

    def res_vk(self): #Метод для получения списка ссылок на фото
        with open('Token.txt', 'r', encoding= 'utf-8') as token:
            URL = 'https://api.vk.com/method/photos.get'
            params = {
            'access_token': token.read(),
            'owner_id': self.vk_id,
            'album_id': 'profile',
            'v': '5.131',
            'extended': '1'
        }  # Параметры запроса
            self.res = requests.get(URL, params=params)
        return
    def photo_list(self):
        self.photos_list = {}
        self.photo_json = []
        count = 0
        count_limit = int(input('Введите количество фотографий для загрузки:\n'))
        for number in range(len(self.res.json()['response']['items'])):
            if self.res.json()['response']['items'][number]['likes']['count'] in self.photos_list:
                self.photos_list[self.res.json()['response']['items'][number]['date']] = self.res.json()['response']['items'][number]['sizes'][-1]['url']
                self.photo_json.append({
                    'file_name' : f"{self.res.json()['response']['items'][number]['date']}.jpg",
                    'size' : self.res.json()['response']['items'][number]['sizes'][-1]['type']
                })
                count += 1
                if count == count_limit:
                    break
            else:
                self.photos_list[self.res.json()['response']['items'][number]['likes']['count']] = self.res.json()['response']['items'][number]['sizes'][-1]['url']
                self.photo_json.append({
                    'file_name': f"{self.res.json()['response']['items'][number]['likes']['count']}.jpg",
                    'size': self.res.json()['response']['items'][number]['sizes'][-1]['type']
                })
                count += 1
                if count == count_limit:
                    break
    def create_folder(self):#Создаем папку
        self.name_folder = input('Введите название папки:\n')
        requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers= self.headers, params= {'path': self.name_folder})

    def upload_yandex(self):
        count = 0
        self.url_upload = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers= self.headers, params={'path': f'/{self.name_folder}', 'overwrite' : True} )
        for photo in self.photos_list:
            requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', headers= self.headers, params={'path': f'/{self.name_folder}/{photo}.png', 'url': self.photos_list.get(photo), 'overwrite' : True})
            count +=1
            print(f'Количество загруженных фотографий: {count}')

    def json_photo(self):
        self.name_file = input('Введите название папки: \n')
        with open(f'{self.name_file}.json', 'w') as photo_file:
            json.dump(self.photo_json, photo_file, ensure_ascii= False, indent= 4)





polygon_token = input(f'Введите токен:\n',)
vk_id = input(f'Введите id своего аккаунта вконтакте:\n')
user = User(polygon_token, vk_id)
user.res_vk()
user.photo_list()
user.create_folder()
user.upload_yandex()
user.json_photo()
print(f'https://disk.yandex.ru/client/disk/{user.name_folder}')
print(os.path.abspath(user.name_file))




