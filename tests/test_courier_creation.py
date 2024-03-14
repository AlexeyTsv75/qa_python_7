import pytest
import requests
import helper
import data


class TestCourierCreation:
    # тест пройден
    def test_courier_creation_with_all_data_success_with_correct_code_and_text(self):
        payload = {"login": helper.get_ten_random_string(data.needed_length),
                   "password": helper.get_ten_random_string(data.needed_length),
                   "firstName": helper.get_ten_random_string(data.needed_length)}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        code_response = response.status_code
        text_response = response.text
        helper.created_courier_login_and_delete(payload)
        assert code_response == 201 and text_response == '{"ok":true}'

    # тест не пройден. Ожидаемое тело ответа не соответствует фактическому
    def test_create_two_similar_courier_and_couriers_with_the_same_login_impossible(self):
        payload = {"login": helper.get_ten_random_string(data.needed_length),
                   "password": helper.get_ten_random_string(data.needed_length),
                   "firstName": helper.get_ten_random_string(data.needed_length)}
        requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        response_second = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        code_response = response_second.status_code
        text_response = response_second.text
        helper.created_courier_login_and_delete(payload)
        assert code_response == 409 and text_response == '{"message": "Этот логин уже используется"}', (
            f'Result is {code_response} but code is 409'
            f' and text is {text_response}, but text have to be = "message": "Этот логин уже используется"'
        )

    # тест пройден при создании курьера без пароля и без логина
    # тест не пройден при создании курьера без имени. ОР = курьер не создан, ФР = курьер создан
    @pytest.mark.parametrize('empty_field', ["login", "password", "firstName"])
    def test_creation_courier_without_required_field_impossible(self, empty_field):
        payload = {"login": helper.get_ten_random_string(data.needed_length),
                   "password": helper.get_ten_random_string(data.needed_length),
                   "firstName": helper.get_ten_random_string(data.needed_length)}
        payload[empty_field] = ""
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        code_response = response.status_code
        text_response = response.json()
        assert code_response == 400 and text_response["message"] == "Недостаточно данных для создания учетной записи"
