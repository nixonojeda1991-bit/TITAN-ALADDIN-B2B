import streamlit as st
import pandas as pd
import requests
import ccxt
import plotly.graph_objects as go
import time

# --- CONFIGURACIÓN ---
API_URL = "http://titan-core:8000"  # Comunicación interna Docker
st.set_page_config(page_title="TITÁN TERMINAL", layout="wide", page_icon="🦁")

# Estilos Institucionales
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    div.stButton > button { background-color: #00ff00; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦁 TITÁN TERMINAL | B2B LAYER")

# --- BARRA LATERAL (CONTROLES) ---
with st.sidebar:
    st.header("📡 Watchtower")
    symbol_input = st.text_input("Activo (Ej: BTC-USD)", value="BTC-USD")
    exchange_id = st.selectbox("Exchange", ["binance", "kraken", "coinbase"])
    
    st.markdown("---")
    st.info(f"Conectado a Núcleo: {API_URL}")

# --- PANTALLA PRINCIPAL ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Grafico de Mercado: {symbol_input}")
    # Usamos CCXT para el gráfico visual (Datos rápidos)
    try:
        exchange_class = getattr(ccxt, exchange_id)()
        # Mapeo simple de símbolos
        ticker = symbol_input.replace("-", "/") 
        if exchange_id == 'binance' and 'USD' in ticker and 'USDT' not in ticker:
             ticker = ticker.replace('USD', 'USDT')
             
        ohlcv = exchange_class.fetch_ohlcv(ticker, timeframe='1h', limit=50)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                        open=df['open'], high=df['high'],
                        low=df['low'], close=df['close'])])
        fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.warning(f"Esperando datos del Exchange... ({str(e)})")

with col2:
    st.subheader("🧠 INTELIGENCIA TITÁN")
    st.write("Solicitando análisis al Núcleo Soberano...")
    
    if st.button("EJECUTAR ANÁLISIS"):
        with st.spinner("Procesando en Kernel Gemini 2.5..."):
            try:
                # AQUÍ OCURRE LA MAGIA B2B: HTTP REQUEST
                response = requests.get(f"{API_URL}/aladdin/{symbol_input}")
                
                if response.status_code == 200:
                    st.success("Dictamen Recibido")
                    # Mostramos la respuesta tal cual la envía el núcleo
                    st.code(response.text, language="yaml")
                else:
                    st.error(f"Error del Núcleo: {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error de Conexión: El Núcleo parece estar apagado. ({e})")

# Footer
st.markdown("---")
st.caption("TITÁN SYSTEMS INC. | Licensed to Director Nixon | Architecture: Microservices v2.0")