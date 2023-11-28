# adapted from https://developers.google.com/gmail/api/quickstart/python
# and https://developers.google.com/gmail/api/guides/sending#python 

import base64

from google.auth.transport.requests import Request
from email.message import EmailMessage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

service = None

def init():
    global service

    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    credentials = flow.run_local_server(port=0)

    service = build("gmail", "v1", credentials=credentials)

def sendMessage(to: str, body: str, subject: str = "Verify Email"):
    if (service == None):
        init()

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