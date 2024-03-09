import pytest
import requests

import data


class TestCourierCreation:
    # тест пройден
    def test_courier_creation_with_all_data_success_with_correct_code_and_text(self):
        payload = {"login": data.login, "password": data.password, "firstName": data.first_name}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        code_response = response.status_code
        text_response = response.text
        courier_payload = {"login": payload["login"], "password": payload["password"]}
        courier_login = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                      data=courier_payload)
        cl = courier_login.json()
        courier_id = cl["id"]
        del_payload = {"id": courier_id}
        requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}',
                        data=del_payload)
        assert code_response == 201 and text_response == '{"ok":true}'

    # тест не пройден. Ожидаемое тело ответа не соответствует фактическому
    def test_create_two_similar_courier_and_couriers_with_the_same_login_impossible(self):
        payload = {"login": data.login, "password": data.password, "firstName": data.first_name}
        requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        response_second = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        code_response = response_second.status_code
        text_response = response_second.text
        courier_payload = {"login": payload["login"], "password": payload["password"]}
        courier_login = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                      data=courier_payload)
        cl = courier_login.json()
        courier_id = cl["id"]
        del_payload = {"id": courier_id}
        requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}',
                        data=del_payload)
        assert code_response == 409 and text_response == '{"message": "Этот логин уже используется"}', (
            f'Result is {code_response} but code is 409'
            f' and text is {text_response}, but text have to be = "message": "Этот логин уже используется"'
        )

    # тест пройден при создании курьера без пароля и без логина
    # тест не пройден при создании курьера без имени. ОР = курьер не создан, ФР = курьер создан
    @pytest.mark.parametrize('empty_field', ["login", "password", "firstName"])
    def test_creation_courier_without_required_field_impossible(self, empty_field):
        payload = {"login": data.login, "password": data.password, "firstName": data.first_name}
        payload[empty_field] = ""
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        code_response = response.status_code
        text_response = response.json()
        assert code_response == 400 and text_response["message"] == "Недостаточно данных для создания учетной записи"
