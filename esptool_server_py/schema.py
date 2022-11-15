from datetime import date
from pydantic import BaseModel


class Firmware(BaseModel):
    filename: str
    alias: str
    board: str
    cmd: str
    description: str
    time: str
