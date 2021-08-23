import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import shutil
import io
from googleapiclient.http import MediaIoBaseDownload

# All permissions for my google drive
#* Any time you want to edit these scopes, you will need to delete the ../creds/token.json
#* file and re-authorize using oauth
SCOPES = ['https://www.googleapis.com/auth/drive']

def build_service():
    """Build service to access google drive

    :return: google drive api service
    :rtype: googleapiclient.discovery.Resource
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


def download_file(service, file_idi, file_name=None):
    """Use service.files().get_media to download non-google workspace files

    :param service: Service built with `build_service`
    :type service: googleapiclient.discovery.Resource
    :param file_id: Unique identifier for the file to be downloaded
    :type file_id: str
    :return: File name retrieved from the meta data of the file downloaded
    :rtype: str
    """
    # Setup request for the file
    request = service.files().get_media(fileId=file_id)
    # setup the file handler to recieve the byte stream
    fh = io.BytesIO()

    # the download utility 
    downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
    # continue to download until all bytes are recieved
    done = False
    while not done:
        status, done = downloader.next_chunk()

    # go to beginning of stream
    fh.seek(0)

    # get file name meta data to store file with same name, 
    # only executed if user did not provide a file name to store the file locally
    if file_name == None:
        file_name_results = service.files().get(fileId=file_id, fields='name').execute()
        file_name = file_name_results['name']
    # copy stream from file handler to local storage
    with open(file_name, 'wb') as f:
        shutil.copyfileobj(fh, f)
    
    return file_name

def download_files(service, file_ids):
    dwnloaded_files = []
    for file_id in file_ids:
        file_name = download_file(service, file_id)
        dwnloaded_files.append(file_name)
    return dwnloaded_files
    

    
if __name__ == '__main__':
    service = build_service()
    file_name = download_file(service, "<input file id here>")
    
