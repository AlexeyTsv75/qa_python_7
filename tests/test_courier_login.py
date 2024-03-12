import requests
import data
import helper


class TestCourierLogin:

    def test_courier_login_with_all_fields_success_and_return_id(self):
        new_courier = helper.register_new_courier_and_return_login_password(data.needed_length)
        payload = {"login": new_courier[0], "password": new_courier[1]}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        code_response = response.status_code
        text_response = response.json()
        courier_id = text_response['id']
        helper.delete_courier(new_courier)
        assert code_response == 200 and isinstance(courier_id, int)

    def test_courier_login_with_incorrect_login_failed(self):
        new_courier = helper.register_new_courier_and_return_login_password(data.needed_length)
        payload = {"login": helper.get_ten_random_string(data.needed_length), "password": new_courier[1]}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        code_response = response.status_code
        text_response = response.json()
        helper.delete_courier(new_courier)
        assert code_response == 404 and text_response["message"] == "Учетная запись не найдена"

    def test_courier_login_with_incorrect_password_failed(self):
        new_courier = helper.register_new_courier_and_return_login_password(data.needed_length)
        payload = {"login": new_courier[0], "password": helper.get_ten_random_string(data.needed_length)}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        code_response = response.status_code
        text_response = response.json()
        helper.delete_courier(new_courier)
        assert code_response == 404 and text_response["message"] == "Учетная запись не найдена"

    def test_courier_login_without_login_failed(self):
        new_courier = helper.register_new_courier_and_return_login_password(data.needed_length)
        payload = {"login": None, "password": new_courier[1]}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        code_response = response.status_code
        text_response = response.json()
        helper.delete_courier(new_courier)
        assert code_response == 400 and text_response["message"] == "Недостаточно данных для входа"

    def test_courier_login_without_password_failed(self):
        new_courier = helper.register_new_courier_and_return_login_password(data.needed_length)
        payload = {"login": new_courier[0], "password": ""}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        code_response = response.status_code
        text_response = response.json()
        helper.delete_courier(new_courier)
        assert code_response == 400 and text_response["message"] == "Недостаточно данных для входа"
