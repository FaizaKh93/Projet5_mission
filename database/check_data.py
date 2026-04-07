from sqlalchemy import text
from database.db_config import engine

with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM predictions"))
    rows = result.fetchall()

    for row in rows:
        print(row)