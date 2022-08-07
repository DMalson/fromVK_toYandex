from vk import VK
from file_op import FileOp
import json
import time
import PySimpleGUI as sg

if __name__ == '__main__':
    # Вводим исходные данные
    with open("Service/VK-service.txt", "r", encoding="utf-8") as ini_file:
        my_ini = json.load(ini_file)
        access_token = my_ini['vk_token']
        # user_id = my_ini['vk_id']
        # ya_token = my_ini['yandex_token']
        user_id = input("Введите ID пользователя VK для копирования фото: ")
        ya_token = input("Введите yandex-token для копирования файлов: ")
    # Подключаемся к ВК и получаем список альбомов
    my_vk = VK(access_token, user_id)
    vk_albums = my_vk.get_albums()['response']['items']
    # albums_list = [album['id'] for album in vk_albums['response']['items']]
    print(f"У пользователя {len(vk_albums)} альбомов с фотографиями.")
    # Устанавливаем лимит фотографий из альбома на загрузку
    num_fotos = input("Введите количество фото для сохранения: ")
    # Создаём экземпляр класса для сохранения фотографий
    storage = FileOp(ya_token)
    # Перебираем альбомы и пытаемся сохранить фотографии в пределах лимита на Яндекс.Диске
    for i, item in enumerate(vk_albums):
        vk_photos = my_vk.get_photos(item['id'])
        sg.one_line_progress_meter('Подождите...', i + 1, len(vk_albums), 'Скопировано альбомов')
        if 'response' in vk_photos.keys():
            storage.save_album_toYD(item['title'],vk_photos)
        else:
            print(f"Ошибка - {vk_photos['error']['error_code']} {vk_photos['error']['error_msg']}")
        time.sleep(0.1)
    storage.save_json()