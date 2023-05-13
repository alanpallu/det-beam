import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def create_table_from_excel_file(excel_file, table_name, database_name
                                 , server_name, port, user_name, password):
    engine = create_engine(f'postgresql://'
    f'{user_name}:{password}@{server_name}:{port}/{database_name}')

    conn = engine.connect()

    # read Excel file
    df = pd.read_excel(excel_file)

    # create a table in the database
    df.to_sql(table_name, conn, if_exists='replace', index=True)


def select_all(table_name, database, host, port, user, password):
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

    sql1 = f"select * from {table_name}"

    res = pd.read_sql(sql1, conn)
    res.set_index('BX', inplace=True)
    return res
