import redshift_connector
import pandas as pd
from src.security.AWSSecretManager import get_secret_database

creds = get_secret_database()


def get_conn():
    return redshift_connector.connect(**creds)


def upload_df_to_database(df, fileType):
    conn = get_conn()
    with conn.cursor() as cursor:
        cursor.write_dataframe(df, f"public.{fileType}")
        cursor.execute(f"SELECT * FROM public.{fileType}; ")
        result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def get_metric(type):
    conn = get_conn()
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM public.{type};")
        result = cursor.fetchall()
        field_names = [i[0] for i in cursor.description]
        df = pd.DataFrame(result)
        df.columns = field_names
    conn.commit()
    conn.close()
    #print("results: ", df.to_dict(orient="records"))
    return df.to_dict(orient="records")
