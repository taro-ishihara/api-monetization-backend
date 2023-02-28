import os
import json
import time
import urllib.request
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
level_name = os.environ['LOG_LEVEL']
level = logging.getLevelName(level_name)
logger.setLevel(level)

def get_secret():
    secret_name = "dev/managedapimonetization/fronteggapikey"
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
    return json.loads(secret)

api_keys = get_secret()
FRONTEGG_CLIENT_ID = api_keys['FRONTEGG_CLIENT_ID']
FRONTEGG_SECRET = api_keys['FRONTEGG_SECRET']

TOKEN = ''
TOKEN_EXP = 0
def vender_auth():
    global TOKEN
    global TOKEN_EXP
    if int(time.time()) < TOKEN_EXP:
        logger.info('recycle token')
        return TOKEN
        
    url = 'https://api.frontegg.com/auth/vendor/'
    data = {
        'clientId': FRONTEGG_CLIENT_ID,
        'secret': FRONTEGG_SECRET
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = json.loads(res.read())
        TOKEN = body['token']
        TOKEN_EXP = int(time.time()) + int(body['expiresIn'])
        return body['token']
        
def get_roles(token, role_key):
    url = 'https://api.frontegg.com/identity/resources/roles/v1'
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Accept': 'application/json',
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        body = json.loads(res.read())
        role = [role for role in body if role['key'] == role_key][0]
        return role
    
def get_permission(token, permission_key):
    url = 'https://api.frontegg.com/identity/resources/permissions/v1'
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Accept': 'application/json',
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        body = json.loads(res.read())
        permissions = [permission for permission in body if permission['key'] == permission_key]
        return permissions[0]
        
def create_permissions(token, product_id, subscription_id, createdat):
    url = 'https://api.frontegg.com/identity/resources/permissions/v1'
    data = [
        {
            'key': '{}.{}'.format(product_id, subscription_id),
            'name': '{} {}'.format(product_id, subscription_id),
            'description': f'subscribed from {createdat}'
        }
    ]
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = json.loads(res.read())
        return body
        
def delete_permission(token, permission_id):
    url = 'https://api.frontegg.com/identity/resources/permissions/v1/{}'.format(permission_id)
    headers = {
        'Authorization': 'Bearer {}'.format(token),
    }
    req = urllib.request.Request(url, headers=headers, method='DELETE')
    with urllib.request.urlopen(req) as res:
        return res
        
def set_permission_to_role(token, role_id, permissions):
    url = 'https://api.frontegg.com/identity/resources/roles/v1/{}/permissions'.format(role_id)
    data = {
        'permissionIds': permissions
    }
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    req = urllib.request.Request(url, json.dumps(data).encode(), headers, method='PUT')
    with urllib.request.urlopen(req) as res:
        body = json.loads(res.read())
        return body

def lambda_handler(event, context):
    body = json.loads(event['body'])
    logger.info(body)
    
    # extract parameters from body
    product_id = body['data']['object']['plan']['product']
    subscription_id = body['data']['object']['id']
    createdat = body['data']['object']['created']
    
    # token
    token = vender_auth()
    
    # get permissions
    role = get_roles(token, 'System')
    permissions = role['permissions']
    
    # add
    if body['type'] == 'customer.subscription.created':
        new_permission = create_permissions(token, product_id, subscription_id, createdat)
        permissions.append(new_permission[0]['id'])
        set_permission_to_role(token, role['id'], permissions)
    
    # delete
    if body['type'] == 'customer.subscription.deleted':
        permission_key = '{}.{}'.format(product_id, subscription_id)
        old_permission = get_permission(token, permission_key)
        delete_permission(token, old_permission['id'])
    
    return {
        'statusCode': 200,
    }
