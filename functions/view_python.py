import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


def transformar_colunas_df_raw_para_view(df_sem_tratamento):
    # ======== CONFIGURAÇÃO DE CONEXÃO COM AWS RDS =========
    load_dotenv()
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASS")
    HOST = os.getenv("DB_HOST")
    PORT = 3306
    DB_NAME = os.getenv("DB_NAME")
    TABLE_CLIENTES = "bronze.clientes_raw"

    # Criando engine de conexão (MySQL como exemplo)
    engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

    # ======= LEITURA DAS TABELAS DO BANCO ========
    clientes_df = pd.read_sql("SELECT * FROM bronze.clientes_raw", engine)
    cidades_df = pd.read_sql("SELECT * FROM silver.cidades_cleaned", engine)
    estados_df = pd.read_sql("SELECT * FROM silver.estados_cleaned", engine)

    # ======== LEITURA DO ARQUIVO LOCAL DE TRANSAÇÕES =========
    transacoes_df = df_sem_tratamento.copy()

    # ======= COMPLETAR A INFORMAÇÃO DE ESTADO NA TRANSAÇÃO ========
    # Primeiro normalizamos o nome da cidade para fazer o join
    transacoes_df['cidade_transacao'] = transacoes_df['cidade_transacao'].str.strip().str.lower()
    cidades_df['nome_cidade'] = cidades_df['nome_cidade'].str.strip().str.lower()

    # Fazendo o merge para pegar o ID do estado
    transacoes_df = transacoes_df.merge(cidades_df, left_on='cidade_transacao', right_on='nome_cidade', how='left')

    # Agora adicionando a sigla ou nome do estado
    transacoes_df = transacoes_df.merge(estados_df, left_on='fk_id_estado', right_on='id_estado', how='left')
    transacoes_df.rename(columns={'uf_estado': 'estado_transacao'}, inplace=True)

    # ======= JOIN COM CLIENTES ========
    df_view = pd.merge(transacoes_df, clientes_df, on='id_cliente', how='left')

    # ======= RENOMEANDO E FORMATANDO ========
    df_view.rename(columns={
        'score_credito': 'score',
        'data_nascimento': 'data_nascimento',
        'cidade_residencia': 'cidade_residencia',
        'estado_residencia': 'estado_residencia',
        'pais_residencia': 'pais_residencia',
        'tipo_conta': 'tipo_conta',
        'data_cadastro': 'data_cadastro',
        'data_emissao_cartao': 'data_emissao_cartao',
        'flag_fraude_confirmada': 'flag',
    }, inplace=True)

    # ======= COLUNAS FINAIS =========
    colunas_finais = [
        'data_transacao', 'valor', 'tipo_transacao', 'canal', 'dispositivo',
        'cidade_transacao', 'estado_transacao', 'pais_transacao',
        'data_nascimento', 'cidade_residencia', 'estado_residencia', 'pais_residencia',
        'tipo_conta', 'pessoa_fisica', 'score', 'data_cadastro', 'data_emissao_cartao',
        'flag', 'id_cliente'
    ]

    colunas_existentes = [col for col in colunas_finais if col in df_view.columns]
    df_view_final = df_view[colunas_existentes]

    df_view_final = df_view_final.sort_values(by=['data_transacao', "id_cliente"])
    
    return df_view_final
