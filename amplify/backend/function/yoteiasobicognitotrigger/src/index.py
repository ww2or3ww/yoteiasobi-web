import os
import json
import datetime
import requests

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import boto3
COGNITO_CLIENT = boto3.client('cognito-idp')
S3 = boto3.client("s3")
S3_BUCKET_NAME   = os.environ['S3_BUCKET_NAME']

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

    triggerSource = event["triggerSource"]
    if triggerSource == "PostConfirmation_ConfirmSignUp":
      attributes = response['Users'][0]['Attributes']
      updateCustomAttributes(userPoolId, userName, attributes)
      
    if triggerSource == "PostAuthentication_Authentication":
      updateIsAdmin(userPoolId, userName)

  except Exception as e:
    logger.exception(e)

  return event

def get_value_from_attributes(attributes, name):
  attr = list(filter(lambda data: data['Name'] == name , attributes))
  if attr and len(attr) == 1:
    return attr[0]['Value']
  
  return ''
  
def updateCustomAttributes(userPoolId, userName, attributes):
  name = get_value_from_attributes(attributes, 'name')
  email = get_value_from_attributes(attributes, 'email')
  picture = get_value_from_attributes(attributes, 'picture')

  custom_name = get_value_from_attributes(attributes, 'custom:name')
  custom_picture = get_value_from_attributes(attributes, 'custom:picture')
  
  update_attributes = []
  if not custom_name and name:
    update_attributes.append({
      'Name': 'custom:name',
      'Value': name
    })
  if not custom_picture and picture:
    key = uploadPictureToStorage(userName, picture)
    update_attributes.append({
      'Name': 'custom:picture',
      'Value': key
    })
  logger.info(update_attributes)
    
  if len(update_attributes) > 0:
    COGNITO_CLIENT.admin_update_user_attributes(
      UserPoolId = userPoolId,
      Username = userName, 
      UserAttributes = update_attributes
    )

def uploadPictureToStorage(userName, picture):
  try:
    response = requests.get(picture, stream=True)
    contentType = response.headers['Content-Type']
    contentDisposition = response.headers['Content-Disposition']
    ATTRIBUTE = 'filename='
    fileName = contentDisposition[contentDisposition.find(ATTRIBUTE) + len(ATTRIBUTE):]
    fileName = fileName.strip('"')
    root, ext = os.path.splitext(fileName)
    key = "public/profile/{0}{1}".format(userName, ext)
    S3.upload_fileobj(response.raw, S3_BUCKET_NAME, key)
    return key
    
  except Exception as e:
    logger.exception(e)
    raise

def updateIsAdmin(userPoolId, userName):
  try:
    response = COGNITO_CLIENT.admin_list_groups_for_user(
      UserPoolId = userPoolId,
      Username = userName
    )
    groups = response['Groups']
    group = list(filter(lambda data: data['GroupName'] == 'Admin' , groups))
    admin = "0"
    if group:
      admin = "1"
    update_attributes = [
        {
        'Name': 'custom:admin',
        'Value': admin
        }
      ]
    COGNITO_CLIENT.admin_update_user_attributes(
      UserPoolId = userPoolId,
      Username = userName, 
      UserAttributes = update_attributes
    )
  except Exception as e:
    logger.exception(e)
