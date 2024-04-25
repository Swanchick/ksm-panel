from utils import Connector
from typing import Dict


class InstanceConnector(Connector):
    def __init__(self, host: str):
        super().__init__(host, "instance")

    def get_instances(self, engine_password: str, user_key: str) -> Dict:
        return self.send(engine_password, user_key, "instance_data", {}, "instance", "get")

    def get_instance(self, engine_password: str, user_key: str, instance_id: int) -> Dict:
        return self.send(
            engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "get_instance"
        )

    def get_output(self, engine_password: str, user_key: str, instance_id: int) -> Dict:
        return self.send(
            engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "call",
            "get_output"
        )

    def start_instance(self, engine_password: str, user_key: str, instance_id: int) -> Dict:
        return self.send(
            engine_password,
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "call",
            "server_start"
        )

    def stop_instance(self, engine_password: str, user_key: str, instance_id: int) -> Dict:
        return self.send(
            engine_password, 
            user_key,
            "instance_data",
            {"instance_id": instance_id},
            "instance",
            "call",
            "server_stop"
        )

