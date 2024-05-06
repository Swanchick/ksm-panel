from flask import Flask, render_template, request, redirect, session
from engine import EngineConnector, InstancePermission
from panel import Panel


panel = Panel()

app = Flask(__name__)
app.secret_key = panel.secret_key


@app.route("/")
def index():
    if "user_key" not in session:
        return redirect("/login/")

    user_key = session["user_key"]

    response = panel.connector.get_instances(user_key)
    if response["status"] == 403:
        return redirect("/login/")

    instances = response["instances"] if response is not None else []

    return render_template("index.html", instances=instances)


@app.route("/instance/<instance_id>/")
def instance(instance_id: int):
    if "user_key" not in session:
        return redirect("/")

    response = panel.connector.get_instance("debug", int(instance_id))
    if response["status"] == 403:
        return redirect("/")

    return render_template("instance/instance.html", instance_data=response["instance_data"])


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

    return response


@app.route("/instance/<instance_id>/call/get_output/")
def instance_get_output(instance_id: int):
    if "user_key" not in session:
        return {}

    user_key = session["user_key"]

    response = panel.connector.get_output(user_key, int(instance_id))

    return response


@app.route("/instance/<instance_id>/call/server_send/", methods=["POST"])
def instance_send_server(instance_id: int):
    if request.method != "POST":
        return "Method not allowed", 405

    if "user_key" not in session:
        return {}

    data = request.json
    command = data["command"]

    response = panel.connector.send_command("debug", int(instance_id), command)

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

    response = panel.connector.stop_instance("debug", int(instance_id))

    return response


@app.route("/login/", methods=["GET", "POST"])
def authorization():
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        
        response = panel.connector.user_authorization(username, password)

        if response["status"] == 200:
            user_key = response["user_data"]["key"]
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

    user = response["user"]

    if user["is_administrator"] is False:
        return redirect("/")

    instance_types = panel.connector.get_instance_types()

    if request.method == "POST":
        form = request.form

        instance_name = form.get("instance_name")
        if instance_name != "":
            instance_type = form.get("instance_type")

            response = panel.connector.create_instance(user_key, instance_name, instance_type)
            print(response)

            if response["status"] == 200:
                return redirect("/")

    return render_template("instance_editor.html", instance_types=instance_types["instance_types"])


@app.route("/instance/<instance_id>/folders/", methods=["GET", "POST"])
def instance_folder(instance_id: int):
    if "user_key" not in session:
        return redirect(f"/instance/{instance_id}/")

    user_key = session["user_key"]
    folder_path = []

    is_post = request.method == "POST"

    if is_post:
        data = request.json

        folder_path = data["current_folder"]
        folder_name = data["folder"]
        if folder_name != "":
            if folder_name == "..":
                if len(folder_path) > 0:
                    folder_path.pop()
            else:
                folder_path.append(folder_name)

    response = panel.connector.get_folders(user_key, int(instance_id), folder_path)
    if response["status"] != 200:
        return redirect(f"/instance/{instance_id}/")

    folders = response["folders"]

    if is_post:
        return {"folder": folder_path, "data": response}

    return render_template("instance/folders.html", instance_id=instance_id, folders=folders, folder=folder_path)


@app.route("/instance/<instance_id>/file/<file_name>/", methods=["GET", "POST"])
def instance_file(instance_id: int, file_name: str):
    if "user_key" not in session:
        return redirect(f"/instance/{instance_id}/")

    user_key = session["user_key"]

    path = request.args.get("path")
    path_split = path.split("/")

    if request.method == "POST":
        data = request.json
        file_data = data["file_data"]

        response = panel.connector.write_file(user_key, int(instance_id), path_split, file_name, file_data)

        return response

    response = panel.connector.open_file(user_key, int(instance_id), path_split, file_name)
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

if __name__ == "__main__":
    app.run(debug=True)

    # panel.start(app)
