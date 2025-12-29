import vertexai
from vertexai.generative_models import GenerativeModel

def obtener_dictamen_gemini(simbolo, precio, rsi, estado):
    try:
        vertexai.init(project="tcis-titan-12", location="us-central1")
        model = GenerativeModel("gemini-2.5-flash")
        prompt = f"ACTIVO: {simbolo} | PRECIO: {precio} | RSI: {rsi} ({estado}). DAME ORDEN: COMPRAR/VENDER."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ERROR IA: {e}"
