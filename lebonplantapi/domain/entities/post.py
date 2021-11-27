from dataclasses import dataclass
from datetime import datetime

from .user import User


@dataclass
class Post:
    id: int
    body: str
    picture_link: str
    posted_at: datetime
    title: str
    author: User
