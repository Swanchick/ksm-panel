from utils import Settings
from engine import EngineConnector
from waitress import serve
from flask import Flask


class Panel:
    __host: str
    __port: int
    __engine_connector: EngineConnector
    __secret_key: str

    def __init__(self):
        settings = Settings().get()

        panel_settings = settings["panel"]
        self.__host = panel_settings["host"]
        self.__port = panel_settings["port"]

        engine_settings = settings["engine"]

        engine_host = engine_settings["host"]
        engine_port = engine_settings["port"]
        engine_password = engine_settings["password"]
        self.__secret_key = engine_settings["secret_key"]

        self.__engine_connector = EngineConnector(engine_host, engine_port, self.__secret_key, engine_password)

    def start(self, app: Flask):
        print("KSM Panel has been successfully started.")
        print(f"Running on http://{self.host}:{self.port}/")

        serve(app, host=self.__host, port=self.__port)

    @property
    def host(self) -> str:
        return self.__host

    @property
    def port(self) -> int:
        return self.__port

    @property
    def secret_key(self) -> str:
        return self.__secret_key

    @property
    def connector(self) -> EngineConnector:
        return self.__engine_connector
