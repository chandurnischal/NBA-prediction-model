import mysql.connector as mc
import pandas as pd


def sqlTodf(query: str, creds: dict) -> pd.DataFrame:
    with mc.connect(**creds) as conn:
        cur = conn.cursor()

        cur.execute(query)
        column_names = [column[0] for column in cur.description]
        rows = cur.fetchall()

    data = pd.DataFrame(rows, columns=column_names)

    return data
