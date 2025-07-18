import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def avaliar_modelo(modelo, df):
    X = df.drop("indicativo_flag", axis=1)
    y = df["indicativo_flag"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    y_pred = modelo.predict(X_test)

    return classification_report(y_test, y_pred)