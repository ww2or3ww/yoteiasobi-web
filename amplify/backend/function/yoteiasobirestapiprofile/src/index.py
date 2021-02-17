import json
import datetime

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import boto3
COGNITO_CLIENT = boto3.client('cognito-idp')

def handler(event, context):
  try:
    logger.info('=== START ===')
    logger.info(json.dumps(event, ensure_ascii=False, indent=2))

    body = json.loads(event['body'])
    name = body['name']
    comment = body['comment']
    logger.info('name={0}, comment={1}'.format(name, comment))
    
    if not name:
      raise ValueError('name is not exist.')

    poolId, userName = getUserInfo(event)
    logger.info('user info = {0}, {1}'.format(poolId, userName))

    updateUserInfo(poolId, userName, name, comment)

    return {
      "statusCode": 200,
      "body": json.dumps(body),
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    }

  except Exception as e:
      logger.exception(e)
      return {
        "statusCode": 500,
        "body": json.dumps("error : {0}".format(e)),
        'headers': {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
      }

def getUserInfo(event):
  poolId = None
  userName = None

  try:
    poolId = event["requestContext"]["identity"]["cognitoAuthenticationProvider"].split(',')[0].split('/')[1]
    userSub = event["requestContext"]["identity"]["cognitoAuthenticationProvider"].split(',')[1].split(':')[2]
    response = COGNITO_CLIENT.list_users(
        UserPoolId = poolId,
        Filter = "sub = \"{0}\"".format(userSub)
    )
    userName = response['Users'][0]['Username']
    
  except Exception as e:
    logger.exception(e)
    raise

  return poolId, userName

def updateUserInfo(poolId, userName, name, comment):

  try:
    update_attributes = [
      {
        'Name': 'custom:name',
        'Value': name
      },
      {
        'Name': 'custom:comment',
        'Value': comment
      }
    ]
    COGNITO_CLIENT.admin_update_user_attributes(
        UserPoolId = poolId,
        Username = userName, 
        UserAttributes = update_attributes
      )
  except Exception as e:
    logger.exception(e)
    raise
