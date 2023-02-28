import json

import pytest
from unittest.mock import patch

with patch.dict("os.environ", {"LOG_LEVEL": "INFO"}):
    from functions.event_inspect import app as event_inspect_func
    from functions.register import app as register_func
    from functions.list_products import app as list_products_func
    from functions.subscribe import app as subscribe_func

@pytest.fixture()
def apigw_event_register():
    """ Generates API GW Event"""

    return {
        'resource': '/eventinspect', 'path': '/eventinspect', 'httpMethod': 'POST', 'headers': {'Accept': 'application/json, text/plain, */*', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-ASN': '16509', 'CloudFront-Viewer-Country': 'IE', 'Content-Type': 'application/json', 'frontegg-trace-id': 'b0888b70-5fb5-45ad-a3db-c435af526de0', 'Host': '8gpzexe4e9.execute-api.us-west-1.amazonaws.com', 'uber-trace-id': '20e2db89158e7a41f32fe78c929caee8:74323a3f21985b34:0:01', 'User-Agent': 'FrontEgg HTTP Client', 'Via': '1.1 8070396f8b32ef8fc0f9390bd6dee8de.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'Dme8BOvAPTHi3EiZfr1JiYpnHykieBJKLt8_CAY6gJWp4MaV9t3_DQ==', 'X-Amzn-Trace-Id': 'Root=1-63fb95b2-330ce6e72658e3fa1b03338b', 'X-Forwarded-For': '99.81.198.187, 64.252.133.137', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https', 'x-webhook-secret': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2Nzc0MzIyNDIsImV4cCI6MTY3NzQzMjU0Mn0.9J6KfkQhXx3oCOGxapYNXLdcqChFHKWAMLaEnUhXqKI'}, 'multiValueHeaders': {'Accept': ['application/json, text/plain, */*'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-ASN': ['16509'], 'CloudFront-Viewer-Country': ['IE'], 'Content-Type': ['application/json'], 'frontegg-trace-id': ['b0888b70-5fb5-45ad-a3db-c435af526de0'], 'Host': ['8gpzexe4e9.execute-api.us-west-1.amazonaws.com'], 'uber-trace-id': ['20e2db89158e7a41f32fe78c929caee8:74323a3f21985b34:0:01'], 'User-Agent': ['FrontEgg HTTP Client'], 'Via': ['1.1 8070396f8b32ef8fc0f9390bd6dee8de.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['Dme8BOvAPTHi3EiZfr1JiYpnHykieBJKLt8_CAY6gJWp4MaV9t3_DQ=='], 'X-Amzn-Trace-Id': ['Root=1-63fb95b2-330ce6e72658e3fa1b03338b'], 'X-Forwarded-For': ['99.81.198.187, 64.252.133.137'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https'], 'x-webhook-secret': ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2Nzc0MzIyNDIsImV4cCI6MTY3NzQzMjU0Mn0.9J6KfkQhXx3oCOGxapYNXLdcqChFHKWAMLaEnUhXqKI']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'rxrt1c', 'resourcePath': '/eventinspect', 'httpMethod': 'POST', 'extendedRequestId': 'A9RT-FwZyK4FUmw=', 'requestTime': '26/Feb/2023:17:24:02 +0000', 'path': '/Prod/eventinspect', 'accountId': '044107946839', 'protocol': 'HTTP/1.1', 'stage': 'Prod', 'domainPrefix': '8gpzexe4e9', 'requestTimeEpoch': 1677432242761, 'requestId': '839b1e59-3a11-4e2e-b8d9-b2cecb8a4c37', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '99.81.198.187', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'FrontEgg HTTP Client', 'user': None}, 'domainName': '8gpzexe4e9.execute-api.us-west-1.amazonaws.com', 'apiId': '8gpzexe4e9'}, 'body': '{"eventKey":"frontegg.user.created","user":{"id":"user-id","sub":"sub","email":"test@email.com","verified":true,"mfaEnrolled":false,"roles":[],"permissions":[],"provider":"local","tenantId":"tenant-id","tenantIds":["tenant-id"],"tenants":[{"tenantId":"tenant-id","roles":[]}],"metadata":"{}","createdAt":"2023-02-26T04:46:56.749Z","lastLogin":"2023-02-26T04:46:56.749Z"},"eventContext":{"vendorId":"vendor-id","tenantId":"tenant-id","userId":"user-id"}}', 'isBase64Encoded': False
    }


def test_event_inspect_handler():
    ret = event_inspect_func.lambda_handler({}, "")

    assert ret["statusCode"] == 200


# def test_register_handler(apigw_event_register):
#     ret = event_inspect_func.lambda_handler(apigw_event_register, "")
#     data = json.loads(ret["body"])

#     assert ret["statusCode"] == 200
#     # assert "message" in ret["body"]
#     # assert data["message"] == "hello world"

# def test_list_products_handler():
#     ret = list_products_func.lambda_handler({}, "")

#     print(ret)
#     assert ret["statusCode"] == 200
#     # assert "message" in ret["body"]
#     # assert data["message"] == "hello world"

def test_subscribe_handler():
    ret = subscribe_func.lambda_handler({}, "")

    print(ret)
    assert ret["statusCode"] == 200
    # assert "message" in ret["body"]
    # assert data["message"] == "hello world"
