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
    name, comment, picture = getParamFromBody(body)
    logger.info('name={0}, comment={1}, picture={2}'.format(name, comment, picture))

    poolId, userName = getUserInfo(event)
    logger.info('user info = {0}, {1}'.format(poolId, userName))

    updateUserInfo(poolId, userName, name, comment, picture)
    
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

def getParamFromBody(body):
  name = ""
  comment = None
  picture = None
  
  if 'name' not in body or not body['name']:
    raise ValueError('name is not exist.')

  name = body['name']
  if "comment" in body:
    comment = body['comment']
  
  if "picture" in body:
    picture = body['picture']
    
  return name, comment, picture

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

def updateUserInfo(poolId, userName, name, comment, picture):

  try:
    update_attributes = [
      {
        'Name': 'custom:name',
        'Value': name
      }
    ]
    if comment:
      update_attributes.append(
        {
          'Name': 'custom:comment',
          'Value': comment
        }
      )
    if picture:
      update_attributes.append(
        {
          'Name': 'custom:picture',
          'Value': picture
        }
      )
    COGNITO_CLIENT.admin_update_user_attributes(
        UserPoolId = poolId,
        Username = userName, 
        UserAttributes = update_attributes
      )
  except Exception as e:
    logger.exception(e)
    raise
