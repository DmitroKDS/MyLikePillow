from app.code.main.features import db
from app.code.messages.features import date

from datetime import datetime


async def get():
    orders = await db.select(
        f"""
            SELECT
                orders.id, 
                orders.request_id,
                contacts.full_name,
                orders.pay_method,
                orders.pil_size,
                orders.pil_quantity,
                orders.full_price,
                orders.date,
                orders.comment,
                orders.status
            FROM 
                orders
            INNER JOIN
                contacts ON orders.contact_id = contacts.id
            ORDER BY 
                orders.id DESC
        """
    )
    
    orders = [
        (id, str(request_id).zfill(8), full_name, pay_method.replace("1", "Повний платіж").replace("2", "Накладений платіж"), pil_size, pil_quantity, full_price, date.format(m_date), comment, status) 
        for id, request_id, full_name, pay_method, pil_size, pil_quantity, full_price, m_date, comment, status in orders
    ]
    orders = [[order for order in orders if order[9]==0], [order for order in orders if order[9]==1], [order for order in orders if order[9]==2]]

    return orders


async def edit_status(id: int, status: int, user: str = ""):
    status_str = {0: 'не оплачений', 1: 'оплачений', 2: 'завершений'}[status]
    await db.update(
        "UPDATE orders SET status = %s, log = CONCAT(%s, COALESCE(log, '')) WHERE id = %s",
        (
            status,
            f"""{datetime.now().strftime('%d.%m.%Y %H:%M')} - {user} змінив(ла) статус заказа на {status_str}\n""",
            id
        )
    )