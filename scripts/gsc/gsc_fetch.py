# gsc_fetch.py
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
from datetime import date, timedelta
import time, sys, os

# ---------- CONFIGURA ESTO ----------
KEY_FILE = "service_account.json"           # nombre del JSON en tu carpeta
SITE = "https://studiorethinkibiza.com/"        # o "sc-domain:https://studiorethinkibiza.com/"
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
# -------------------------------------

end_date = date.today()
start_date = end_date - timedelta(days=30)

if not os.path.exists(KEY_FILE):
    print(f"ERROR: no se encuentra {KEY_FILE}. Coloca la clave en la carpeta del script.")
    sys.exit(1)

creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
service = build('searchconsole', 'v1', credentials=creds)

def fetch_page(start_row=0, page_size=25000):
    body = {
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat(),
        "dimensions": ["page", "query"],
        "rowLimit": page_size,
        "startRow": start_row
    }
    return service.searchanalytics().query(siteUrl=SITE, body=body).execute()

def resp_to_df(resp):
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
    return pd.DataFrame(data)

def fetch_all():
    all_df = pd.DataFrame()
    start_row = 0
    page_size = 25000
    while True:
        print(f"Fetching startRow={start_row}")
        resp = fetch_page(start_row=start_row, page_size=page_size)
        df = resp_to_df(resp)
        if df.empty:
            break
        all_df = pd.concat([all_df, df], ignore_index=True)
        if len(df) < page_size:
            break
        start_row += page_size
        time.sleep(1)
    return all_df

if __name__ == "__main__":
    print("Descargando GSC:", SITE, start_date, "->", end_date)
    df = fetch_all()
    if df.empty:
        print("No se han obtenido filas. Revisa permisos y que la propiedad tenga datos.")
        sys.exit(1)
    out = f"gsc_{start_date.isoformat()}_{end_date.isoformat()}.csv"
    df.to_csv(out, index=False)
    print("Exportado:", out, "Filas:", len(df))
