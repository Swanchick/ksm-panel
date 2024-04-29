from utils import Connector
from typing import Dict, Optional


class EngineConnector(Connector):
    def __init__(self, host: str):
        super().__init__(host)

    def get_instances(self, engine_password: str, user_key: str) -> Optional[Dict]:
        response = self.send(engine_password, user_key, "instance_data", {}, "instance", "get")

        return response

    def get_instance(self, engine_password: str, user_key: str, instance_id: int) -> Optional[Dict]:
        response = self.send(
            engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "get_instance"
        )

        return response

    def get_output(self, engine_password: str, user_key: str, instance_id: int) -> Optional[Dict]:
        response = self.send(
            engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "call",
            "get_output"
        )

        return response

    def get_permissions(self, engine_password: str, user_key: str) -> Optional[Dict]:
        response = self.send(
            engine_password,
            user_key,
            "instance_data",
            {},
            "permission",
            "get"
        )

        return response

    def get_user_permissions(self, engine_password: str, user_key: str, instance_id: int) -> Optional[Dict]:
        response = self.send(
            engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "call",
            "get_permissions"
        )

        return response

    def send_command(self, engine_password: str, user_key: str, instance_id: int, command: str) -> Optional[Dict]:
        response = self.send(
            engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id, "args": [command]},
            "instance",
            "call",
            "server_send"
        )

        return response

    def start_instance(self, engine_password: str, user_key: str, instance_id: int) -> Optional[Dict]:
        response = self.send(
            engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "call",
            "server_start"
        )

        return response

    def stop_instance(self, engine_password: str, user_key: str, instance_id: int) -> Optional[Dict]:
        response = self.send(
            engine_password, 
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "call",
            "server_stop"
        )

        return response

    def add_permission(self, engine_password: str, user_key: str, instance_id: int, user_id: int, permission: int) -> Dict:
        response = self.send(
            engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id, "args": [user_id, permission]},
            "instance",
            "call",
            "add_permission"
        )

        return response

    def remove_permission(self, engine_password: str, user_key: str, instance_id: int, user_id: int, permission: int) -> Dict:
        response = self.send(
            engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id, "args": [user_id, permission]},
            "instance",
            "call",
            "remove_permission"
        )

        return response

    def get_users(self, engine_password: str, user_key: str) -> Optional[Dict]:
        response = self.send(
            engine_password,
            user_key,
            "instance_data",
            {},
            "user",
            "get"
        )

        return response
