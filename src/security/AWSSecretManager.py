import boto3
from botocore.exceptions import ClientError
import json

AWS_ACCESS_KEY = "AKIA4FBMJACIS3JKVZ7I"
AWS_SECRET_KEY = "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"
AWS_REGION_NAME = "us-east-1"


def get_secret_database():

    secret_name = "sqlworkbench!114a4537-dad3-4b14-a714-304ed2d46cb0"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION_NAME
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    # Your code goes here.
    return json.loads(secret)
