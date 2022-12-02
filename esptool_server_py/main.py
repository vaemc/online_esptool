import subprocess
import uvicorn
import models
import schema
import os
import platform
import pathlib
import serial.tools.list_ports
import yaml
from fastapi import Depends, FastAPI, HTTPException, File, Form, UploadFile, requests
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from subprocess import Popen, PIPE, STDOUT

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


flash_ws_port = application_config()['websocket']['port']['flash']
monitor_ws_port = application_config()['websocket']['port']['monitor']
base_path = str(pathlib.Path(__file__).parent.resolve())


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
def firmware_delete(id: int, db: Session = Depends(get_db)):
    firmware = db.query(models.Firmware).filter(models.Firmware.id == id).first()
    db.delete(firmware)
    db.commit()
    file_delete(firmware.alias)
    return "ok"


@app.delete("/file/delete/{name}")
def file_delete(name: str):
    os.remove("./upload_file/" + name)
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
    print(os.popen("ps -ef |grep 'websocketd --port=%s' | awk '{print $2}' | xargs kill -9" % flash_ws_port).read())
    esptool_cmd = "{path}/tools/esptool{platform} {cmd}".format(path=base_path,
                                                                platform='.exe' if platform.system().lower() == 'windows' else '',
                                                                cmd=firmware.cmd).replace("${PORT}", port).replace(
        "${BIN}", base_path + firmware_path + firmware.alias)
    websocketd_cmd = "nohup {path}/tools/websocketd{platform} --port={flash_ws_port} {cmd} &".format(path=base_path,
                                                                                                     platform='.exe' if platform.system().lower() == 'windows' else '',
                                                                                                     flash_ws_port=flash_ws_port,
                                                                                                     cmd=esptool_cmd)
    print(websocketd_cmd)
    subprocess.call(websocketd_cmd, shell=True)
    return "ok"


@app.get("/monitor/")
def monitor(port: str, baud: str):
    os.popen("ps -ef |grep 'websocketd --port=%s' | awk '{print $2}' | xargs kill -9" % monitor_ws_port)
    monitor_cmd = "python3 {path}/tools/monitor.py -p {port} -b {baud}".format(path=base_path, port=port, baud=baud)
    websocketd_cmd = "nohup {path}/tools/websocketd{platform} --port={monitor_ws_port} {cmd} &".format(path=base_path,
                                                                                                       platform='.exe' if platform.system().lower() == 'windows' else '',
                                                                                                       monitor_ws_port=monitor_ws_port,
                                                                                                       cmd=monitor_cmd)
    print(websocketd_cmd)
    subprocess.call(websocketd_cmd, shell=True)
    return "ok"


@app.post("/upload/file")
async def upload_file(file: UploadFile, alias: str = Form()):
    try:
        contents = file.file.read()
        with open(base_path + firmware_path + alias, 'wb') as f:
            f.write(contents)
    except Exception:
        print("There was an error uploading the file")
        return {"error"}
    finally:
        file.file.close()
    print(f"Successfully uploaded {alias}")
    return {"ok"}


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
