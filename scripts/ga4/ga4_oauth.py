from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import pickle
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
CREDENTIALS_CANDIDATES = [
    os.path.join(BASE_DIR, "Credentials", "ga_credentials.json"),
    os.path.join(BASE_DIR, "Credentials", "credentials.json"),
]
TOKEN_FILE = os.path.join(BASE_DIR, "ga_token.pickle")


def credentials_file() -> str:
    for path in CREDENTIALS_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        "No se encontro ga_credentials.json ni credentials.json en Credentials/"
    )


def main():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds_data = pickle.load(f)
            if isinstance(creds_data, str):
                creds_data = json.loads(creds_data)
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file(), SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(json.loads(creds.to_json()), f)

    print(f"OK: token guardado en {TOKEN_FILE}")
    print("Siguiente paso: py .\\scripts\\ga4\\ga4_extract.py")


if __name__ == "__main__":
    main()
