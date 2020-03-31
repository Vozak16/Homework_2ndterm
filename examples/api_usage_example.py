from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
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

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', labelIds=['IMPORTANT']).execute()
    message = results.get('messages', [])[0]
    msg = service.users().messages().get(userId='me', id=message['id']).execute()

    print("Message: " + msg['snippet'])
    for i in range(len(msg['payload']['headers'])):
        if msg['payload']['headers'][i]['name'] == 'From':
            print("From: " + msg['payload']['headers'][i]['value'])
        if msg['payload']['headers'][i]['name'] == 'Date':
            print("Date: " + msg['payload']['headers'][i]['value'])
            break
    # creating the json file
    messages = results.get('messages', [])

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        print("\n")
        break

    with open("api_dict_example.json", 'w') as json_file:
        json.dump(msg, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
