import redshift_connector
import pandas as pd
from security.AWSSecretManager import get_secret_database

creds = get_secret_database()


def get_conn():
    return redshift_connector.connect(**creds)


def upload_df_to_database(df, fileType):
    conn = get_conn()
    with conn.cursor() as cursor:
        cursor.write_dataframe(df, f"public.{fileType}")
        cursor.execute(f"select * from public.{fileType}; ")
        result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result
