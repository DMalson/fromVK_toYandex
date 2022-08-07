import requests
import json

class FileOp :

    def __init__(self,ya_token):
        self.ya_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.ya_token = ya_token
        self.ya_headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {ya_token}'}
        self.list_of_files = []

    def save_json(self):
        dest = requests.get(f"{self.ya_url + '/upload'}?path={'VK/photos.json'}&overwrite=True",
                            headers=self.ya_headers).json()
        requests.put(dest['href'], files={'file': json.dumps(self.list_of_files)})

    # Тестовый вариант - сохранение в файл
    # def save_album(self, album_name, album):
    #     if not os.path.exists('VK'):
    #         os.mkdir('VK')
    #     if not os.path.exists('VK/' + album_name):
    #         print('VK/' + album_name)
    #         os.mkdir('VK/' + album_name)
    #     for foto in album['response']['items']:
    #         filename = str(foto['id'])
    #         foto_url = list(sorted(foto['sizes'], key=lambda dict: dict['type'], reverse=True))[0]['url']
    #         r=requests.get(foto_url)
    #         with open('VK/' + album_name + '/' + filename + '.jpg', 'wb') as f:
    #             f.write(r.content)

    def save_album_toYD(self, album_name, album, num_photos = 5):
        # Создаём каталог на Яндекс.Диск
        requests.put(f"{self.ya_url}?path={'VK/' + album_name}", headers=self.ya_headers)
        # Формируем список фотографий с наибольшим разрешением из нескольких представлений в ВК.
        save_list = []
        for photo in album['response']['items']:
            photo_params = [str(photo['id']),str(photo['likes']['count'])]
            sorted_list = list(sorted(photo['sizes'], key=lambda dict: dict['type'], reverse=True))
            photo_params.append(sorted_list[0]['url'])
            photo_params.append(sorted_list[0]['width'] * sorted_list[0]['height'])
            photo_params.append(sorted_list[0]['type'])
            save_list.append(photo_params)
        # Обрабатываем список фотографий и сохраняем на Яндекс.Диск из альбома только num_photos с наибольшим разрешением
        for best_photo in sorted(save_list, key=lambda rec: rec[3])[:-num_photos - 1:-1]:
            source=requests.get(best_photo[2])
            filename = best_photo[1] + '_' + best_photo[0] + '.jpg'
            dest = requests.get(f"{self.ya_url + '/upload'}?path={'VK/' + album_name+ '/' + filename}&overwrite=True",
                                headers=self.ya_headers).json()
            requests.put(dest['href'], files={'file': source.content})
            self.list_of_files.append({"file_name" : filename, "size": best_photo[4]})
