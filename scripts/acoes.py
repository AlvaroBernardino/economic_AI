# acoes.py
import requests
import pandas as pd
from time import sleep
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

# Top 10 ações da B3 por volume - definidas manualmente
top_10_acoes = ["PETR4", "VALE3", "ITUB4", "BBDC4", "ABEV3", "BBAS3", "B3SA3", "WEGE3", "RENT3", "MGLU3"]

def buscar_dados_acao_alpha_vantage(ticker_b3, api_key, num_registros=10):
    ticker = ticker_b3 + ".SA"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}&outputsize=compact"

    response = requests.get(url)
    if response.status_code != 200:
        if response.status_code == 503:
            print(f"[{ticker_b3}] Servidor Alpha Vantage indisponível (503). Tentando novamente em alguns segundos...")
            sleep(30)
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"[{ticker_b3}] Erro {response.status_code} após nova tentativa.")
        else:
            raise Exception(f"[{ticker_b3}] Erro {response.status_code}")

    data = response.json()
    if "Note" in data or "Information" in data:
        print(f"[{ticker_b3}] Nota da API: {data.get('Note', data.get('Information', 'Limite de API provavelmente atingido.'))}")
        return None
    if "Time Series (Daily)" not in data:
        print(f"[{ticker_b3}] Sem dados 'Time Series (Daily)' na resposta. Resposta completa: {data}")
        return None

    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
    df.columns = ["abertura", "alta", "baixa", "fechamento", "volume"]
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=True)
    df["ticker"] = ticker_b3
    df = df.tail(num_registros)

    return df

# Coleta os dados
df_total = pd.DataFrame()

for ativo in top_10_acoes:
    try:
        print(f"🔄 Coletando {ativo}...")
        df = buscar_dados_acao_alpha_vantage(ativo, api_key)

        if df is not None and not df.empty:
            df_total = pd.concat([df_total, df])
            print(f"✅ {ativo} adicionado com {len(df)} registros.")
        elif df is not None and df.empty:
            print(f"⚠️ {ativo} retornou um DataFrame vazio após o processamento.")
        
        sleep(15)  # Respeita o limite da API gratuita
    except Exception as e:
        print(f"❌ Erro com {ativo}: {e}")

# Define caminho absoluto com base na localização do script
base_dir = os.path.dirname(__file__)
output_path = os.path.join(base_dir, "..", "data", "top_10_acoes.csv")

# Garante que a pasta de destino existe
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Salva o arquivo final
if not df_total.empty:
    df_total.to_csv(output_path, index=True, encoding="utf-8-sig")
    print(f"📁 Arquivo final salvo com {len(df_total)} linhas.")
else:
    print("ℹ️ Nenhum dado foi coletado para salvar no arquivo CSV.")