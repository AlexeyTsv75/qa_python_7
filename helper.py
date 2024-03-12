import random
import string

import requests


def get_ten_random_string(wanted_length):
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string
    return generate_random_string(wanted_length)


def register_new_courier_and_return_login_password(wanted_length):
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = get_ten_random_string(wanted_length)
    password = get_ten_random_string(wanted_length)
    first_name = get_ten_random_string(wanted_length)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
    # возвращаем список
    return login_pass


def delete_courier(courier_existed):
    courier = courier_existed
    payload_delete = {"login": courier[0], "password": courier[1]}
    response_delete = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                    data=payload_delete)
    text_response_delete = response_delete.json()
    courier_id_delete = text_response_delete['id']
    del_payload_delete = {"id": courier_id_delete}
    requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id_delete}',
                    data=del_payload_delete)


def created_courier_login_and_delete(payload):
    courier_payload = {"login": payload["login"], "password": payload["password"]}
    courier_login = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                  data=courier_payload)
    cl = courier_login.json()
    courier_id = cl["id"]
    del_payload = {"id": courier_id}
    requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}',
                    data=del_payload)
