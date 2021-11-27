from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, func
from sqlalchemy.orm import declarative_base


SRID_WGS84 = 4326


class ModelMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    version = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=lambda: datetime.now(),
        nullable=False,
    )


Base = declarative_base(cls=ModelMixin)
