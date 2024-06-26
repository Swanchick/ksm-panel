from flask import Flask, render_template, request, redirect, session
from engine import InstancePermission
from panel import Panel


panel = Panel()

app = Flask(__name__)
app.secret_key = panel.secret_key


@app.route("/")
def main():
    if "user_key" not in session:
        return redirect("/login/")

    user_key = session["user_key"]

    response = panel.connector.get_instances(user_key)
    if response["status"] == 403:
        return redirect("/login/")

    instances = response["instances"] if response is not None else []

    return render_template("main.html", instances=instances)


@app.route("/instance/<instance_id>/")
def instance(instance_id: int):
    return redirect(f"/instance/{instance_id}/console/")


@app.route("/instance/")
def instance_blank():
    return redirect("/")


@app.route("/instance/<instance_id>/console/")
def instance_console(instance_id: int):
    if "user_key" not in session:
        return redirect("/")

    user_key = session["user_key"]
    response = panel.connector.get_instance(user_key, int(instance_id))

    if response["status"] == 403:
        return redirect("/")

    if response["status"] != 200:
        return redirect("/")

    return render_template("instance/console.html", instance_data=response["instance"])


@app.route("/instance/<instance_id>/permissions/")
def instance_permission(instance_id: int):
    if "user_key" not in session:
        return redirect(f"/instance/{instance_id}/")

    user_key = session["user_key"]

    user_permissions = panel.connector.get_user_permissions(user_key, int(instance_id))
    permissions = panel.connector.get_permissions(user_key)
    users = panel.connector.get_users(user_key)

    if user_permissions["status"] == 403 or permissions["status"] == 403 or user_permissions["status"] == 403:
        return redirect(f"/instance/{instance_id}/")

    instance_permission = InstancePermission(user_permissions["users"], permissions["permissions"], users["users"])

    return render_template(
        "instance/permissions.html",
        permissions=instance_permission.get_user_permissions(),
        instance_id=instance_id
    )


@app.route("/instance/<instance_id>/permissions/add/", methods=["POST"])
def instance_permission_add(instance_id: int):
    if "user_key" not in session:
        return {}

    user_key = session["user_key"]

    data = request.json
    user_id = data["user_id"]
    permission_id = int(data["permission_id"])

    response = panel.connector.add_permission(user_key, instance_id, user_id, permission_id)

    if response["status"] != 200:
        return redirect("/")

    return response


@app.route("/instance/<instance_id>/permissions/remove/", methods=["POST"])
def instance_permission_remove(instance_id: int):
    if "user_key" not in session:
        return {}

    user_key = session["user_key"]

    data = request.json
    user_id = data["user_id"]
    permission_id = int(data["permission_id"])

    response = panel.connector.remove_permission(user_key, instance_id, user_id, permission_id)

    if response["status"] != 200:
        return redirect("/")

    return response


@app.route("/instance/<instance_id>/call/get_output/")
def instance_get_output(instance_id: int):
    if "user_key" not in session:
        return {}

    user_key = session["user_key"]

    response = panel.connector.get_output(user_key, int(instance_id))

    if response["status"] != 200:
        return redirect("/")

    return response


@app.route("/instance/<instance_id>/call/server_send/", methods=["POST"])
def instance_send_server(instance_id: int):
    if request.method != "POST":
        return "Method not allowed", 405

    if "user_key" not in session:
        return {}

    user_key = session["user_key"]

    data = request.json
    command = data["command"]

    response = panel.connector.send_command(user_key, int(instance_id), command)

    return response


@app.route("/instance/<instance_id>/call/start_server/")
def instance_start_server(instance_id: int):
    if "user_key" not in session:
        return {}

    user_key = session["user_key"]

    response = panel.connector.start_instance(user_key, int(instance_id))

    return response


@app.route("/instance/<instance_id>/call/stop_server/")
def instance_stop_server(instance_id: int):
    if "user_key" not in session:
        return {}

    user_key = session["user_key"]

    response = panel.connector.stop_instance(user_key, int(instance_id))

    return response


@app.route("/login/", methods=["GET", "POST"])
def authorization():
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        
        response = panel.connector.user_authorization(username, password)

        if response["status"] == 200:
            user_key = response["key"]
            session["user_key"] = user_key

            return redirect("/")

    return render_template("login.html")


@app.route("/instance/create/", methods=["GET", "POST"])
def create_instance():
    if "user_key" not in session:
        return redirect("/")

    user_key = session["user_key"]
    response = panel.connector.get_user(user_key)
    if response["status"] != 200:
        return redirect("/")

    if not response["user"]["is_administrator"]:
        return redirect("/")

    if request.method == "POST":
        form = request.form
        instance_name = form.get("instance_name")
        instance_docker_image = form.get("instance_docker_image")
        panel.connector.create_instance(user_key, instance_name, instance_docker_image)

        return redirect("/")

    return render_template("instance_editor.html")


@app.route("/instance/<instance_id>/folders/", methods=["GET", "POST"])
def instance_folder(instance_id: int):
    if "user_key" not in session:
        return redirect(f"/instance/{instance_id}/")

    user_key = session["user_key"]
    args = request.args

    if "path" not in args:
        return redirect(f"/instance/{instance_id}/")

    path = args.get("path")

    folder_path = [] if path == "/" or path == "" else path.split("/")

    if ".." in folder_path:
        banned_folders = ["", "..", "."]
        for folder in banned_folders:
            while folder in folder_path:
                folder_path.remove(folder)

        path = "/".join(folder_path[:-1])
        last_slash = "/" if len(folder_path) != 0 else ""

        return redirect(
            f"/instance/{instance_id}/folders/?path=/{path}{last_slash}"
        )

    if request.method == "POST":
        data = request.json
        method = data["method"]
        name = data["name"]

        response = {}

        if method == "file":
            response = panel.connector.create_file(user_key, instance_id, name, folder_path)
        elif method == "folder":
            response = panel.connector.create_folder(user_key, instance_id, name, folder_path)
        elif method == "remove":
            print("Hello World")
            t = data["type"].split("/")[-1]

            if t == "file":
                response = panel.connector.delete_file(user_key, instance_id, name, folder_path)
            elif t == "folder":
                response = panel.connector.delete_folder(user_key, instance_id, name, folder_path)

        return response, 200

    response = panel.connector.get_folders(user_key, int(instance_id), folder_path)
    if response["status"] != 200:
        return redirect(f"/instance/{instance_id}/")

    folders = response["folders"]

    return render_template(
        "instance/folders.html",
        instance_id=instance_id,
        folders=folders,
        folder_path=folder_path,
    )


@app.route("/instance/<instance_id>/file/<file_name>/", methods=["GET", "POST"])
def instance_file(instance_id: int, file_name: str):
    if "user_key" not in session:
        return redirect(f"/instance/{instance_id}/")

    user_key = session["user_key"]

    path = request.args.get("path")
    folder_path = path.split("/")

    banned_folders = ["", "..", "."]
    for folder in banned_folders:
        while folder in folder_path:
            folder_path.remove(folder)

    if request.method == "POST":
        data = request.json
        file_data = data["file_data"]

        response = panel.connector.write_file(user_key, int(instance_id), folder_path, file_name, file_data)

        return response

    response = panel.connector.open_file(user_key, int(instance_id), file_name, folder_path)

    if response["status"] != 200:
        return redirect(f"/instance/{instance_id}/")

    return render_template(
        "instance/file.html",
        path=path,
        file=response["message"],
        file_name=file_name,
        instance_id=instance_id
    )


@app.route("/user/create/", methods=["GET", "POST"])
def user_create():
    if "user_key" not in session:
        return redirect("/")

    user_key = session["user_key"]
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        is_admin = (form["is_admin"] == "on") if "is_admin" in form else False

        if username != "" and password != "":
            response = panel.connector.create_user(user_key, username, password, is_admin)
            if response["status"] == 200:
                return redirect("/")

    return render_template("user.html")


@app.route("/settings/")
def settings():
    if "user_key" not in session:
        return redirect("/")

    user_key = session["user_key"]
    response = panel.connector.get_user(user_key)
    if response["status"] != 200:
        return redirect("/")

    if not response["user"]["is_administrator"]:
        return redirect("/")

    response = panel.connector.get_ports(user_key)
    if response["status"] != 200:
        return redirect("/")

    print(response)

    ports = response["ports"]

    return render_template("settings.html", ports=ports, enumerate=enumerate)


@app.route("/instance/<instance_id>/settings/")
def instance_settings(instance_id):
    if "user_key" not in session:
        return redirect("/")

    user_key = session["user_key"]

    response_arguments = panel.connector.get_arguments(user_key, instance_id)
    arguments = response_arguments["arguments"]

    response_port = panel.connector.get_port(user_key, instance_id)
    port = response_port["port"]

    response_ports = panel.connector.get_ports(user_key)
    ports = response_ports["ports"]

    return render_template(
        "instance/settings.html",
        instance_id=instance_id,
        arguments=arguments,
        enumerate=enumerate,
        port=port,
        ports=ports
    )


@app.route("/instance/<instance_id>/call/add_argument/", methods=["POST"])
def add_argument(instance_id: int):
    if "user_key" not in session:
        return {}

    user_key = session["user_key"]

    data = request.json
    argument = data["argument"]

    if argument is None or argument == "":
        return {}

    response = panel.connector.add_argument(user_key, instance_id, argument)

    print(response)

    return response


@app.route("/instance/<instance_id>/call/delete_argument/", methods=["POST"])
def delete_argument(instance_id: int):
    if "user_key" not in session:
        return {}

    data = request.json
    argument_id = data["argument_id"]

    user_key = session["user_key"]

    response = panel.connector.delete_argument(user_key, instance_id, argument_id)

    return response


@app.route("/instance/<instance_id>/call/change_port/", methods=["POST"])
def change_port(instance_id: int):
    if "user_key" not in session:
        return {}

    data = request.json
    port = data["port"]

    user_key = session["user_key"]

    response = panel.connector.change_port(user_key, instance_id, port)

    return response


@app.route("/settings/call/unpin_port/", methods=["POST"])
def unpin_port():
    if "user_key" not in session:
        return {}

    data = request.json
    port = data["port"]

    user_key = session["user_key"]

    response = panel.connector.unpin_port(user_key, port)

    return response


@app.route("/settings/call/delete_port/", methods=["POST"])
def delete_port():
    if "user_key" not in session:
        return {}

    data = request.json
    port = data["port"]

    user_key = session["user_key"]

    response = panel.connector.delete_port(user_key, port)

    return response


@app.route("/settings/call/add_port/", methods=["POST"])
def add_port():
    if "user_key" not in session:
        return {}

    data = request.json
    port = data["port"]

    user_key = session["user_key"]

    response = panel.connector.add_port(user_key, port)

    return response


if __name__ == "__main__":
    app.run(debug=True)

    # panel.start(app)
