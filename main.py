from flask import Flask, render_template, request, redirect, session
from engine import EngineConnector, InstancePermission

app = Flask(__name__)
app.secret_key = "<Secret Key>"

instance_connector = EngineConnector("127.0.0.1:52146")


@app.route("/")
def index():
    if "user_key" not in session:
        return redirect("/login/")

    user_key = session["user_key"]

    response = instance_connector.get_instances("12345678", user_key)
    instances = response["instances"] if response is not None else []

    return render_template("index.html", instances=instances)


@app.route("/instance/<instance_id>/")
def instance(instance_id: int):
    response = instance_connector.get_instance("12345678", "debug", int(instance_id))

    return render_template("instance/instance.html", instance_data=response["instance_data"])


@app.route("/instance/<instance_id>/permissions/")
def instance_permission(instance_id: int):
    user_permissions = instance_connector.get_user_permissions("12345678", "debug", int(instance_id))
    permissions = instance_connector.get_permissions("12345678", "debug")
    users = instance_connector.get_users("12345678", "debug")

    instance_permission = InstancePermission(user_permissions["users"], permissions["permissions"], users["users"])

    return render_template(
        "instance/permissions.html",
        permissions=instance_permission.get_user_permissions(),
        instance_id=instance_id
    )


@app.route("/instance/<instance_id>/permissions/add/", methods=["POST"])
def instance_permission_add(instance_id: int):
    data = request.json

    user_id = data["user_id"]
    permission_id = int(data["permission_id"])

    response = instance_connector.add_permission("12345678", "debug", instance_id, user_id, permission_id)

    print(response)

    return response


@app.route("/instance/<instance_id>/permissions/remove/", methods=["POST"])
def instance_permission_remove(instance_id: int):
    data = request.json

    user_id = data["user_id"]
    permission_id = int(data["permission_id"])

    response = instance_connector.remove_permission("12345678", "debug", instance_id, user_id, permission_id)

    print(response)

    return response


@app.route("/instance/<instance_id>/call/get_output/")
def instance_get_output(instance_id: int):
    response = instance_connector.get_output("12345678", "debug", int(instance_id))

    return response


@app.route("/instance/<instance_id>/call/server_send/", methods=["POST"])
def instance_send_server(instance_id: int):
    if request.method != "POST":
        return "Method not allowed", 405

    data = request.json
    command = data["command"]

    response = instance_connector.send_command("12345678", "debug", int(instance_id), command)

    return response


@app.route("/instance/<instance_id>/call/start_server/")
def instance_start_server(instance_id: int):
    response = instance_connector.start_instance("12345678", "debug", int(instance_id))

    return response


@app.route("/instance/<instance_id>/call/stop_server/")
def instance_stop_server(instance_id: int):
    response = instance_connector.stop_instance("12345678", "debug", int(instance_id))

    return response


@app.route("/login/")
def authorization():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
