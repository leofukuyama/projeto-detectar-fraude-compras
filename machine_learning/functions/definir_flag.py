from joblib import load
from sklearn.ensemble import RandomForestClassifier
from functions import tratar_dados


def inserir_flag(df_sem_tratamento):
    modelo_indicativo = load(filename="machine_learning/modelo_indicativo.joblib")

    df = tratar_dados(df_sem_tratamento)

    