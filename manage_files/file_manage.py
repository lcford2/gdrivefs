import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import shutil
import io
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']

def build_service():
    """
    main()
    Shows basic usage of the Drive v3 API.
    Prints the names of ids of the first 10 files the user has access to.
    """

    creds = None

    # the file token.json stores the user's access and refresh tokens, and is 
    # created automatically when the authorization flow completes for the first time

    if os.path.exists('../creds/token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

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
    return service

def get_top_files(service, n=10):
    # Call the Drive v3 API
    results = service.files().list(
            pageSize=n, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

def download_file(service, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()

    downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
    done = False
    while not done:
        status, done = downloader.next_chunk()

    fh.seek(0)

    file_name_results = service.files().get(fileId=file_id, fields='name').execute()
    file_name = file_name_results['name']
    with open(file_name, 'wb') as f:
        shutil.copyfileobj(fh, f)
        
def parse_directory(service, dir_name):
    page_token = None

    while True:
        response = service.files().list(
            q=f"name = '{dir_name}'"
        )
    
if __name__ == '__main__':
    service = build_service()
    # download_file(service, '1EmNSR9iyKwJNhpEplKlxFhpWsDtn4FQP')
    parse_directory(service)
