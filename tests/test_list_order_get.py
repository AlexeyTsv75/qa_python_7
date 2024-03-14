import requests


class TestListOrderGet:
    def test_order_list_budy_is_list_success(self):
        payload = {"limit": 5, "page": 0}
        response = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders', params=payload)
        code_response = response.status_code
        text_response = response.json()
        assert code_response == 200 and isinstance(text_response["orders"], list)
