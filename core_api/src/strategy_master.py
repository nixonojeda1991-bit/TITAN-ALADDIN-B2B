import pandas as pd
import ta
from src.db_manager import get_engine
from src.collector import recolectar_datos_reales
from src.oracle_ai import obtener_dictamen_gemini

def generar_reporte(simbolo):
    recolectar_datos_reales(simbolo)
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM market_prices ORDER BY date ASC", engine)
    
    if df.empty: return "CARGANDO..."

    precio = df['close'].iloc[-1]
    rsi = ta.momentum.RSIIndicator(df['close'], window=14).rsi().iloc[-1]
    estado = "SOBRECOMPRA" if rsi > 70 else "SOBREVENTA" if rsi < 30 else "NEUTRAL"

    ai_msg = obtener_dictamen_gemini(simbolo, precio, rsi, estado)
    return f"TITÁN V-FINAL\nACTIVO: {simbolo}\nPRECIO: {precio}\n{ai_msg}"
