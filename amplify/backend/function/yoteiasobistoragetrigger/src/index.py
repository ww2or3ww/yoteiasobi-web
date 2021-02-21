import json

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
  try:
    logger.info('=== START ===')
    logger.info(json.dumps(event, ensure_ascii=False, indent=2))

  except Exception as e:
      logger.exception(e)

  return {
    'message': 'Hello from your new Amplify Python lambda!'
  }
