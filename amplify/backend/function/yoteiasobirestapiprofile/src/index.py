import os
import json
from datetime import date, datetime

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import boto3
COGNITO_CLIENT = boto3.client('cognito-idp')
S3 = boto3.client("s3")

S3_BUCKET_NAME   = os.environ['S3_BUCKET_NAME']

def handler(event, context):
  try:
    logger.info('=== START ===')
    logger.info(json.dumps(event, ensure_ascii=False, indent=2))
    
    method = event['httpMethod']
    
    retCode = 500
    retBody = ""
    if method == 'GET':
      retCode, retBody = get(event)
    elif method == 'PUT':
      retCode, retBody = put(event)
    elif method == 'DELETE':
      retCode, retBody = delete(event)
    else:
      raise ValueError('{0} is not supported.'.format(method))
    
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
      
def get(event):
  poolId, userName, pictureOrg, isAdmin = getUserInfo(event)
  logger.info('user info = {0}, {1}, {2} (admin={3})'.format(poolId, userName, pictureOrg, isAdmin))
  if not isAdmin:
    return 401, "need admin."
  
  result = None
  if "pathParameters" in event and event['pathParameters']:
    result = get_at(event, poolId)
  else:
    result = get_list(event, poolId)
    
  return 200, json.dumps(result, ensure_ascii=False, indent=2, default=json_serial)
    
def get_at(event, poolId):
  username = getPathParameter(event)
  response = COGNITO_CLIENT.list_users(
      UserPoolId = poolId, 
      Filter = "username = \"{0}\"".format(username)
  )
  user = response['Users'][0]
  retUser = createRetUser(user)
  return retUser
  
def getPathParameter(event):
  pathParameters = event['pathParameters']
  return pathParameters['proxy']
    
def get_list(event, poolId):
  count, search = getQueryParams(event)
  users = []
  
  response = COGNITO_CLIENT.list_users(
      UserPoolId = poolId, 
      Filter = "email ^= \"{0}\"".format(search)
  )
  users.extend(response['Users'])
  
  if search:
    response = COGNITO_CLIENT.list_users(
        UserPoolId = poolId, 
        Filter = "name ^= \"{0}\"".format(search)
    )
    users.extend(response['Users'])
  
  retUserList = []
  for user in users:
    tmp = list(filter(lambda data: data['username'] == user['Username'] , retUserList))
    if tmp:
      continue
    retUser = createRetUser(user)
    retUserList.append(retUser)
  
  return retUserList

def getQueryParams(event):
  count = 0
  search = ""
  queryPrm = event['queryStringParameters']
  if "count" in queryPrm:
    count = int(queryPrm['count'])
  if "search" in queryPrm:
    search = queryPrm['search']

  return count, search
  
def createRetUser(user):
  attributes = user['Attributes']
  retUser = {
    "username": user['Username'], 
    "name": get_value_from_attributes(attributes, 'custom:name'),
    "picture": get_value_from_attributes(attributes, 'custom:picture'),
    "email": get_value_from_attributes(attributes, 'custom:email'),
    "admin": get_value_from_attributes(attributes, 'custom:admin'),
    "comment": get_value_from_attributes(attributes, 'custom:comment'),
    "enabled": user['Enabled']
  }
  return retUser

def put(event):
  body = json.loads(event['body'])
  name, comment, picture = getParamFromBody(body)
  logger.info('name={0}, comment={1}, picture={2}'.format(name, comment, picture))

  poolId, userName, pictureOrg, isAdmin = getUserInfo(event)
  logger.info('user info = {0}, {1}, {2}'.format(poolId, userName, pictureOrg))

  updateUserInfo(poolId, userName, name, comment, picture)
  
  if picture and pictureOrg and picture != pictureOrg:
    removeOldPicture(pictureOrg)
    
  return 200, "success : {0}".format(userName)
    
def delete(event):
  pathParameters = event['pathParameters']
  userName = pathParameters['proxy']
  logger.info(userName)
  
  poolId, userNameFrom, pictureOrg, isAdmin = getUserInfo(event)
  logger.info('user info = {0}, {1}, {2}'.format(poolId, userNameFrom, pictureOrg))
  
  response = COGNITO_CLIENT.admin_delete_user(
    UserPoolId = poolId,
    Username = userName
  )
  
  removeOldPicture(pictureOrg)

  return 200, "success : {0}".format(userName)

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
  picture = None
  isAdmin = False

  try:
    poolId, userSub = getCognitoAuthenticationProviderFromEvent(event)
    response = COGNITO_CLIENT.list_users(
        UserPoolId = poolId,
        Filter = "sub = \"{0}\"".format(userSub)
    )
    userName = response['Users'][0]['Username']
    attributes = response['Users'][0]['Attributes']
    picture = get_value_from_attributes(attributes, 'custom:picture')
    admin = get_value_from_attributes(attributes, 'custom:admin')
    if admin == '1':
      isAdmin = True
    
  except Exception as e:
    logger.exception(e)
    raise

  return poolId, userName, picture, isAdmin
  
def getCognitoAuthenticationProviderFromEvent(event):
  poolId = event["requestContext"]["identity"]["cognitoAuthenticationProvider"].split(',')[0].split('/')[1]
  userSub = event["requestContext"]["identity"]["cognitoAuthenticationProvider"].split(',')[1].split(':')[2]
  return poolId, userSub  

def get_value_from_attributes(attributes, name):
  attr = list(filter(lambda data: data['Name'] == name , attributes))
  if attr and len(attr) == 1:
    return attr[0]['Value']
  
  return ''
  
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

def removeOldPicture(picture):
  try:
    S3.delete_object(Bucket=S3_BUCKET_NAME, Key=picture)
  except Exception as e:
    logger.exception(e)

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

