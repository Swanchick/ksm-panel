from typing import Dict, List
from .permission import Permission


class InstancePermission:
    __user_permissions: Dict
    __all_permissions: Dict
    __all_users: Dict

    def __init__(self, user_permissions: Dict, all_permissions: Dict, all_users: Dict):
        self.__user_permissions = user_permissions
        self.__all_permissions = all_permissions
        self.__all_users = all_users

    def __get_permissions(self, user_id: int) -> Dict:
        for user_permission in self.__user_permissions:
            if user_id == user_permission["user_id"]:

                return user_permission["permissions"]

    def get_user_permissions(self) -> Dict[str, List[Permission]]:
        out = {}

        for user in self.__all_users:
            username = user["name"]
            user_id = user["user_id"]
            is_user_admin = user["is_administrator"]

            out[username] = []

            for permission in self.__all_permissions:
                activated = False
                user_permission = self.__get_permissions(user_id)

                if user_permission is not None:
                    activated = permission in user_permission

                permission_name = list(permission.keys())[0]
                permission_value = list(permission.values())[0]

                permission_object = Permission(
                    permission_name,
                    permission_value,
                    activated,
                    username,
                    user_id,
                    is_user_admin
                )

                out[username].append(permission_object)

        return out
