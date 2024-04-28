from flask import Flask, render_template, jsonify, request, redirect
from instance import InstanceConnector, InstancePermission

app = Flask(__name__)

instance_connector = InstanceConnector("127.0.0.1:52146")
instance_connector.connect("12345678")


@app.route("/")
def index():
    response = instance_connector.get_instances("12345678", "debug")
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

    instance_permission = InstancePermission(user_permissions["users"], permissions["permissions"])

    return render_template(
        "instance/permissions.html",
        permissions=instance_permission.get_user_permissions()
    )


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


if __name__ == "__main__":
    app.run(debug=True)
