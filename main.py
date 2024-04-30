from flask import Flask, render_template, request, redirect, session
from engine import EngineConnector, InstancePermission

app = Flask(__name__)
app.secret_key = "<Secret Key>"

engine_connector = EngineConnector("127.0.0.1:52146", "12345678")


@app.route("/")
def index():
    if "user_key" not in session:
        return redirect("/login/")

    user_key = session["user_key"]

    response = engine_connector.get_instances(user_key)
    if response["status"] == 403:
        return redirect("/login/")

    instances = response["instances"] if response is not None else []

    return render_template("index.html", instances=instances)


@app.route("/instance/<instance_id>/")
def instance(instance_id: int):
    if "user_key" not in session:
        return redirect("/login/")

    response = engine_connector.get_instance("debug", int(instance_id))
    if response["status"] == 403:
        return redirect("/login/")

    return render_template("instance/instance.html", instance_data=response["instance_data"])


@app.route("/instance/<instance_id>/permissions/")
def instance_permission(instance_id: int):
    if "user_key" not in session:
        return redirect("/login/")

    user_key = session["user_key"]

    user_permissions = engine_connector.get_user_permissions(user_key, int(instance_id))
    permissions = engine_connector.get_permissions(user_key)
    users = engine_connector.get_users(user_key)
    if user_permissions["status"] == 403 or permissions["status"] == 403 or user_permissions["status"] == 403:
        return redirect("/")

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

    response = engine_connector.add_permission(user_key, instance_id, user_id, permission_id)

    return response


@app.route("/instance/<instance_id>/permissions/remove/", methods=["POST"])
def instance_permission_remove(instance_id: int):
    if "user_key" not in session:
        return {}

    user_key = session["user_key"]

    data = request.json
    user_id = data["user_id"]
    permission_id = int(data["permission_id"])

    response = engine_connector.remove_permission(user_key, instance_id, user_id, permission_id)

    return response


@app.route("/instance/<instance_id>/call/get_output/")
def instance_get_output(instance_id: int):
    if "user_key" not in session:
        return {}

    user_key = session["user_key"]

    response = engine_connector.get_output(user_key, int(instance_id))

    return response


@app.route("/instance/<instance_id>/call/server_send/", methods=["POST"])
def instance_send_server(instance_id: int):
    if request.method != "POST":
        return "Method not allowed", 405

    if "user_key" not in session:
        return {}

    data = request.json
    command = data["command"]

    response = engine_connector.send_command("debug", int(instance_id), command)

    return response


@app.route("/instance/<instance_id>/call/start_server/")
def instance_start_server(instance_id: int):
    if "user_key" not in session:
        return {}

    user_key = session["user_key"]

    response = engine_connector.start_instance(user_key, int(instance_id))

    return response


@app.route("/instance/<instance_id>/call/stop_server/")
def instance_stop_server(instance_id: int):
    if "user_key" not in session:
        return {}

    response = engine_connector.stop_instance("debug", int(instance_id))

    return response


@app.route("/login/", methods=["GET", "POST"])
def authorization():
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        
        response = engine_connector.user_authorization(username, password)

        if response["status"] != 200:
            return redirect("/login/")

        user_key = response["user_data"]["key"]
        session["user_key"] = user_key

        return redirect("/")

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
