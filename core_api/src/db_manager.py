from sqlalchemy import create_engine
import time

def get_engine():
    for _ in range(10):
        try:
            return create_engine("postgresql://postgres:password@timescaledb:5432/postgres")
        except:
            time.sleep(3)
    raise RuntimeError("ERROR CRÍTICO: BD no responde")
