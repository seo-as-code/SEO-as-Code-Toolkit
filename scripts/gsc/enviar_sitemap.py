from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/webmasters']
SITE = "https://studiorethinkibiza.com/"
SITEMAP_URL = "https://studiorethinkibiza.com/sitemap.xml"
KEY_FILE = r"C:\Users\emami\proyecto_seo\credentials.json"

def get_creds():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(KEY_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)

    return creds

def enviar_sitemap():
    creds = get_creds()
    service = build('searchconsole', 'v1', credentials=creds)

    print("Enviando sitemap a GSC:", SITEMAP_URL)
    service.sitemaps().submit(siteUrl=SITE, feedpath=SITEMAP_URL).execute()
    print("Sitemap enviado correctamente.")

if __name__ == "__main__":
    enviar_sitemap()
