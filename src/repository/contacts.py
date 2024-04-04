from datetime import date, timedelta

from sqlalchemy import select, and_, or_, extract
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    statement = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(statement)
    return contacts.scalars().all()


async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    statement = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(statement)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    statement = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(statement)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(
    contact_id: int, body: ContactUpdateSchema, db: AsyncSession, user: User
):
    statement = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(statement)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.notes = body.notes
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    statement = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(statement)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contacts(query: str, db: AsyncSession, user: User):
    statement = (
        select(Contact)
        .filter(
            or_(
                Contact.name.ilike(f"%{query}%"),
                Contact.surname.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%"),
            )
        )
        .filter_by(user=user)
    )
    contacts = await db.execute(statement)
    return contacts.scalars().all()


async def congrats(db: AsyncSession, user: User):
    current_date = date.today()
    next_week = current_date + timedelta(days=7)

    statement = (
        select(Contact)
        .filter(
            and_(
                extract("month", Contact.birthday) >= current_date.month,
                extract("day", Contact.birthday) >= current_date.day,
                extract("month", Contact.birthday) <= next_week.month,
                extract("day", Contact.birthday) <= next_week.day,
            )
        )
        .filter_by(user=user)
    )
    contacts = await db.execute(statement)
    return contacts.scalars().all()
