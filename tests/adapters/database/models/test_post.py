from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from lebonplantapi.adapters.database.models import Post, User


pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.usefixtures("db"),
]


class TestPost:
    async def test_ok(self, session_autoclose: AsyncSession) -> None:
        post = Post(
            body="This is fine.",
            picture_link="https://www.google.com/?search=picture_of_dog_on_fire",
            posted_at=datetime.now(),
            title="I am fine",
            author=User(id=45, name="Covfefe loving dog"),
        )
        session_autoclose.add(post)
        await session_autoclose.flush()
