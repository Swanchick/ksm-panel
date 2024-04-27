import requests.cookies
from flask import Flask, render_template, jsonify, request, redirect
from requests import post

from instance.instance_connector import InstanceConnector

app = Flask(__name__)

instance_connector = InstanceConnector("127.0.0.1:52146")


@app.route("/")
def index():
    response = instance_connector.get_instances("12345678", "debug")

    return render_template("index.html", instances=response["instances"])


@app.route("/instance/<instance_id>/")
def instance(instance_id: int):
    response = instance_connector.get_instance("12345678", "debug", int(instance_id))

    return render_template("instance.html", instance_data=response["instance_data"])


@app.route("/instance/<instance_id>/call/get_output/")
def instance_get_output(instance_id: int):
    response = instance_connector.get_output("12345678", "debug", int(instance_id))

    return response


@app.route("/instance/<instance_id>/call/get_last_output/")
def instance_get_last_output(instance_id: int):
    response = instance_connector.get_last_output("12345678", "debug", int(instance_id))

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
