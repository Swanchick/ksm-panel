class Permission:
    __name: str
    __permission: int
    __activated: bool

    __username: str
    __user_id: int
    __is_administrator: bool

    def __init__(self, name: str, permission: int, activated: bool, username: str, user_id: int, is_admin: bool):
        self.__name = name
        self.__permission = permission
        self.__activated = activated

        self.__username = username
        self.__user_id = user_id
        self.__is_administrator = is_admin

    @property
    def name(self) -> str:
        return self.__name

    @property
    def permission(self) -> int:
        return self.__permission

    @property
    def activated(self):
        return self.__activated

    @property
    def username(self) -> str:
        return self.__username

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def is_administrator(self) -> bool:
        return self.__is_administrator
