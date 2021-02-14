import json
import datetime

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import boto3
COGNITO_CLIENT = boto3.client('cognito-idp')

def handler(event, context):
  try:
    logger.info(json.dumps(event, ensure_ascii=False, indent=2))

    userPoolId = event["userPoolId"]
    userName = event["userName"]
    response = COGNITO_CLIENT.list_users(
        UserPoolId = userPoolId,
        Filter = "username = \"{0}\"".format(userName)
    )
    logger.info(response)

    attributes = response['Users'][0]['Attributes']
    name = get_value_from_ttributes(attributes, 'name')
    email = get_value_from_ttributes(attributes, 'email')
    picture = get_value_from_ttributes(attributes, 'picture')

    custom_name = get_value_from_ttributes(attributes, 'custom:name')
    custom_email = get_value_from_ttributes(attributes, 'custom:email')
    custom_picture = get_value_from_ttributes(attributes, 'custom:picture')
    
    update_attributes = []
    if not custom_name and name:
      update_attributes.append({
        'Name': 'custom:name',
        'Value': name
      })
    if not custom_email and email:
      update_attributes.append({
        'Name': 'custom:email',
        'Value': email
      })
    if not custom_picture and picture:
      update_attributes.append({
        'Name': 'custom:picture',
        'Value': picture
      })
    logger.info(update_attributes)
      
    if len(update_attributes) > 0:
      COGNITO_CLIENT.admin_update_user_attributes(
        UserPoolId = userPoolId,
        Username = userName, 
        UserAttributes = update_attributes
      )

  except Exception as e:
      logger.exception(e)

  return event

def get_value_from_ttributes(attributes, name):
  attr = list(filter(lambda data: data['Name'] == name , attributes))
  if attr and len(attr) == 1:
    return attr[0]['Value']
  
  return ''