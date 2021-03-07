import os
import json

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
  try:
    logger.info('=== START ===')
    logger.info(json.dumps(event, ensure_ascii=False, indent=2))
    method = event['httpMethod']
    
    retCode = 200
    retBody = "calendar {0} done!!".format(method)

    return {
      "statusCode": retCode,
      "body": retBody,
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
      