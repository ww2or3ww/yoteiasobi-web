import os
import json
import datetime
import stripe

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import boto3
COGNITO_CLIENT = boto3.client('cognito-idp')

ENVVAL_STRIPE_SECRET_KEY            = os.environ['ENVVAL_STRIPE_SECRET_KEY']
ENVVAL_STRIPE_DESCRIPTION_CAPTION   = os.environ['ENVVAL_STRIPE_DESCRIPTION_CAPTION']
DEF_STRIPE_CURRENCY                 = 'JPY'

def handler(event, context):
  try:
    logger.info('=== START ===')
    logger.info(json.dumps(event, ensure_ascii=False, indent=2))
    
    body = json.loads(event['body'])
    token = body['token']
    amount = body['amount']
    logger.info('token={0}, amount={1}({2})'.format(token, amount, DEF_STRIPE_CURRENCY))
    
    name, email = getUserInfo(event)
    description= ENVVAL_STRIPE_DESCRIPTION_CAPTION + '{0}:{1}'.format(name, email)
    
    stripe.api_key = ENVVAL_STRIPE_SECRET_KEY
    charge = stripe.Charge.create(
      amount = amount,
      currency = DEF_STRIPE_CURRENCY,
      description = description,
      source = token,
    )
    logger.info(charge)

    message = "{0}:{1}({2})".format(charge['description'], charge['amount'], charge['currency'])
    body = {
        "message": message
    }
    logger.info(message)
    logger.info('=== DONE ===')
    
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
  name = None
  email = None

  try:
    poolId = event["requestContext"]["identity"]["cognitoAuthenticationProvider"].split(',')[0].split('/')[1]
    userSub = event["requestContext"]["identity"]["cognitoAuthenticationProvider"].split(',')[1].split(':')[2]
    logger.info('user info = {0}, {1}'.format(poolId, userSub))

    response = COGNITO_CLIENT.list_users(
        UserPoolId = poolId,
        Filter = "sub = \"{0}\"".format(userSub)
    )
    logger.info(response)
    
    userName = response['Users'][0]['Username']
    attributes = response['Users'][0]['Attributes']
    name = get_value_from_attributes(attributes, 'custom:name')
    email = get_value_from_attributes(attributes, 'email')
    
    logger.info("poolId = {0}, sub = {1}, userName = {2}".format(poolId, userSub, userName))
    logger.info("name = {0}, email = {1}".format(name, email))

  except Exception as e:
    logger.exception(e)
    raise

  return name, email

def get_value_from_attributes(attributes, name):
  attr = list(filter(lambda data: data['Name'] == name , attributes))
  if attr and len(attr) == 1:
    return attr[0]['Value']
  
  return ''