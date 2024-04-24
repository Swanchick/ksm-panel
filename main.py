from flask import Flask, render_template
from requests import post

from instance.instance_connector import InstanceConnector

app = Flask(__name__)

instance_connector = InstanceConnector("127.0.0.1:52146")

@app.route("/")
def index():
    response = instance_connector.get_instances("12345678", "debug")

    print(response)

    return render_template("index.html", instances=response["instances"])


@app.route("/instance/<instance_id>")
def instance(instance_id: int):
    return render_template("instance.html")


if __name__ == "__main__":
    app.run(debug=True)
