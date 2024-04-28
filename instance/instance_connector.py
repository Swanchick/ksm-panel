from utils import Connector
from typing import Dict, Optional


class InstanceConnector(Connector):
    def __init__(self, host: str):
        super().__init__(host, "instance")

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

    def get_last_output(self, engine_password: str, user_key: str, instance_id: int) -> Optional[Dict]:
        response = self.send(
            engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "call",
            "get_last_output"
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

