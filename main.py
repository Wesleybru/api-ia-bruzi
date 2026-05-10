from fastapi import FastAPI
import requests
import asyncio

app = FastAPI()

# Memória da IA BRUZI
historico_bruzi = []

def rastrear_double_ponto_bet():
    # Este é o endereço onde os dados do jogo "Double Max" ficam escondidos
    url = "https://betpontobet.bet.br/api/casino/games/double-max/history" 
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # Tentamos ler os últimos giros
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            dados_site = response.json()
            
            # Aqui pegamos a lista de resultados (geralmente vem em 'data' ou 'results')
            lista_giros = dados_site.get('data', []) or dados_site.get('results', [])
            
            novos_giros = []
            for item in lista_giros[:20]: # Pegamos os últimos 20
                valor = item.get('roll') or item.get('number')
                cor_num = item.get('color')
                
                # Traduzindo as cores do sistema deles
                cor = "BRANCO" if cor_num == 0 else "VERMELHO" if cor_num == 1 else "PRETO"
                sinal = "⚪" if cor == "BRANCO" else "🔴" if cor == "VERMELHO" else "⚫"
                
                novos_giros.append({
                    "id": item.get('id'),
                    "valor": valor,
                    "cor": cor,
                    "sinal": sinal
                })
            return novos_giros
    except Exception as e:
        print(f"Erro ao rastrear: {e}")
        return None
    return None

async def loop_monitoramento():
    global historico_bruzi
    while True:
        dados = rastrear_double_ponto_bet()
        if dados:
            historico_bruzi = dados
        await asyncio.sleep(5) # Verifica a cada 5 segundos para ser rápido

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(loop_monitoramento())

@app.get("/api/atualizada")
def pegar_dados():
    return {
        "sucesso": True,
        "plataforma": "BetPontoBet",
        "dono": "IA BRUZI",
        "dados": historico_bruzi
    }

@app.get("/")
def home():
    return {"status": "IA BRUZI ATIVA", "monitorando": "BetPontoBet - Double Max"}
    
