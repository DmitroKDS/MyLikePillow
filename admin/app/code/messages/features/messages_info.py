from app.code.main.features import db
from . import date
import config
from datetime import datetime


async def get(id: int):
    message = await db.select(
        f"""
            SELECT 
                messages.id, 
                messages.problem, 
                contacts.full_name,
                messages.date,
                messages.comment,
                messages.request_id,
                messages.status,
                messages.log
            FROM 
                messages 
            INNER JOIN
                contacts ON messages.contact_id = contacts.id
            WHERE
                messages.id=%s
            ORDER BY 
                messages.id ASC
        """,
        (id,)
    )
    message = message[0]

    info = {
        "id": str(message[0]).zfill(8),
        "problem": message[1],
        "full_name": message[2],
        "date": date.format(message[3]),
        "comments": list(enumerate(message[4].split("|"))) if message[4] is not None else [],
        "status": (message[6], {0: "c1c1c1", 1: "ffcc66", 2: "99ff9b"}[message[6]]),
        "log": message[7] if message[7] is not None else ""
    }

    if message[5]!=None:
        info = info | {
            "img": f"{config.FTP}/data/got_img/{message[5]}.png",
            "no_bg_img": f"{config.FTP}/data/no_bg/{message[5]}.png",
            "pil_effect_img": f"{config.FTP}/data/pil_effect/{message[5]}.png"
        }

    return info


async def add_comment(id: int, comment: str, user: str = ""):
    comment = comment.replace("|", "")
    comments = [c for _, c in (await get(id))["comments"]]+[comment]

    await db.update(
        "UPDATE messages SET comment = %s, log = CONCAT(%s, COALESCE(log, '')) WHERE id = %s",
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
        "UPDATE messages SET comment = %s, log = CONCAT(%s, COALESCE(log, '')) WHERE id = %s",
        (
            '|'.join(comments),
            f"""{datetime.now().strftime('%d.%m.%Y %H:%M')} - {user} видалив(ла) коммент - {comment}\n""",
            id
        )
    )