from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Post(Base):
    __tablename__ = "post"
    __table_args__ = {"schema": "lebonplantapi"}

    author_id = Column(Integer, ForeignKey("lebonplantapi.user.id"), nullable=False)
    body = Column(String(3000), nullable=False)
    picture_link = Column(String(255), nullable=False)
    posted_at = Column(TIMESTAMP(timezone=True), nullable=False)
    title = Column(String(255), nullable=False)

    author = relationship("User", lazy="joined")
