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

app = FastAPI()
origins = [
    "http://localhost:8080",
]

firmware_path = "upload_file/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)


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


@app.post("/firmware/flash/{port}")
def firmware_flash(firmware: schema.Firmware, port: str):
    cmd = firmware.cmd.replace("${port}", port).replace("${bin}", firmware_path + firmware.alias).replace("${PORT}",
                                                                                                          port).replace(
        "${BIN}", firmware_path + firmware.alias)
    base_path = str(pathlib.Path(__file__).parent.resolve())
    if platform.system().lower() == 'windows':
        print("windows")
        fillCmd = "{path}\\tools\\websocketd.exe --port=8083 {path}\\tools\\esptool.exe write_flash 0x0 {path}\\tools\\ESP32S3_WIFI_SCAN.bin".format(
            path=base_path)
        print(fillCmd)
        # print(os.popen(fillCmd).read())
    if platform.system().lower() == 'linux':
        print("linux")
        fillCmd = "{path}\\tools\\websocketd.exe --port=8083 {path}\\tools\\esptool.exe write_flash 0x0 {path}\\tools\\ESP32S3_WIFI_SCAN.bin".format(
            path=base_path)
        print(fillCmd)
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


@app.get("/")
def hello():
    return "hello"


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
