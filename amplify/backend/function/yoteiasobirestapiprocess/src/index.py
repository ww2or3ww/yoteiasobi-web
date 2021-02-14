import os
import json
import datetime
import stripe

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENVVAL_STRIPE_SECRET_KEY    = os.environ['ENVVAL_STRIPE_SECRET_KEY']

def handler(event, context):
  try:
    logger.info('===============================')
    logger.info(json.dumps(event, ensure_ascii=False, indent=2))
    logger.info(event['body'])
    body = json.loads(event['body'])
    token = body['token']
    amount = body['amount']
    logger.info('token={0}, amount={1}'.format(token, amount))
    stripe.api_key = ENVVAL_STRIPE_SECRET_KEY
    charge = stripe.Charge.create(
      amount=amount,
      currency='JPY',
      description='Example charge',
      source=token,
    )

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
