from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import pandas as pd
import pickle
import os
import json

PROPERTY_ID = "286215654"  # tu Property ID de GA4
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
CREDENTIALS_FILE = r"C:\Users\emami\Downloads\client_secret_950684690625-44usnmdsams5guknq98q8en33780ac7v.apps.googleusercontent.com.json"
TOKEN_FILE = "ga_token.pickle"

def get_ga4_creds():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds_data = pickle.load(f)
            if isinstance(creds_data, str):
                creds_data = json.loads(creds_data)
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(json.loads(creds.to_json()), f)
    return creds

def main():
    creds = get_ga4_creds()
    client = BetaAnalyticsDataClient(credentials=creds)

    # 🔧 Ajuste para propiedades web
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[{"name": "pageTitle"}, {"name": "pagePath"}],
        metrics=[{"name": "sessions"}, {"name": "totalUsers"}, {"name": "engagedSessions"}],
        date_ranges=[{"start_date": "2024-01-01", "end_date": "today"}],
        limit=10000,
    )

    response = client.run_report(request)

    rows = []
    for row in response.rows:
        rows.append({
            "pageTitle": row.dimension_values[0].value,
            "pagePath": row.dimension_values[1].value,
            "sessions": row.metric_values[0].value,
            "totalUsers": row.metric_values[1].value,
            "engagedSessions": row.metric_values[2].value
        })

    df = pd.DataFrame(rows)
    out = "ga4_report_last_30_days.csv"
    df.to_csv(out, index=False)
    print("✅ Exportado:", out, "Filas:", len(df))

if __name__ == "__main__":
    main()


