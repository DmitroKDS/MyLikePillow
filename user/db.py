from mysql.connector.aio import connect
import config

async def create_db() -> None:
    async with await connect(host=config.HOST, user=config.USER, password=config.PASSWORD, database=config.DB) as db_connector:
        async with await db_connector.cursor() as db_cursor:
            await db_cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS admins (
                    id INT PRIMARY KEY,
                    name VARCHAR(255),
                    role VARCHAR(255)
                );
                '''
            )

            await db_cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INT PRIMARY KEY,
                    full_name VARCHAR(255),
                    phone VARCHAR(20) NOT NULL
                );
                '''
            )

            await db_cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS channels (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    count INT NOT NULL
                );
                '''
            )

            await db_cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    contact_id INT NOT NULL,
                    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
                );
                '''
            )

            await db_cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    problem VARCHAR(255),
                    contact_id INT NOT NULL,
                    request_id INT NULL,
                    date DATETIME NOT NULL,
                    comment VARCHAR(255),
                    status INT NOT NULL,
                    log VARCHAR(255),
                    FOREIGN KEY (request_id) REFERENCES requests(id) ON DELETE CASCADE,
                    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
                );
                '''
            )

            await db_cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    request_id INT NOT NULL,
                    contact_id INT NOT NULL,
                    pay_method VARCHAR(255),
                    pil_size VARCHAR(255) NOT NULL,
                    pil_quantity INT NOT NULL,
                    full_price INT NOT NULL,
                    comment VARCHAR(255),
                    date DATETIME NOT NULL,
                    status INT NOT NULL,
                    log VARCHAR(255),
                    FOREIGN KEY (request_id) REFERENCES requests(id) ON DELETE CASCADE
                );
                '''
            )

        await db_connector.commit()


async def select(statement: str, param: tuple = None) -> list:
    async with await connect(host=config.HOST, user=config.USER, password=config.PASSWORD, database=config.DB) as db_connector:
        async with await db_connector.cursor() as db_cursor:
            await db_cursor.execute(statement, param)
            rows = await db_cursor.fetchall()

    return rows


async def update(statement: str, param: tuple = None) -> int:
    async with await connect(host=config.HOST, user=config.USER, password=config.PASSWORD, database=config.DB) as db_connector:
        async with await db_connector.cursor() as db_cursor:
            await db_cursor.execute(statement, param)

            last_id = db_cursor.lastrowid

        await db_connector.commit()

    return last_id