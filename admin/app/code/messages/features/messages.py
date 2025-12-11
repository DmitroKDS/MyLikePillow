from app.code.main.features import db
from . import date
from datetime import datetime


async def get():
    messages = await db.select(
        f"""
            SELECT 
                messages.id, 
                messages.problem, 
                contacts.full_name,
                messages.date,
                messages.comment,
                messages.status
            FROM 
                messages 
            INNER JOIN
                contacts ON messages.contact_id = contacts.id
            ORDER BY 
                messages.id ASC
        """
    )

    messages = [(id, problem, full_name, date.format(m_date), comment, status) for id, problem, full_name, m_date, comment, status in messages]
    messages = [[message for message in messages if message[5]==0], [message for message in messages if message[5]==1], [message for message in messages if message[5]==2]]

    return messages


async def edit_status(id: int, status: int, user: str = ""):
    status_str = {0: 'новий', 1: 'в процессі', 2: 'завершений'}[status]
    await db.update(
        "UPDATE messages SET status = %s, log = CONCAT(%s, COALESCE(log, '')) WHERE id = %s",
        (
            status,
            f"""{datetime.now().strftime('%d.%m.%Y %H:%M')} - {user} змінив(ла) статус питання на {status_str}\n""",
            id
        )
    )