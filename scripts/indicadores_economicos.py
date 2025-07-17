# indicadores_economicos.py
import requests
import pandas as pd
import os
from datetime import datetime

# Mapeamento dos indicadores e seus códigos SGS
indicadores = {
    "IPCA": 433,
    "SELIC": 432,
    "PIB": 4380,
    "DÓLAR": 1,
    "COMMODITIES": 22795,
    "IGP-M": 189 
}

def coletar_indicadores_bacen(indicadores: dict, n_ultimos: int = 20) -> pd.DataFrame:
    todos_dados = []

    for nome, codigo in indicadores.items():
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/{n_ultimos}?formato=json"
        response = requests.get(url)

        if response.status_code == 200:
            dados = response.json()
            df = pd.DataFrame(dados)
            df["valor"] = df["valor"].str.replace(",", ".").astype(float)
            df["indicador"] = nome
            df["data_coleta"] = datetime.now().date()
            todos_dados.append(df)
        else:
            print(f"❌ Erro ao buscar {nome} (código {codigo}). Status: {response.status_code}")

    df_final = pd.concat(todos_dados, ignore_index=True)
    df_final.rename(columns={"data": "data", "valor": "valor"}, inplace=True)
    return df_final

# Define o caminho absoluto com base na localização do script
base_dir = os.path.dirname(__file__)
output_path = os.path.join(base_dir, "..", "data", "indicadores_economicos.csv")

# Garante que a pasta de destino exista
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Coletar e salvar
df_indicadores = coletar_indicadores_bacen(indicadores)
df_indicadores.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"✅ Arquivo '{output_path}' salvo com sucesso.")
