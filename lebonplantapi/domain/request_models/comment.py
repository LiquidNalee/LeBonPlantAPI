from dataclasses import dataclass
from datetime import datetime


@dataclass
class CommentCreation:
    author_id: int
    body: str
    id: int
    post_id: int
    posted_at: datetime
