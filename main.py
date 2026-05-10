from fastapi import FastAPI
import asyncio
import websockets
import json

app = FastAPI()

# Nossa "memória" para guardar os giros sem depender de API externa
historico_bruzi = []

async def conectar_sinal_real():
    uri = "wss://api-v2.blaze.com/replication/?EIO=3&transport=websocket" # Exemplo da Blaze/DoubleMax
    
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("✅ IA BRUZI Conectada ao sinal direto!")
                while True:
                    msg = await websocket.recv()
                    
                    # Filtra apenas quando sai um resultado novo (giro completo)
                    if 'double.tick' in msg:
                        dados = json.loads(msg[str(msg).find('{'):])
                        cor = "VERMELHO" if dados['color'] == 1 else "PRETO" if dados['color'] == 2 else "BRANCO"
                        novo_giro = {
                            "id": dados['id'],
                            "valor": dados['roll'],
                            "cor": cor,
                            "sinal": "🔴" if cor == "VERMELHO" else "⚫" if cor == "PRETO" else "⚪"
                        }
                        
                        # Adiciona no topo do nosso histórico
                        if not historico_bruzi or novo_giro['id'] != historico_bruzi[0]['id']:
                            historico_bruzi.insert(0, novo_giro)
                            if len(historico_bruzi) > 20: historico_bruzi.pop()
                            print(f"🎰 Novo Giro Detectado: {cor} ({dados['roll']})")
        except Exception as e:
            print(f"🚨 Conexão perdida, tentando reconectar em 5s... {e}")
            await asyncio.sleep(5)

# Inicia o rastreador assim que a API liga
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(conectar_sinal_real())

@app.get("/api/atualizada")
def pegar_dados():
    return {
        "sucesso": True,
        "fonte": "Propria (IA BRUZI)",
        "dados": historico_bruzi
    }

@app.get("/")
def home():
    return {"status": "IA BRUZI ONLINE 24H", "historico_tamanho": len(historico_bruzi)}
    
