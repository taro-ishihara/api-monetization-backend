import os
import json
import logging
import stripe
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
level_name = os.environ['LOG_LEVEL']
level = logging.getLevelName(level_name)
logger.setLevel(level)

def get_secret():
    secret_name = "dev/managedapimonetization/stripeapikey"
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
    return secret

stripe.api_key = json.loads(get_secret())['STRIPE_API_KEY']

def lambda_handler(event, context):
    tenant_id = event['requestContext']['authorizer']['jwt']['claims']['tenantId']

    customers = stripe.Customer.search(
        query="metadata['fronteggTenantId']:'{}'".format(tenant_id),
    )
    if customers['data']:
        customer_id = customers['data'][0]['id']

    product_id = json.loads(event['body']).get('productId', '')
    prices = stripe.Price.list(product=product_id)

    if len(prices['data']) == 1:
        price_id = prices['data'][0]['id']

    stripe.Subscription.create(
        customer=customer_id,
        items=[
            {"price": price_id},
        ],
        metadata={
            'productId': product_id
        }
    )
    return {
        "statusCode": 200,
    }