import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """
    Shows basic usage of the Drive v3 API.
    Prints the names of ids of the first 10 files the user has access to.
    """

    creds = None

    # the file token.json stores the user's access and refresh tokens, and is 
    # created automatically when the authorization flow completes for the first time

    if os.path.exists('../creds/token.json'):
        creds = Credentials.from_authorized_user_file('../creds/token.json', SCOPES)

    # if there are no (valid) credentials, ask the user to login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    '../creds/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('../creds/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
     
if __name__ == '__main__':
    main()
