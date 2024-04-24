from utils import Connector


class InstanceConnector(Connector):
    def __init__(self, host: str):
        super().__init__(host, "instance")

    def get_instances(self):
        self.send()


