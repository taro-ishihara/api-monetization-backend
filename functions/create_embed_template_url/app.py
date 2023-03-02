import os
import json
import logging
import datetime
import urllib.request
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
level_name = os.environ['LOG_LEVEL']
level = logging.getLevelName(level_name)
logger.setLevel(level)

def get_moesif_api_key():
    secret_name = "dev/managedapimonetization/moesifapikey"
    region_name = "us-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
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
    api_key = json.loads(secret)['MOESIF_API_KEY']
    return api_key
    
def get_expiration():
    now = datetime.datetime.now()
    one_day_later = now + datetime.timedelta(days=1)
    iso_date = one_day_later.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    return iso_date
    
def create_url(token, tenant_id, workspace_id):
    expiration = get_expiration()
    url = 'https://api.moesif.com/v1/portal/~/workspaces/{}/access_token?expiration={}'.format(workspace_id, expiration)
    data = {
        "template": {
            "values": {
                "user_id": tenant_id
            }
        }
    }
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json',
    }
    req = urllib.request.Request(url, json.dumps(data).encode(), headers, method='POST')
    with urllib.request.urlopen(req) as res:
        body = json.loads(res.read())
        return body

def lambda_handler(event, context):
    workspace_id = json.loads(event['body']).get('workspaceId', '')
    tenant_id = event['requestContext']['authorizer']['jwt']['claims']['tenantId']
    token = get_moesif_api_key()
    url = create_url(token, tenant_id, workspace_id)

    return {
        "statusCode": 200,
        'isBase64Encoded': False,
        "body": json.dumps(url),
        'headers': {
            'Content-Type': 'application/json'
        }
    }