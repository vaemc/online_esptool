from fastapi import Depends, FastAPI, HTTPException, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
import models
import schema
import os
from database import SessionLocal, engine

import serial.tools.list_ports

app = FastAPI()
origins = [
    "http://localhost:8080",
]

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
    users = db.query(models.Firmware).all()
    return users


@app.post("/firmware/save")
def firmware_save(firmware: schema.Firmware, db: Session = Depends(get_db)):
    db_firmware = models.Firmware(filename=firmware.filename, alias=firmware.alias, board=firmware.board,
                                  cmd=firmware.cmd, description=firmware.description, time=firmware.time)
    db.add(db_firmware)
    db.commit()
    db.refresh(db_firmware)
    return db_firmware


@app.post("/upload/file")
async def upload_file(file: UploadFile, alias: str = Form()):
    print(alias)
    try:
        contents = file.file.read()
        with open("./upload_file/" + alias, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    return {"message": f"Successfully uploaded {alias}"}



@app.get("/")
async def say_hello():
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
