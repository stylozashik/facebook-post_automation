import os
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Facebook authentication function
def authenticate_facebook():
    # Replace with your Facebook authentication code
    access_token = "YOUR_FACEBOOK_ACCESS_TOKEN"
    return access_token

# Google Drive authentication function
def authenticate_drive():
    # Define scopes and credentials file
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    CLIENT_SECRET_FILE = 'credentials.json'
    
    # Authenticate with Google Drive
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

# Function to list video files and extract metadata
def list_and_extract(service):
    results = service.files().list(q="mimeType='video/*'").execute()
    files = results.get('files', [])
    return files

# Function to post to Facebook
def post_to_facebook(access_token, message):
    url = "https://graph.facebook.com/me/feed"
    data = {
        "message": message,
        "access_token": access_token
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Post successful!")
    else:
        print(f"Failed to post: {response.json()}")

def main():
    # Authenticate with Facebook
    facebook_access_token = authenticate_facebook()

    # Authenticate with Google Drive
    drive_creds = authenticate_drive()
    service = build('drive', 'v3', credentials=drive_creds)

    # List video files and extract metadata
    video_files = list_and_extract(service)
    
    for file in video_files:
        title = file['name']
        description = file.get('description', '')
        print(f"Title: {title}, Description: {description}")
        
        # Post to Facebook using extracted metadata
        message = f"New video: {title}\nDescription: {description}"
        post_to_facebook(facebook_access_token, message)

if __name__ == '__main__':
    main()
