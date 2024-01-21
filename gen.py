import asyncio
import asyncpg
from faker import Faker
import datetime

fake = Faker()

async def generate_and_insert_data(conn, chunk_size):
    data = []
    for _ in range(chunk_size):
        first_name = fake.first_name()
        last_name = fake.last_name()
        city = fake.city()
        email = fake.email()
        message_date = fake.date_time_this_decade()
        message = fake.text()
        data.append((first_name, last_name, city, email, message_date, message))

    query = "INSERT INTO messages (first_name, last_name, city, email, message_date, message) VALUES ($1, $2, $3, $4, $5, $6)"
    await conn.executemany(query, data)

async def main():
    conn = await asyncpg.connect(user='postgres', password='12345678',
                                 database='postgres', host='127.0.0.1')

    chunk_size = 250000
    for _ in range(10):
        await generate_and_insert_data(conn, chunk_size)

    await conn.close()

asyncio.run(main())
