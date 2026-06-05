from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import sys

SCOPES = ['https://www.googleapis.com/auth/webmasters']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "Credentials", "credentials.json")
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

from lib.site_config import gsc_site_url, sitemap_url  # noqa: E402


def get_creds():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)

    return creds


def enviar_sitemap():
    site = gsc_site_url()
    feed = sitemap_url()
    creds = get_creds()
    service = build('searchconsole', 'v1', credentials=creds)

    print("Enviando sitemap a GSC:", feed)
    service.sitemaps().submit(siteUrl=site, feedpath=feed).execute()
    print("Sitemap enviado correctamente.")


if __name__ == "__main__":
    enviar_sitemap()
