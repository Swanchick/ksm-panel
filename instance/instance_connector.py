from utils import Connector


class InstanceConnector(Connector):
    def __init__(self, host: str):
        super().__init__(host, "instance")

    def get_instances(self, engine_password: str, user_key: str):
        return self.send(engine_password, user_key, "instance_data", {}, "instance", "get")


