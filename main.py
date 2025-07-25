import numpy as np
import pandas as pd
import streamlit as st
import mysql.connector
import os
from joblib import load
from dotenv import load_dotenv
from mysql.connector import Error
from passlib.hash import pbkdf2_sha256
from functions.carregar_view import carregar_dados
from functions.tratar_dados import tratar_colunas_df
from functions.avaliar_modelo import avaliar_modelo

st.set_page_config(page_title="Detecção de Fraudes",
                   page_icon="💡",
                   layout="wide",
                   initial_sidebar_state="collapsed")


# Função para verificar credenciais com hash
def verify_user(username, password):
    try:
        load_dotenv()

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if result and pbkdf2_sha256.verify(password, result['password']):
            return True
        return False
        
    except Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return False

# Página de login
def login_page():
    st.title("💳 Login - Sistema de Detecção de Fraudes")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    
    if st.button("Login"):
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")

# Função para retornar os transações com as duas flags
def retornar_df_duas_flags():
    try:
        load_dotenv()
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )
        
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bronze.transacoes_com_indicativo_raw;")

        column_names = [i[0] for i in cursor.description]

        data = cursor.fetchall()

        data = pd.DataFrame(data, columns=column_names)

        cursor.close()
        conn.close()

        return data

    except Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return False
    
# Formatar valores
def formatar_valores(valor):
    valor_formatado = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return valor_formatado


# Página principal (após login)
def main_page():
    with st.sidebar:        
        st.markdown(f"👤 Usuário: **{st.session_state.username}**")
        st.markdown("---")
        
        if st.button("🚪 Sair"):
            st.session_state.logged_in = False
            st.rerun()

    st.title("🚨 Detecção de Fraudes com Random Forest")
    st.markdown("Este painel mostra como o modelo foi treinado e aplicado, passo a passo.")

    st.subheader("🔍 Etapa 1: Carregamento dos Dados")
    df = carregar_dados()
    st.dataframe(df.head())

    # Etapa de tratamento
    st.subheader("🧹 Etapa 2: Tratamento e Preparação de Dados")
    st.write("Ajustar tipos dos dados, transformar valores categóricos em dummies e criar um novo indicativo de flag.")
    
    df_tratado = tratar_colunas_df(df)
    st.write("Colunas após tratamento:", df_tratado.columns.tolist())

    st.write("Separar entre features e target:")
    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(df_tratado.drop("indicativo_fraude", axis=1))
    with col2:
        st.dataframe(df_tratado["indicativo_fraude"])

    # Treinamento
    st.subheader("🏋️ Etapa 3: Treinamento do Modelo")
    st.write("Instanciar RandomForestClassifier e treinar  modelo:")
    modelo_indicativo = load("machine_learning\modelo_indicativo.joblib")
    if modelo_indicativo:
        st.success("Modelo treinado com sucesso!")

    # Avaliação
    st.subheader("📊 Etapa 4: Avaliação do Modelo")
    relatorio = avaliar_modelo(modelo_indicativo, df_tratado)
    
    st.markdown(f"```\n{relatorio}\n```")

    df_duas_flags = retornar_df_duas_flags()

    total_original = df_duas_flags[df_duas_flags["flag_fraude_confirmada"] == 1]["valor"].sum()
    total_modelo = df_duas_flags[df_duas_flags["flag_modelo"] == 1]["valor"].sum()
    diferenca_valores_totais = total_modelo - total_original

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Flags Originais:", f"R$ {formatar_valores(total_original)}")
    with col2:
        st.metric("Flags Modelo:", f"R$ {formatar_valores(total_modelo)}")
    with col3:
        st.metric("Diferença:", f"R$ {formatar_valores(diferenca_valores_totais)}")


# Configuração inicial
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.rerun()
    
# Menu principal
if not st.session_state.logged_in:
    login_page()
else:
    main_page()