# adapted from https://developers.google.com/gmail/api/quickstart/python
# and https://developers.google.com/gmail/api/guides/sending#python 

import base64
import os
import traceback

from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

service = None

def init():
    global service

    try:
        creds = None

        if (os.path.exists("token.json")):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", scopes=SCOPES,
                    redirect_uri="http://tasks312.me/oauth"
                )

                creds = flow.run_local_server(port=8080, login_hint='tasks.312.cse@gmail.com')

            with open("token.json", "w") as token:
                cjson = creds.to_json()
        
                # sometimes they just don't give us a refresh token.
                # really cool behavior, thanks Google
                if "refresh_token" not in cjson:
                    # python sucks, therefore, make a string copy
                    cjson = cjson[:-1]
                    cjson += ", \"refresh_token\": \"\"}"

                token.write(cjson)

        service = build("gmail", "v1", credentials=creds)
    except Exception as e:
        traceback.print_exc()

def sendMessage(to: str, body: str, subject: str = "Verify Email"):
    global service
    
    if (service == None):
        init()

    if (service == None):
        return None

    message = EmailMessage()

    message.set_content(body)

    message["To"] = to
    message["From"] = "tasks.312.cse@gmail.com"
    message["Subject"] = subject

    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()

    payload = {"raw": encoded}

    try:
        msg = (
            service.users().messages().send(userId="me", body=payload).execute()
        )

    except HttpError as error:
        print(f"Email Error: {error}", flush=True)
        msg = None

    return msg