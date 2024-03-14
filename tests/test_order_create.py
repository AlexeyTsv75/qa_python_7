import json

import pytest
import requests


class TestOrderCreate:
    @pytest.mark.parametrize('colour', [["BLACK"], ["GRAY"], ["BLACK", "GRAY"], []])
    def test_order_create_accord_to_color_success_and_return_track(self, colour):
        payload = {
                    "firstName": "Naruto",
                    "lastName": "Uchiha",
                    "address": "Konoha, 142 apt.",
                    "metroStation": 4,
                    "phone": "+7 800 355 35 35",
                    "rentTime": 5,
                    "deliveryDate": "2024-03-16",
                    "comment": "Saske, come back to Konoha",
                    "color": colour
                  }
        payload_string = json.dumps(payload)
        headers = {"Content-type": "application/json"}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', data=payload_string,
                                 headers=headers)
        code_response = response.status_code
        text_response = response.json()
        track = text_response['track']
        requests.put(f'https://qa-scooter.praktikum-services.ru/api/v1/orders/cancel?track={track}')
        assert code_response == 201 and isinstance(track, int)
