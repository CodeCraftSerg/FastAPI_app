import unittest
from unittest.mock import MagicMock, AsyncMock, Mock
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema
from src.repository.contacts import (
    get_contacts,
    get_all_contacts,
    get_contact,
    create_contact,
    update_contact,
    delete_contact,
    search_contacts,
    congrats,
)


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(id=1, username="test_user", password="qwerty", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [
            Contact(
                id=1,
                name="test_name_1",
                surname="test_surname_1",
                email="test_email_1",
                phone="test_phone_1",
                birthday=date.today(),
                notes="test_notes_1",
                user=self.user,
            ),
            Contact(
                id=2,
                name="test_name_2",
                surname="test_surname_2",
                email="test_email_2",
                phone="test_phone_2",
                birthday=date.today(),
                notes="test_notes_2",
                user=self.user,
            ),
        ]
        mocked_contacts = Mock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_get_all_contacts(self):
        limit = 10
        offset = 0
        contacts = [
            Contact(
                id=1,
                name="test_name_1",
                surname="test_surname_1",
                email="test_email_1",
                phone="test_phone_1",
                birthday=date.today(),
                notes="test_notes_1",
                user=self.user,
            ),
            Contact(
                id=2,
                name="test_name_2",
                surname="test_surname_2",
                email="test_email_2",
                phone="test_phone_2",
                birthday=date.today(),
                notes="test_notes_2",
                user=self.user,
            ),
        ]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_all_contacts(limit, offset, self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact = Contact(
            id=1,
            name="test_name_1",
            surname="test_surname_1",
            email="test_email_1",
            phone="test_phone_1",
            birthday="2024-04-09",
            notes="test_notes_1",
            user=self.user,
        )
        mocked_contact = Mock()
        mocked_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await get_contact(1, self.session, self.user)
        self.assertEqual(result, contact)

    async def test_create_contact(self):
        body = ContactSchema(
            name="name",
            surname="surname",
            email="test@email.net",
            phone="+380939876532",
            birthday="2024-04-09",
            notes="test_notes",
        )
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.notes, body.notes)

    async def test_update_contact(self):
        body = ContactUpdateSchema(
            name="name",
            surname="surname",
            email="test@email.net",
            phone="+380939876532",
            birthday="2024-04-09",
            notes="test_notes",
        )
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(
            id=1,
            name="name",
            surname="surname",
            email="test@email.net",
            phone="+380939876532",
            birthday="2024-04-09",
            notes="test_notes",
            user=self.user,
        )
        self.session.execute.return_value = mocked_contact
        result = await update_contact(1, body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.notes, body.notes)

    async def test_delete_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(
            id=1,
            name="name",
            surname="surname",
            email="test@email.net",
            phone="+380939876532",
            birthday="2024-04-09",
            notes="test_notes",
            user=self.user,
        )
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()

        self.assertIsInstance(result, Contact)

    async def test_search_contacts(self):
        contacts = [
            Contact(
                name="test_name_1",
                surname="test_surname_1",
                email="test_email_1",
                user=self.user,
            ),
            Contact(
                name="test_name_2",
                surname="test_surname_2",
                email="test_email_2",
                user=self.user,
            ),
        ]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await search_contacts("test_name_1", self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_congrats(self):
        contacts = [
            Contact(
                name="test_name_1",
                surname="test_surname_1",
                email="test_email_1",
                birthday=date.today(),
                user=self.user,
            ),
            Contact(
                name="test_name_2",
                surname="test_surname_2",
                email="test_email_2",
                birthday=date.today(),
                user=self.user,
            ),
        ]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await congrats(self.session, self.user)
        self.assertEqual(result, contacts)
