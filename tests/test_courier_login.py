import requests
import random
import string
import data


def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

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


class TestCourierLogin:

    def test_courier_login_with_all_fields_success_and_return_id(self):
        new_courier = register_new_courier_and_return_login_password()
        payload = {"login": new_courier[0], "password": new_courier[1]}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        code_response = response.status_code
        text_response = response.json()
        courier_id = text_response['id']
        delete_courier(new_courier)
        assert code_response == 200 and isinstance(courier_id, int)

    def test_courier_login_with_incorrect_login_failed(self):
        new_courier = register_new_courier_and_return_login_password()
        payload = {"login": data.login, "password": new_courier[1]}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        code_response = response.status_code
        text_response = response.json()
        delete_courier(new_courier)
        assert code_response == 404 and text_response["message"] == "Учетная запись не найдена"

    def test_courier_login_with_incorrect_password_failed(self):
        new_courier = register_new_courier_and_return_login_password()
        payload = {"login": new_courier[0], "password": data.password}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        code_response = response.status_code
        text_response = response.json()
        delete_courier(new_courier)
        assert code_response == 404 and text_response["message"] == "Учетная запись не найдена"

    def test_courier_login_without_login_failed(self):
        new_courier = register_new_courier_and_return_login_password()
        payload = {"login": None, "password": new_courier[1]}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        code_response = response.status_code
        text_response = response.json()
        delete_courier(new_courier)
        assert code_response == 400 and text_response["message"] == "Недостаточно данных для входа"

    def test_courier_login_without_password_failed(self):
        new_courier = register_new_courier_and_return_login_password()
        payload = {"login": new_courier[0], "password": ""}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        code_response = response.status_code
        text_response = response.json()
        delete_courier(new_courier)
        assert code_response == 400 and text_response["message"] == "Недостаточно данных для входа"
