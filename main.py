import numpy as np
import pandas as pd
import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
import joblib
from mysql.connector import Error
from passlib.hash import pbkdf2_sha256

# Função para criar o hash da senha (usar quando cadastrar usuário)
def create_hash(password):
    return pbkdf2_sha256.hash(password)

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
    st.title("Sistema de Login Seguro")
    
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

# Página principal (após login)
def main_page():
    st.title(f"Bem-vindo, {st.session_state.username}!")
    st.write("Você está na área segura do sistema")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# Configuração inicial
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.rerun()
    
# Menu principal
if not st.session_state.logged_in:
    login_page()
else:
    main_page()