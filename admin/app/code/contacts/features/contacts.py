from app.code.main.features import db


async def get():
    contacts = await db.select(f"SELECT id, full_name, phone FROM contacts ORDER BY id DESC")

    return contacts