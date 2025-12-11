from app.code.main.features import db
from app.code.messages.features import date
import config
from datetime import datetime


async def get(id: int):
    message = await db.select(
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
                orders.status,
                orders.log
            FROM 
                orders 
            INNER JOIN
                contacts ON orders.contact_id = contacts.id
            WHERE
                orders.id=%s
            ORDER BY 
                orders.id ASC
        """,
        (id,)
    )
    message = message[0]

    info = {
        "id": str(message[1]).zfill(8),
        "full_name": message[2],
        "pay_method": message[3].replace("1", "Повний платіж").replace("2", "Накладений платіж"),
        "pil_size": message[4],
        "pil_quantity": message[5],
        "full_price": message[6],
        "date": date.format(message[7]),
        "comments": list(enumerate(message[4].split("|"))) if message[8] is not None else [],
        "status": (message[9], {0: "c1c1c1", 1: "ffcc66", 2: "99ff9b"}[message[9]]),
        "log": message[10] if message[10] is not None else "",
        "img": f"{config.FTP}/data/got_img/{message[1]}.png",
        "no_bg_img": f"{config.FTP}/data/no_bg/{message[1]}.png",
        "pil_effect_img": f"{config.FTP}/data/pil_effect/{message[1]}.png"
    }

    return info


async def add_comment(id: int, comment: str, user: str = ""):
    comment = comment.replace("|", "")
    comments = [c for _, c in (await get(id))["comments"]]+[comment]

    await db.update(
        "UPDATE orders SET comment = %s, log = CONCAT(%s, COALESCE(log, '')) WHERE id = %s",
        (
            '|'.join(comments),
            f"""{datetime.now().strftime('%d.%m.%Y %H:%M')} - {user} додав(ла) коммент - {comment}\n""",
            id
        )
    )


async def delete_comment(id: int, index: int, user: str = ""):
    comments = [c for _, c in (await get(id))["comments"]]
    comment = comments[index]

    comments.pop(index)

    await db.update(
        "UPDATE orders SET comment = %s, log = CONCAT(%s, COALESCE(log, '')) WHERE id = %s",
        (
            '|'.join(comments),
            f"""{datetime.now().strftime('%d.%m.%Y %H:%M')} - {user} видалив(ла) коммент - {comment}\n""",
            id
        )
    )