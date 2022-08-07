import os
import requests

class FileOp :

    def __init__(self,ya_token):
        self.ya_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.ya_token = ya_token
        self.ya_headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {ya_token}'}

    def save_album(self, album_name, album):
        if not os.path.exists('VK'):
            os.mkdir('VK')
        if not os.path.exists('VK/' + album_name):
            print('VK/' + album_name)
            os.mkdir('VK/' + album_name)
        for foto in album['response']['items']:
            filename = str(foto['id'])
            foto_url = list(sorted(foto['sizes'], key=lambda dict: dict['type'], reverse=True))[0]['url']
            r=requests.get(foto_url)
            with open('VK/' + album_name + '/' + filename + '.jpg', 'wb') as f:
                f.write(r.content)

    def save_album_toYD(self, album_name, album):
        requests.put(f"{self.ya_url}?path={'VK/' + album_name}", headers=self.ya_headers)
        # print(r.status_code)
        for foto in album['response']['items']:
            filename = str(foto['id'])
            foto_url = list(sorted(foto['sizes'], key=lambda dict: dict['type'], reverse=True))[0]['url']
            source=requests.get(foto_url)
            dest = requests.get(f"{self.ya_url + '/upload'}?path={'VK/' + album_name+ '/' + filename}&overwrite=True",
                               headers=self.ya_headers).json()
            print(dest)
            res=requests.put(dest['href'], files={'file': source.content})

