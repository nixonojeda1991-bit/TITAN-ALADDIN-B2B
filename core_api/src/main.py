from fastapi import FastAPI
from src.strategy_master import generar_reporte

app = FastAPI()
@app.get("/aladdin/{simbolo}")
def aladdin(simbolo: str):
    return generar_reporte(simbolo)
