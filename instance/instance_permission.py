from typing import Dict
from .permission import Permission


class InstancePermission:
    __user_permissions: Dict
    __all__permissions: Dict

    def __init__(self, user_permissions: Dict, all__permissions: Dict):
        self.__user_permissions = user_permissions
        self.__all__permissions = all__permissions

    def get_user_permissions(self):
        out = {}

        for user in self.__user_permissions:
            username = user["user"]["name"]
            user_id = user["user"]["user_id"]
            is_user_admin = user["user"]["is_administrator"]

            out[username] = []

            for permission in self.__all__permissions:
                activated = permission in user["permissions"]

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
