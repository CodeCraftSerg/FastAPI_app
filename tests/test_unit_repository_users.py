import unittest
from unittest.mock import MagicMock, AsyncMock, Mock
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.user import UserSchema
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar_url,
)


class TestAsyncUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(
            id=1,
            username="user",
            email="user@mail.net",
            password="qwerty",
            avatar="path/to/avatar.png",
            refresh_token="token",
            role="admin",
            confirmed=True,
        )
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_user_by_email(self):
        user = self.user
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await get_user_by_email(user.email, self.session)
        self.assertEqual(result.username, "user")
        self.assertEqual(result.email, "user@mail.net")

    async def test_create_user(self):
        body = UserSchema(username="user", email="user@mail.net", password="qwerty")
        result = await create_user(body, self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)

    async def test_update_token(self):
        token = "new_token"
        result = await update_token(self.user, token, self.session)
        self.assertIsNone(result)

    async def test_confirmed_email(self):
        user = self.user
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await confirmed_email(user.email, self.session)
        self.assertIsNone(result)

    async def test_update_avatar_url(self):
        user = self.user
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        new_avatar = "path/to/new_avatar.png"
        result = await update_avatar_url(user.email, new_avatar, self.session)
        self.assertEqual(result.avatar, new_avatar)
