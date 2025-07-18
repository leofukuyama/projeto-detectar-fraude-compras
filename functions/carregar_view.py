import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carregar variáveis de ambiente
load_dotenv()

def conectar_ao_banco():
    # Montar a string de conexão para MySQL
    usuario = os.getenv("DB_USER")
    senha = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    banco = os.getenv("DB_NAME")

    # Criar engine SQLAlchemy
    engine = create_engine(f"mysql+mysqlconnector://{usuario}:{senha}@{host}/{banco}")
    return engine

def carregar_dados():
    engine = conectar_ao_banco()
    query = "SELECT * FROM gold.dados_machine_learning;"
    df = pd.read_sql(query, engine)
    return df
