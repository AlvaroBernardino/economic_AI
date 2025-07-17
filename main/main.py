# main.py

import os

# Executa scripts de coleta e análise de dados
os.system("python scripts/indicadores_economicos.py")
os.system("python scripts/acoes.py")
os.system("python scripts/noticias.py")
os.system("python scripts/agentes_economicos.py")

# Obtém a porta que o Azure define como variável de ambiente
port = os.getenv("PORT", "8000")

# Executa o Streamlit na porta correta, ouvindo em todas as interfaces
os.system(f"streamlit run streamlit/dashboard.py --server.port={port} --server.address=0.0.0.0")
