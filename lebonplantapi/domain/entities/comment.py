from dataclasses import dataclass
from datetime import datetime

from .post import Post
from .user import User


@dataclass
class Comment:
    author: User
    body: str
    id: int
    post: Post
    posted_at: datetime
