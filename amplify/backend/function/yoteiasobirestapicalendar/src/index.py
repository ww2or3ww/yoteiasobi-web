# --- coding: utf-8 ---
import os
import json
from datetime import date, datetime, timedelta

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import boto3
COGNITO_CLIENT = boto3.client('cognito-idp')

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
  id = getPathParameter(event)
  poolId, userName, email, isAdmin = getUserInfo(event)
  logger.info('user info = {0}, {1}, {2} (admin={3})'.format(poolId, userName, email, isAdmin))
  logger.info('calendarID={0}'.format(id))
  result = get_calender_events(id, email)
  return 200, json.dumps(result, ensure_ascii=False, indent=2, default=json_serial)

def getPathParameter(event):
  pathParameters = event['pathParameters']
  return pathParameters['proxy']
  
def get_calender_events(id, email):

    service = get_google_service_calendar()
    calendar_id = "{0}@group.calendar.google.com".format(id)
    
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
    emails = [email] * len(items)
    result = list(map(convert_data, items, emails))
    return result
    
def convert_data(data, email):
  ret = {}
  start, end, timed = get_date_or_datetime(data)
  ret = {
    "name": data["summary"], 
    "start": start, 
    "end": end, 
    "timed": timed,
    "isPublic": False,
    "isMine": False,
    "isMasked": False,
  }

  if "description" in data:
    ret["description"] = data["description"]
    ret = update_event_data(ret, email)
  else:
    ret = update_to_mask_data(ret)
  
  return ret

def update_event_data(data, email):
  description = data["description"]

  index = description.find("\n")
  if index >= 0:
    description = description[:index]
  else:
    index = description.lower().find("<br>")
    if index >= 0:
      description = description[:index]

  index = description.find("public")
  if index >= 0:
    data["isPublic"] = True
  else:
    index = description.find(email)
    if index >= 0:
      data["isMine"] = True
    else:
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
  
  calendar = json.loads(event['body'])
  calendar['email'] = email
  logger.info('calendar = {0}'.format(calendar))
  
  service = get_google_service_calendar()
  ret = service.events().insert(
    calendarId = "{0}@group.calendar.google.com".format(calendar["calendarId"]),
    body= {
        'summary': calendar["name"],
        'description': '{0}\n{1}'.format(calendar['email'], calendar['description']),
        'start': {
            'dateTime': calendar["start"]
        },
        'end': {
            'dateTime': calendar["end"]
        },
        #'attendees': [
        #  { 'email': 'ww2or3ww@gmail.com' }
        #],
    }
  ).execute()
  
  logger.info("insert ret = {0}".format(ret))
  
  return 200, "success : {0}".format(ret)

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
  poolId = event["requestContext"]["identity"]["cognitoAuthenticationProvider"].split(',')[0].split('/')[1]
  userSub = event["requestContext"]["identity"]["cognitoAuthenticationProvider"].split(',')[1].split(':')[2]
  return poolId, userSub  

def get_value_from_attributes(attributes, name):
  attr = list(filter(lambda data: data['Name'] == name , attributes))
  if attr and len(attr) == 1:
    return attr[0]['Value']
  
  return ''