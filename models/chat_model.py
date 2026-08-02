from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from config.database import Base


class Message(Base):
    __tablename__ = "message"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    role = Column(
        String(20),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )