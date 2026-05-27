from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from datetime import date, timedelta
import pandas as pd
import os, sys

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
SITE = "https://studiorethinkibiza.com/"

def get_creds():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            CREDENTIALS_PATH = os.path.join(BASE_DIR, "Credentials", "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)
    return creds

def main():
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    creds = get_creds()
    service = build('searchconsole', 'v1', credentials=creds)

    body = {
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat(),
        "dimensions": ["page", "query"],
        "rowLimit": 25000
    }

    print("Consultando GSC:", SITE, start_date, "->", end_date)
    resp = service.searchanalytics().query(siteUrl=SITE, body=body).execute()
    rows = resp.get("rows", [])
    data = []
    for r in rows:
        keys = r.get("keys", [])
        data.append({
            "page": keys[0] if len(keys) > 0 else None,
            "query": keys[1] if len(keys) > 1 else None,
            "clicks": r.get("clicks", 0),
            "impressions": r.get("impressions", 0),
            "ctr": r.get("ctr", 0),
            "position": r.get("position", 0)
        })
    df = pd.DataFrame(data)
    if df.empty:
        print("No se han obtenido filas.")
        sys.exit(0)
    out = f"gsc_oauth_{start_date.isoformat()}_{end_date.isoformat()}.csv"
    df.to_csv(out, index=False)
    print("Exportado:", out, "Filas:", len(df))

if __name__ == "__main__":
    main()


