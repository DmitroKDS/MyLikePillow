from app.code.main.features import db



async def get() -> list[tuple[int, str, str]]:
    channels = await db.select(f"SELECT id, name, count FROM channels ORDER BY id DESC")

    channels = [info+(f"https://t.me/mylikepillow_bot?start=channel_{info[-1]}",) for info in channels]

    return channels


async def add(name: str) -> None:
    await db.update(
        "INSERT INTO channels (name, count) VALUES (%s, %s)",
        (
            name,
            0
        )
    )