from requests import post
from typing import Tuple, Dict, Optional
from abc import ABC
from json import loads, dumps
from base64 import b64encode, b64decode
from cryptography.fernet import Fernet


class Connector(ABC):
    __host: str
    __port: int
    __secret_key: str

    def __init__(self, host: str, port: int, secret_key: str):
        self.__host = host
        self.__port = port
        self.__secret_key = secret_key

        self.__cryptography = Fernet(self.__secret_key)

    def __encrypt_data(self, data: Dict) -> Dict:
        json = dumps(data)
        encrypted_json = self.__cryptography.encrypt(json.encode())
        bs64 = b64encode(encrypted_json)

        return {"data": bs64.decode()}

    def __decrypt_data(self, data: str) -> Dict:
        encrypted_data = b64decode(data)
        decrypted_json = self.__cryptography.decrypt(encrypted_data)

        return loads(decrypted_json)

    def __build_route(self, methods: Tuple[str, ...]):
        route = "/".join(methods)

        return f"http://{self.__host}:{self.__port}/api/{route}"

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

        encrypted_data = self.__encrypt_data(final_data)

        try:
            response = post(url, headers=headers, json=encrypted_data)

            if response.status_code != 200:
                return None

            encrypted_data = response.text
            decrypted_data = self.__decrypt_data(encrypted_data)

            return decrypted_data

        except Exception as e:
            print(e)
