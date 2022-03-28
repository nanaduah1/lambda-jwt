import json

from auth.models import db
from auth.schema import schema

AUTHORIZER_KEY = "authorizationToken"
AUTHORIZER_METHOD_ARN = "methodArn"

GRAPHQL_QUERY_KEY = "query"


def handler(event, context):
    if AUTHORIZER_KEY in event and AUTHORIZER_METHOD_ARN in event:
        return handle_token_authorization(
            event[AUTHORIZER_KEY], event[AUTHORIZER_METHOD_ARN]
        )
    elif "body" in event and GRAPHQL_QUERY_KEY in event["body"]:
        return handle_graph_query(event, context)


def handle_token_authorization(token, methodArn):
    db.connect()

    db.close()
    return {
        "body": "",
        "statusCode": "",
        "headers": {"Content-Type": "application/json"},
    }


def handle_graph_query(event, context):
    db.connect()

    body = json.loads(event["body"])
    result = schema.execute(body["query"])
    db.close()
    return {
        "body": json.dumps(result.formatted),
        "statusCode": 200 if result.errors is None else 500,
        "headers": {"Content-Type": "application/json"},
    }
