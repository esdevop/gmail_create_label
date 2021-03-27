import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import traceback
import logging

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.labels']

# Temporary
color_dict = {
    'fail':{'textColor': '#8a1c0a', 'backgroundColor': '#f2b2a8'},
    'pending':{'textColor': '#ffffff', 'backgroundColor': '#c2c2c2'},
    'success':{'textColor': '#0b4f30', 'backgroundColor': '#b3efd3'}
}

def get_service():
    """
    Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # Another option to ignore google cache logging issue
    # service = build('gmail', 'v1', credentials=creds, cache_discovery=False)
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_labels(service):
    list_of_labels = service.users().labels().list(userId='me').execute()
    return list_of_labels.get('labels')

def define_label(name, color=color_dict['pending'], mlv="show", llv="labelShow", tp="user"):
    label = dict()
    label["messageListVisibility"] = mlv
    label["labelListVisibility"] = llv
    label["type"] = tp
    label["color"] = color
    label["name"] = name
    return label

def add_label_to_gmail(service, label):
    try:
        created_label = service.users().labels().create(userId='me',
                                                        body=label).execute()
        return created_label
    except Exception as e:
        traceback.print_exc()
        logging.error(e)

def main():
    with open('logs/debug.log', 'w'):
        logging.basicConfig(filename='logs/debug.log', encoding='utf-8', level=logging.DEBUG)
    service = get_service()
    new_label = define_label("Job Applications/test", color=color_dict["fail"])
    added_label = add_label_to_gmail(service, new_label)


if __name__ == '__main__':
    main()