import yfinance as yf
import pandas as pd
from src.db_manager import get_engine
from sqlalchemy import text

def recolectar_datos_reales(simbolo):
    print(f"--> Bajando {simbolo}...")
    df = yf.download(simbolo, period="7d", interval="1h", progress=False, auto_adjust=True)
    if df.empty: return

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()
    df.columns = [str(c).lower().strip() for c in df.columns]
    rename_map = {'datetime': 'date', 'timestamp': 'date', 'index': 'date'}
    df = df.rename(columns=rename_map)

    if 'date' in df.columns and 'close' in df.columns:
        df = df[['date', 'close']]
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS market_prices"))
            conn.commit()
        df.to_sql('market_prices', engine, if_exists='replace', index=False)
