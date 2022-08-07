import requests

class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

   def get_albums(self, need_system=True):
       url = 'https://api.vk.com/method/photos.getAlbums'
       params = {'owner_id': self.id, "need_system": need_system}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

   def get_photos(self, album_id):
       url = 'https://api.vk.com/method/photos.get'
       params = {'owner_id': self.id, "album_id": album_id, "extended": 1}
       response = requests.get(url, params={**self.params, **params})
       return response.json()




