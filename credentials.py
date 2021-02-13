import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from config.config import Config

def get_credentials_from_file():
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token:
            return pickle.load(token)

def get_credentials(config: Config):
    credentials = get_credentials_from_file()
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    if not credentials:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
            config.client_secrets_file,
            scopes=config.scopes
        )
        flow.run_local_server(
            port=config.port,
            prompt='consent',
            authorization_prompt_message=''
        )
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)
    return credentials
