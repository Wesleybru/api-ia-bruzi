from fastapi import FastAPI
import requests
import asyncio

app = FastAPI()
historico_bruzi = []

def rastrear():
    # Tentando o caminho direto do histórico da BetPontoBet
    url = "https://betpontobet.bet.br/api/casino/games/double-max/history"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://betpontobet.bet.br/"
    }
    try:
        res = requests.get(url, headers=headers, timeout=15).json()
        
        # O "Coringa": Procura a lista em qualquer lugar do arquivo
        itens = []
        if isinstance(res, list): itens = res
        elif 'data' in res: itens = res['data']
        elif 'results' in res: itens = res['results']
        elif 'items' in res: itens = res['items']
        
        novos = []
        for i in itens[:20]:
            # Pega o número e a cor, não importa o nome que o site deu (roll, result, number)
            num = i.get('roll') or i.get('number') or i.get('result') or 0
            c = i.get('color') or i.get('colour') or 0
            
            cor = "BRANCO" if c == 0 else "VERMELHO" if c == 1 else "PRETO"
            sinal = "⚪" if c == 0 else "🔴" if c == 1 else "⚫"
            
            novos.append({
                "id": i.get('id'),
                "valor": num,
                "cor": cor,
                "sinal": sinal
            })
        return novos
    except:
        return None

async def loop():
    global historico_bruzi
    while True:
        d = rastrear()
        if d and len(d) > 0:
            historico_bruzi = d
        await asyncio.sleep(5)

@app.on_event("startup")
async def startup():
    asyncio.create_task(loop())

@app.get("/api/atualizada")
def pegar():
    return {"sucesso": True, "fonte": "IA BRUZI - BetPontoBet", "dados": historico_bruzi}

@app.get("/")
def home():
    return {"status": "ONLINE", "registros": len(historico_bruzi)}
    
