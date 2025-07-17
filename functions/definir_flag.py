from joblib import load
from sklearn.ensemble import RandomForestClassifier
from functions.tratar_dados import tratar_colunas_df
import pandas as pd

def inserir_flag(df_formatado, df_sem_tratamento):
    modelo_indicativo = load(filename="machine_learning/modelo_indicativo.joblib")

    df_tratado = tratar_colunas_df(df_formatado)

    predicao = modelo_indicativo.predict(df_tratado)

    copia_df = df_sem_tratamento.copy()
    copia_df.drop("flag_fraude_confirmada", axis=1, inplace=True)

    copia_df = copia_df.sort_values(by=['data_transacao', "id_cliente"])
    copia_df["flag_fraude_confirmada"] = predicao
    copia_df = copia_df.sort_values("id_transacao")
    
    return copia_df
