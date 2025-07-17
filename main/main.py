# main.py
import os
os.system("python scripts/indicadores_economicos.py")
os.system("python scripts/acoes.py")
os.system("python scripts/noticias.py")
os.system("python scripts/agentes_economicos.py")
os.system("streamlit run streamlit/dashboard.py")