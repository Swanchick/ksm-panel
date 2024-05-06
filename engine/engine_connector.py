from utils import Connector
from typing import Dict, Optional, List


class EngineConnector(Connector):
    __engine_password: str

    def __init__(self, host: str, port: int, secret_key: str, engine_password: str):
        super().__init__(host, port, secret_key)

        self.__engine_password = engine_password

    def get_instances(self, user_key: str) -> Optional[Dict]:
        response = self.send(self.__engine_password, user_key, "instance_data", {}, "instance", "get")

        return response

    def get_instance(self, user_key: str, instance_id: int) -> Optional[Dict]:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "get_instance"
        )

        return response

    def get_instance_types(self):
        response = self.send(
            self.__engine_password,
            "",
            "instance_types",
            {},
            "instance",
            "types"
        )

        return response

    def create_instance(self, user_key: str, instance_name: str, instance_type: str) -> Optional[Dict]:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {"name": instance_name, "instance_type": instance_type},
            "instance",
            "create"
        )

        return response

    def get_output(self, user_key: str, instance_id: int) -> Optional[Dict]:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "call",
            "get_output"
        )

        return response

    def get_permissions(self, user_key: str) -> Optional[Dict]:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {},
            "permission",
            "get"
        )

        return response

    def get_user_permissions(self, user_key: str, instance_id: int) -> Optional[Dict]:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "call",
            "get_permissions"
        )

        return response

    def send_command(self, user_key: str, instance_id: int, command: str) -> Optional[Dict]:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id, "args": [command]},
            "instance",
            "call",
            "server_send"
        )

        return response

    def start_instance(self, user_key: str, instance_id: int) -> Optional[Dict]:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "call",
            "server_start"
        )

        return response

    def stop_instance(self, user_key: str, instance_id: int) -> Optional[Dict]:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "call",
            "server_stop"
        )

        return response

    def add_permission(self, user_key: str, instance_id: int, user_id: int, permission: int) -> Dict:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id, "args": [user_id, permission]},
            "instance",
            "call",
            "add_permission"
        )

        return response

    def remove_permission(self, user_key: str, instance_id: int, user_id: int, permission: int) -> Dict:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id, "args": [user_id, permission]},
            "instance",
            "call",
            "remove_permission"
        )

        return response

    def get_users(self, user_key: str) -> Optional[Dict]:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {},
            "user",
            "get"
        )

        return response

    def get_user(self, user_key: str) -> Dict:
        response = self.send(
            self.__engine_password,
            user_key,
            "",
            {},
            "user",
            "get_user"
        )

        return response

    def user_authorization(self, username: str, password: str) -> Dict:
        response = self.send(
            self.__engine_password,
            "",
            "user_data",
            {
                "name": username,
                "password": password
            },
            "user",
            "authorization"
        )

        return response

    def get_folders(self, user_key: str, instance_id: int, folder_path: List[str]) -> Dict:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id, "args": folder_path},
            "instance",
            "call",
            "get_folders"
        )

        return response

    def open_file(self, user_key: str, instance_id: int, file_path: List[str], file_name: str) -> Dict:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id, "args": file_path + [file_name]},
            "instance",
            "call",
            "open_file"
        )

        return response

    def write_file(self, user_key: str, instance_id: int, file_path: List[str], file_name: str, file_data: str) -> Dict:
        response = self.send(
            self.__engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id, "args": [file_name, file_data] + file_path},
            "instance",
            "call",
            "write_file"
        )

        return response

    def create_user(self, user_key: str, user_name: str, password: str, administrator: bool) -> Dict:
        response = self.send(
            self.__engine_password,
            user_key,
            "user_data",
            {
                "name": user_name,
                "password": password,
                "administrator": administrator
            },
            "user",
            "create"
        )

        return response
