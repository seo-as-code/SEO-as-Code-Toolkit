import os
import pickle
import json
import pandas as pd
from google.oauth2.credentials import Credentials
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from google.api_core.exceptions import PermissionDenied

# ============================
# CONFIGURACIÓN DE RUTAS
# ============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_DIR = os.path.join(BASE_DIR, "Credentials")
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

GA_CREDENTIALS_PATH = os.path.join(CREDENTIALS_DIR, "ga_credentials.json")
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
DEFAULT_PROPERTY_ID = os.getenv("GA4_PROPERTY_ID", "362766096")

# ============================
# CARGAR TOKEN
# ============================

def load_credentials():
    token_candidates = [
        os.path.join(SCRIPT_DIR, "ga_token.pickle"),
        os.path.join(BASE_DIR, "ga_token.pickle"),
        os.path.join(CREDENTIALS_DIR, "ga_token.pickle"),
        os.path.join(os.getcwd(), "ga_token.pickle"),
    ]
    token_path = next((path for path in token_candidates if os.path.exists(path)), None)

    if not token_path:
        searched_paths = "\n".join(f" - {path}" for path in token_candidates)
        raise FileNotFoundError(
            "❌ No se encontró ga_token.pickle.\n"
            "Ejecuta primero scripts/ga4/ga4_oauth.py para generarlo.\n"
            f"Rutas buscadas:\n{searched_paths}"
        )

    with open(token_path, "rb") as token_file:
        token_data = pickle.load(token_file)

    if isinstance(token_data, Credentials):
        return token_data
    if isinstance(token_data, str):
        token_data = json.loads(token_data)
    if isinstance(token_data, dict):
        return Credentials.from_authorized_user_info(token_data, SCOPES)

    raise ValueError(f"Formato de token no soportado en: {token_path}")

# ============================
# EXTRAER DATOS GA4
# ============================

def extract_ga4(property_id=DEFAULT_PROPERTY_ID):
    creds = load_credentials()
    client = BetaAnalyticsDataClient(credentials=creds)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="date"), Dimension(name="sessionSourceMedium")],
        metrics=[Metric(name="sessions"), Metric(name="totalUsers"), Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date="30daysAgo", end_date="yesterday")],
    )

    try:
        response = client.run_report(request)
    except PermissionDenied as exc:
        raise PermissionDenied(
            f"403 sin permisos para properties/{property_id}. "
            "Verifica que el email autenticado tenga acceso a esa propiedad GA4 "
            "o usa el property correcto en GA4_PROPERTY_ID."
        ) from exc

    rows = []
    for row in response.rows:
        rows.append(
            {
                "date": row.dimension_values[0].value,
                "source_medium": row.dimension_values[1].value,
                "sessions": int(row.metric_values[0].value),
                "users": int(row.metric_values[1].value),
                "pageviews": int(row.metric_values[2].value),
            }
        )

    df = pd.DataFrame(rows)
    os.makedirs(DATA_DIR, exist_ok=True)
    output_path = os.path.join(DATA_DIR, "ga4_traffic_last30days.csv")
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"✅ Exportado: {output_path}")
    return output_path


if __name__ == "__main__":
    extract_ga4()