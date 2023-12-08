from flask import Flask, render_template, request
from model.smart_devices import *

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    home = Home("50th street, West")
    bulb = LightBulb("IvyComp", "PittComp", 5)
    home.add_device(bulb)
    return render_template('devices.html', home = home)

@app.route('/post_json', methods=['POST'])
def post_json_data():
    post_data = request.get_json()
    with open("light.json","w") as file_path :
            json.dump(json.dumps(post_data), file_path)
    return post_data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
    