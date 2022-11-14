import json
from json import JSONEncoder
from flask import Flask, render_template, request, jsonify, flash
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import serial.tools.list_ports
import subprocess
import os
ports = serial.tools.list_ports.comports()
app = Flask(__name__, template_folder='./')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['UPLOAD_FOLDER'] = "./firmware"

db = SQLAlchemy(app)
db.init_app(app)
cors = CORS(app)


class Firmware(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    alias = db.Column(db.String(100))
    board = db.Column(db.String(100))
    cmd = db.Column(db.String(200))
    description = db.Column(db.String(200))
    time = db.Column(db.String(100))


# @app.route('/firmware/file', methods=['POST'])
# @cross_origin()
# def firmware_file():

#     return "asd"


@app.route('/firmware/save', methods=['POST'])
@cross_origin()
def firmware_save():
    firmware = Firmware(filename=request.json["filename"], alias=request.json["alias"], board=request.json["board"],
                        cmd=request.json["cmd"], description=request.json["description"], time=request.json["time"])
    db.session.add(firmware)
    db.session.commit()
    return "asd"


@app.route('/firmware/file/save', methods=['POST'])
def upload_file_save():
    file = request.files["file"]
    alias = request.form["alias"]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], alias))
    return "ok"

# @app.route('/firmware/query')
# @cross_origin()
# def firmware_query():

# @app.route('/firmware/update')
# @cross_origin()
# def firmware_update():


@app.route('/firmware/delete')
@cross_origin()
def firmware_query():
    firmware_list = Firmware.query.all()
    return jsonify(firmware_list)


@app.route('/port_list')
@cross_origin()
def port_list():
    serial_ports = []
    for port, desc, hwid in sorted(ports):
        try:
            s = serial.Serial(port)
            s.close()
            serial_ports.append(port)
        except (OSError, serial.SerialException):
            pass
    return jsonify(serial_ports)


@app.route('/execute_cmd')
@cross_origin()
def execute_cmd():
    #os.system("./websocketd --port=8081 cat /dev/ttyS3")
    # os.popen("./websocketd --port=8081 cat /dev/ttyS3").read()
    return_code = subprocess.call(
        "./websocketd --port=8081 cat /dev/ttyS3", shell=True)

    return "aa"


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()


with app.app_context():
    db.create_all()
