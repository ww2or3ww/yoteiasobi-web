# --- coding: utf-8 ---
import os
import json
from datetime import date, datetime, timedelta

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import boto3
COGNITO_CLIENT = boto3.client('cognito-idp')
S3_RES = boto3.resource('s3')
S3_BUCKET_NAME   = os.environ['S3_BUCKET_NAME']
from boto3.dynamodb.conditions import Key
DYNAMODB = boto3.resource('dynamodb')
DYNAMODB_TABLE_NAME   = os.environ['DYNAMODB_TABLE_NAME']

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

GCP_CLIENT_EMAIL            = os.environ['GCP_CLIENT_EMAIL']
GCP_PRIVATE_KEY_ID          = os.environ['GCP_PRIVATE_KEY_ID']
GCP_PRIVATE_KEY             = os.environ['GCP_PRIVATE_KEY']
GCP_CLIENT_ID               = os.environ['GCP_CLIENT_ID']
GCP_CLIENT_X509_CERT_URL    = os.environ['GCP_CLIENT_X509_CERT_URL']

def handler(event, context):
  try:
    logger.info('=== START ===')
    logger.info(json.dumps(event, ensure_ascii=False, indent=2))
    method = event['httpMethod']
    
    retCode = 500
    retBody = ""
    if method == 'GET':
      retCode, retBody = get(event)
    elif method == 'POST':
      retCode, retBody = post(event)
    else:
      raise ValueError('{0} is not supported.'.format(method))

    logger.info(retBody)

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
  calendar_id = getPathParameter(event)
  poolId, userName, email, isAdmin = getUserInfo(event)
  logger.info('user info = {0}, {1}, {2} (admin={3})'.format(poolId, userName, email, isAdmin))
  logger.info('calendarID={0}'.format(calendar_id))
  result = get_calendar_events(calendar_id, userName, email)
  return 200, json.dumps(result, ensure_ascii=False, indent=2, default=json_serial)

def getPathParameter(event):
  pathParameters = event['pathParameters']
  return pathParameters['proxy']
  
def get_calendar_events(calendar_id, userName, email):

    service = get_google_service_calendar()
    
    dt_now = datetime.utcnow()
    dt_from = dt_now + timedelta(weeks=(-1*4*3))
    dt_to = dt_now + timedelta(weeks=(4*3))

    events_result = service.events().list(
      calendarId = calendar_id,
      timeMin = dt_from.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
      timeMax = dt_to.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
      singleEvents=True,
      orderBy='startTime',
      # q=email
      ).execute()
    items = events_result.get("items", [])
    # logger.info(json.dumps(items, ensure_ascii=False, indent=2, default=json_serial))
    
    option = {
      "email": email, 
      "isOwnCalendar": check_is_own_calendar(calendar_id, userName)
    }
    options = [option] * len(items)
    result = list(map(convert_data, items, options))
    return result

def check_is_own_calendar(calendar_id, userName):
  DYNAMODB_TABLE = DYNAMODB.Table(DYNAMODB_TABLE_NAME)
  response = DYNAMODB_TABLE.query(
    KeyConditionExpression=Key('calendarId').eq(calendar_id)
  )
  ret_data = response['Items']
  owner = ret_data[0]["owner"]
  return owner == userName

def convert_data(data, option):
  email = option["email"]
  isOwnCalendar = option["isOwnCalendar"]
  ret = {}
  start, end, timed = get_date_or_datetime(data)

  name = "No Title"
  if "summary" in data:
    name = data["summary"]
    
  ret = {
    "name": name, 
    "start": start, 
    "end": end, 
    "timed": timed,
    "isPublic": False,
    "isProtected": False,
    "isMine": False,
    "isMasked": False,
  }

  if "description" in data:
    ret["description"] = data["description"]

  if isOwnCalendar:
    ret["isPublic"] = True
  elif "description" in ret:
    ret = update_event_data(ret, email)
  else:
    ret = update_to_mask_data(ret)
  
  return ret

def update_event_data(data, email):
  description = ""
  if "description" in data:
    description = data["description"].lower()
    index = description.find("\n")
    if index >= 0:
      description = description[:index]
    else:
      index = description.lower().find("<br>")
      if index >= 0:
        description = description[:index]

  isVisible = False

  index = description.find("public")
  if index >= 0:
    data["isPublic"] = True
    isVisible= True

  index = description.find("protected")
  if index >= 0 and email != None:
    data["isProtected"] = True
    isVisible= True

  index = description.find(email)
  if index >= 0:
    data["isMine"] = True
    isVisible = True
    
  if isVisible == False:
    data = update_to_mask_data(data)

  return data

def update_to_mask_data(data):
  data["name"] = "***"
  data["description"] = "***"
  data["isMasked"] = True
  return data

def get_date_or_datetime(data):
  if "date" in data["start"]:
    return data["start"]["date"], data["start"]["date"], False
  elif "dateTime" in data["start"]:
    return data["start"]["dateTime"], data["end"]["dateTime"], True

def post(event):
  poolId, userName, email, isAdmin = getUserInfo(event)
  logger.info('user info = {0}, {1}, {2} (admin={3})'.format(poolId, userName, email, isAdmin))
  
  data = json.loads(event['body'])
  type = data['type']
  
  if type == 'calendar_event':
    ret = post_calendar_event(data, email)
  elif type == 'calendar_image':
    ret = post_calendar_image(data)
  
  logger.info("insert ret = {0}".format(ret))
  
  return 200, "success : {0}".format(ret)
  
def post_calendar_event(data, email):
  data['email'] = email
  logger.info('data = {0}'.format(data))
  
  service = get_google_service_calendar()
  ret = service.events().insert(
    calendarId = data["calendarId"],
    body= {
        'summary': data["name"],
        'description': '{0}\n{1}'.format(data['email'], data['description']),
        'start': {
            'dateTime': data["start"]
        },
        'end': {
            'dateTime': data["end"]
        },
        #'attendees': [
        #  { 'email': 'ww2or3ww@gmail.com' }
        #],
    }
  ).execute()
  return ret
  
def post_calendar_image(data):
  ret = S3_RES.Object(S3_BUCKET_NAME, data["destKey"]).copy_from(CopySource={'Bucket': S3_BUCKET_NAME, 'Key': data["srcKey"]})
  return ret

def get_google_service_calendar():
    key_file_dict = {
      "type": "service_account",
      "project_id": "yoteiasobi",
      "private_key_id": "",
      "private_key": "",
      "client_email": "",
      "client_id": "",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": ""
    }
    key_file_dict["private_key_id"] = GCP_PRIVATE_KEY_ID
    key_file_dict["private_key"] = GCP_PRIVATE_KEY.replace("\\n", "\n")
    key_file_dict["client_email"] = GCP_CLIENT_EMAIL
    key_file_dict["client_id"] = GCP_CLIENT_ID
    key_file_dict["client_x509_cert_url"] = GCP_CLIENT_X509_CERT_URL

    scope = ['https://www.googleapis.com/auth/calendar']
    api_name = "calendar"
    api_version = "v3"
    service = get_google_service(key_file_dict, scope, api_name, api_version)
    return service

def get_google_service(key_file_dict, scope, api_name, api_version):
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict=key_file_dict, scopes=scope)
    return build(api_name, api_version, credentials=credentials, cache_discovery=False)

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def getUserInfo(event):
  poolId = None
  userName = None
  email = None
  isAdmin = False

  try:
    poolId, userSub = getCognitoAuthenticationProviderFromEvent(event)
    if poolId == None:
      return None, None, None, False
      
    response = COGNITO_CLIENT.list_users(
        UserPoolId = poolId,
        Filter = "sub = \"{0}\"".format(userSub)
    )
    logger.info(response)
    userName = response['Users'][0]['Username']
    attributes = response['Users'][0]['Attributes']
    email = get_value_from_attributes(attributes, 'email')
    admin = get_value_from_attributes(attributes, 'custom:admin')
    if admin == '1':
      isAdmin = True
    
  except Exception as e:
    logger.exception(e)
    raise

  return poolId, userName, email, isAdmin


def getCognitoAuthenticationProviderFromEvent(event):
  if event["requestContext"]["identity"]["cognitoAuthenticationProvider"] == None:
    return None, None
  
  poolId = event["requestContext"]["identity"]["cognitoAuthenticationProvider"].split(',')[0].split('/')[1]
  userSub = event["requestContext"]["identity"]["cognitoAuthenticationProvider"].split(',')[1].split(':')[2]
  return poolId, userSub  

def get_value_from_attributes(attributes, name):
  attr = list(filter(lambda data: data['Name'] == name , attributes))
  if attr and len(attr) == 1:
    return attr[0]['Value']
  
  return ''