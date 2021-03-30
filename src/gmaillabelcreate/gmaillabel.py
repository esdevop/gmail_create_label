import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import traceback
import logging
from itertools import compress
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.labels']

# Attributes
PATH_TO_LIB = os.path.join(os.getcwd(), "src/gmaillabelcreate")
FILENAME_LABEL_COLOR = "label_color.json"

# Text of errors
VALUE_ERROR_DEFINE_LABEL_TEXT = "Wrong arguments: {}. The value must be a string"
VALUE_ERROR_DEFINE_LABEL_COLOR_TEXT = "Missing arguments in 'color': {}"

# Temporary
with open(os.path.join(PATH_TO_LIB, FILENAME_LABEL_COLOR), "r") as f:
    color_dict = json.load(f)

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

    value_names_lst = ["name", "mlv", "llv", "tp"]
    check_lst = list(map(lambda parameter: isinstance(parameter, str), (name, mlv, llv, tp))) 
    if all(check_lst):
        pass
    else:
        error_message = VALUE_ERROR_DEFINE_LABEL_TEXT.format(
            list(compress(value_names_lst, [not element for element in check_lst]))
        )
        raise ValueError(error_message)

    if not isinstance(color, dict):
        raise ValueError("color of the lable must be a dictinary")
    else:
        value_names_lst = ["textColor", "backgroundColor"]
        test_lst = [key_list for key_list in color.keys()]
        check_lst = list(map(lambda parameter: elementinlist(parameter, test_lst), (*value_names_lst, )))
        if all(check_lst):
            pass
        else:
            print(test_lst)
            print(check_lst)
            error_message = VALUE_ERROR_DEFINE_LABEL_COLOR_TEXT.format(
                list(compress(value_names_lst, [not element for element in check_lst]))
            )
            raise ValueError(error_message)

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

def find_label_by(targetgroup, targetname, service):
    label_lst = get_labels(service)
    for element in label_lst:
        try:
            if targetname in element[targetgroup]:
                return element
        except:
            pass
    return None

def update_label(targetgroup, targetname, parameter, service):
    if not isinstance(parameter, dict):
        raise ValueError("A new parameter must be a dictinary")
    label = find_label_by(targetgroup, targetname, service)
    for key in parameter:
        label[key] = parameter[key]
    return label


def update_label_in_gmail(targetgroup, targetname, parameter, service):
    label = update_label(targetgroup, targetname, parameter, service)
    try:
        updated_label = service.users().labels().update(userId='me',
                                                        id=label["id"],
                                                        body=label).execute()
        return updated_label
    except Exception as e:
        traceback.print_exc()
        logging.error(e)


def elementinlist(element, lst):
    if isinstance(lst, list):
        pass
    else:
        raise ValueError("Wrong {}.The input parameter must be a list.".format(lst))
    return element in lst

def main():
    with open('logs/debug.log', 'w'):
        logging.basicConfig(filename='logs/debug.log', encoding='utf-8', level=logging.DEBUG)
    service = get_service()
    new_label = define_label("Job Applications/test", color=color_dict["pending"])
    #added_label = add_label_to_gmail(service, new_label)
    updated_label = update_label_in_gmail("name", "test", {"color":color_dict["pending"]}, service)


if __name__ == '__main__':
    #main()

    print(color_dict)