from .json_reader import JsonReader


class Settings:
    __settings_path: str

    def __init__(self, path: str = "settings.json"):
        self.__settings_path = path

    def get(self):
        json_reader = JsonReader(self.__settings_path)
        return json_reader.read()
