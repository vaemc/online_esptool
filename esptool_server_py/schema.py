from datetime import date
from pydantic import BaseModel


class Firmware(BaseModel):
    id: int
    filename: str
    alias: str
    board: str
    cmd: str
    description: str
    time: str
