from dataclasses import dataclass
from datetime import datetime


@dataclass
class PostCreation:
    body: str
    picture_link: str
    posted_at: datetime
    title: str
    author_id: int
