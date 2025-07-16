from joblib import load
from sklearn.ensemble import RandomForestClassifier
from functions import tratar_dados
import pandas as pd

def inserir_flag(df_sem_tratamento):
    modelo_indicativo = load(filename="machine_learning/modelo_indicativo.joblib")

    df_tratado = tratar_dados(df_sem_tratamento)

    predicao = modelo_indicativo.predict(df_tratado)

    copia_df = df_sem_tratamento.copy()
    copia_df["flag"] = predicao
    
    return copia_df
