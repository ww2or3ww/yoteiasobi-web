import json
import datetime
import logging
import boto3
logger = logging.getLogger()
logger.setLevel(logging.INFO)

COGNITO_CLIENT = boto3.client('cognito-idp')

def handler(event, context):
  logger.info(json.dumps(event, ensure_ascii=False, indent=2))
  userInfo = getUserInfo(event)

  try:
    
    current_time = datetime.datetime.now().time()
    body = {
        "message": "Hello, the current time is " + str(current_time)
    }
    return {
      "statusCode": 200,
      "body": json.dumps(body),
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
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
  userSub = None

  try:
    poolId = event["requestContext"]["identity"]["cognitoAuthenticationProvider"].split(',')[0].split('/')[1]
    userSub = event["requestContext"]["identity"]["cognitoAuthenticationProvider"].split(',')[1].split(':')[2]
    logger.info('user info = {0}, {1}'.format(poolId, userSub))

    response = COGNITO_CLIENT.list_users(
        UserPoolId = poolId,
        Filter = "sub = \"{0}\"".format(userSub)
    )
    logger.info(response)
    user = response['Users'][0]
    userName = user['Username']
    logger.info('==============AdminUpdateUserAttributes===================')
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html
    logger.info("{0}, {1}".format(poolId, userName))
    COGNITO_CLIENT.admin_update_user_attributes(
      UserPoolId = poolId,
      Username = userName, 
      UserAttributes = [
        {
          'Name': 'custom:custom_name',
          'Value': 'test'
        }
      ]
    )
      
  except Exception as e:
    logger.exception(e)
    raise

  return poolId, userSub

