import os
import requests
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# Credenciais da API de Origem
ORIGEM_URL = "https://apidoublemax.pybots.com.br/api/results"
AUTH = ("ivan", "Manuela2021@")

@app.get("/api/atualizada")
def buscar_dados():
    try:
        response = requests.get(ORIGEM_URL, auth=AUTH)
        if response.status_code == 200:
            dados = response.json()
            # Processamento para a IA BRUZI
            processados = []
            for item in dados[:15]:
                cor = item.get("color")
                emoji = "🔴" if cor == "red" else "⚫" if cor == "black" else "⚪"
                txt_cor = "VERMELHO" if cor == "red" else "PRETO" if cor == "black" else "BRANCO"
                
                processados.append({
                    "id": item.get("id"),
                    "resultado": txt_cor,
                    "sinal": emoji,
                    "valor": item.get("value")
                })
            return {"sucesso": True, "dados": processados}
        return {"sucesso": False}
    except Exception as e:
        return {"erro": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
