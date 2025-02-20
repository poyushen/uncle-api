import numpy as np
import pandas as pd
import pymssql


def build_connection():
    connection = pymssql.connect(
        server="0.0.0.0", port=1433, user="SA", password="1qaz!QAZ"
    )

    return connection


def fetch_data(sql: str) -> pd.DataFrame:
    connection = build_connection()
    cursor = connection.cursor()
    cursor.execute(sql)

    fetch = cursor.fetchall()
    if not len(fetch):
        return None

    df = pd.DataFrame(np.array(fetch), columns=np.array(cursor.description)[:, 0])

    connection.close()

    return df


def insert_data(sql: str, data: list) -> None:
    connection = build_connection()
    cursor = connection.cursor()
    cursor.execute(sql, data)

    connection.commit()
    connection.close()


def exec_table(sql) -> None:
    connection = build_connection()
    cursor = connection.cursor()
    cursor.execute(sql)

    connection.commit()
    connection.close()
