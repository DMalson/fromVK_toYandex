from vk import VK
from file_op import FileOp
import json
import time


if __name__ == '__main__':
    with open("Service/VK-service.txt", "r", encoding="utf-8") as ini_file:
        my_ini = json.load(ini_file)
        access_token = my_ini['vk_token']
        user_id = input("Введите ID пользователя VK для копирования фото: ")
        ya_token = input("Введите yandex-token для копирования файлов: ")
    my_vk = VK(access_token, user_id)
    # print(my_vk.users_info())

    vk_albums = my_vk.get_albums()
    # print(vk_photos)
    storage = FileOp(ya_token)
    for item in vk_albums['response']['items']:
        print(f"ID - {item['id']}, альбом - '{item['title']}'")
        vk_photos = my_vk.get_photos(item['id'])
        # pprint.pprint(vk_photos)
        if 'response' in vk_photos.keys():
            print(f"Фотографий - {vk_photos['response']['count']}")
            # storage.save_album(item['title'],vk_photos)
            storage.save_album_toYD(item['title'],vk_photos)
        else:
            print(f"Ошибка - {vk_photos['error']['error_code']} {vk_photos['error']['error_msg']}")
        time.sleep(0.1)