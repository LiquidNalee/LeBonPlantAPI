from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Comment(Base):
    __tablename__ = "comment"
    __table_args__ = {"schema": "lebonplantapi"}

    author_id = Column(Integer, ForeignKey("lebonplantapi.user.id"), nullable=False)
    body = Column(String(3000), nullable=False)
    posted_at = Column(TIMESTAMP(timezone=True), nullable=False)
    post_id = Column(Integer, ForeignKey("lebonplantapi.user.id"), nullable=False)

    author = relationship("User", lazy="joined")
    post = relationship("Post", lazy="joinded")
