from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Firmware(Base):
    __tablename__ = "firmware"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    alias = Column(String)
    board = Column(String)
    cmd = Column(String)
    description = Column(String)
    time = Column(String)
