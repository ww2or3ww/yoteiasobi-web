# --- coding: utf-8 ---
import os
import json
from datetime import date, datetime

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
  result = get_calender_events(id)
  return 200, json.dumps(result, ensure_ascii=False, indent=2, default=json_serial)

def getPathParameter(event):
  pathParameters = event['pathParameters']
  return pathParameters['proxy']
  
def get_calender_events(id):

    service = get_google_service_calendar()
    calendar_id = "{0}@group.calendar.google.com".format(id)
    
    events_result = service.events().list(
      calendarId = calendar_id,
      timeMin = "2021-02-09T11:00:00+09:00",
      timeMax = "2021-02-11T13:00:00+09:00",
      singleEvents=True,
      orderBy='startTime',
      q='ww2or3ww@gmail.com'
      ).execute()
    items = events_result.get("items", [])
    logger.info(json.dumps(items, ensure_ascii=False, indent=2, default=json_serial))
    
    result = []
    for data in items:
      tmp = {}
      start, end, timed = get_date_or_datetime(data)
      result.append(
        {
          "name": data["summary"], 
          "start": start, 
          "end": end, 
          "timed": timed
        }
      )
    return result

def get_date_or_datetime(data):
  if "date" in data["start"]:
    return data["start"]["date"], data["end"]["date"], False
  elif "dateTime" in data["start"]:
    return data["start"]["dateTime"], data["end"]["dateTime"], True


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

