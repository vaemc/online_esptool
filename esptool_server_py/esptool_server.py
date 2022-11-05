from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import serial.tools.list_ports
import subprocess

ports = serial.tools.list_ports.comports()
app = Flask(__name__, template_folder='./')
cors = CORS(app)

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
    print(subprocess.Popen("./websocketd --port=8081 cat /dev/ttyS3", shell=True, stdout=subprocess.PIPE).stdout.read())
    return "aa"

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
