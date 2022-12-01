import subprocess

from fastapi import Depends, FastAPI, HTTPException, File, Form, UploadFile, requests
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schema
import os
from database import SessionLocal, engine
import platform
import pathlib
import serial.tools.list_ports
from subprocess import Popen, PIPE, STDOUT
import yaml


app = FastAPI()
origins = [
    "http://localhost:8080",
]

firmware_path = "/upload_file/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)


def application_config():
    with open('application.yml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data


flash_port = application_config()['websocket']['port']['flash']
monitor_port = application_config()['websocket']['port']['monitor']


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/firmware/query")
def firmware_query(db: Session = Depends(get_db)):
    firmware_list = db.query(models.Firmware).all()
    return firmware_list


@app.post("/firmware/save")
def firmware_save(firmware: schema.Firmware, db: Session = Depends(get_db)):
    db_firmware = models.Firmware(filename=firmware.filename, alias=firmware.alias, board=firmware.board,
                                  cmd=firmware.cmd, description=firmware.description, time=firmware.time)
    db.add(db_firmware)
    db.commit()
    db.refresh(db_firmware)
    return db_firmware


@app.delete("/firmware/delete/{id}")
def firmware_query(id: int, db: Session = Depends(get_db)):
    firmware = db.query(models.Firmware).filter(models.Firmware.id == id).first()
    db.delete(firmware)
    db.commit()
    os.remove("./upload_file/" + firmware.alias)
    return "ok"


def run_cmd(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line


def exe_command(command):
    print(command)
    process = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            print(line.decode().strip())
    exitcode = process.wait()
    return process, exitcode


# https://github.com/espressif/esp-idf/issues/4008
@app.post("/firmware/flash/")
def firmware_flash(firmware: schema.Firmware, port: str):
    base_path = str(pathlib.Path(__file__).parent.resolve())
    #结束烧录的websocketd
    print(os.popen("ps -ef |grep 'websocketd --port=8083' | awk '{print $2}' | xargs kill -9").read())

    esptool_cmd = "{path}/tools/esptool{platform} {cmd}".format(path=base_path,
                                                                  platform='.exe' if platform.system().lower() == 'windows' else '',
                                                                  cmd=firmware.cmd).replace("${PORT}", port).replace(
        "${BIN}", base_path + firmware_path + firmware.alias)

    websocketd_cmd = "nohup {path}/tools/websocketd{platform} --port=8083 {cmd} &".format(path=base_path,
                                                                 platform='.exe' if platform.system().lower() == 'windows' else '',
                                                                 cmd=esptool_cmd)
    print(websocketd_cmd)
    # print(esptool_cmd)

    # exe_command(esptool_cmd)

    subprocess.call(websocketd_cmd, shell=True)
    return "ok"


@app.post("/monitor/")
def monitor(baud: str, port: str):
    base_path = str(pathlib.Path(__file__).parent.resolve())
    #结束监视器的websocketd
    os.popen("ps -ef |grep 'websocketd --port=8085' | awk '{print $2}' | xargs kill -9")



    websocketd_cmd = "nohup {path}/tools/websocketd{platform} --port=8085 {cmd} &".format(path=base_path,
                                                                 platform='.exe' if platform.system().lower() == 'windows' else '',
                                                                 cmd='')
    print(websocketd_cmd)
    # print(esptool_cmd)

    # exe_command(esptool_cmd)

    subprocess.call(websocketd_cmd, shell=True)
    return "ok"


@app.post("/upload/file")
async def upload_file(file: UploadFile, alias: str = Form()):
    print(alias)
    try:
        contents = file.file.read()
        with open(firmware_path + alias, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    return {"message": f"Successfully uploaded {alias}"}


@app.get('/port_list')
def port_list():
    ports = serial.tools.list_ports.comports()
    serial_ports = []
    for port, desc, hwid in sorted(ports):
        try:
            s = serial.Serial(port)
            s.close()
            serial_ports.append(port)
        except (OSError, serial.SerialException):
            pass
    return serial_ports
