from requests import post
from typing import Tuple, Dict, Optional
from abc import ABC


class Connector(ABC):
    __host: str
    __route: str

    def __init__(self, host: str, route: str):
        self.__host = host
        self.__route = route

    def __build_route(self, methods: Tuple[str, ...]):
        return f"http://{self.__host}/api/{"/".join(methods)}"

    def send(self, engine_password: str, user_key: str, data_name: str, data: dict, *methods: str) -> Optional[Dict]:
        url = self.__build_route(methods)

        headers = {
            "Content-Type": "application/json"
        }

        final_data = {
            "password": engine_password,
            "user_key": user_key,
            data_name: data
        }

        try:
            response = post(url, headers=headers, json=final_data)

            if response.status_code != 200:
                return None

            return response.json()
        except Exception as e:
            print(e)

            return None


