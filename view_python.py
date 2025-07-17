import pandas as pd
from sqlalchemy import create_engine

# ======== CONFIGURAÇÃO DE CONEXÃO COM AWS RDS =========
# Substitua os valores abaixo pelas suas credenciais
USER = "admin"
PASSWORD = "Adminfraudes123"
HOST = "bancofraudes.cfwaeqkk247n.sa-east-1.rds.amazonaws.com"
PORT = 3306
DB_NAME = "bancoFraude"
TABLE_CLIENTES = "silver.clientes_raw"

# Criando engine de conexão (MySQL como exemplo)
engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

# Leitura da tabela 'clientes' direto do banco
clientes_df = pd.read_sql(f"SELECT * FROM {TABLE_CLIENTES}", engine)

# ======== LEITURA DO ARQUIVO LOCAL DE TRANSAÇÕES =========
transacoes_df = pd.read_csv("transacoes_raw.csv")

# ======== JUNÇÃO E FORMATAÇÃO DOS DADOS =========
df_view = pd.merge(transacoes_df, clientes_df, on='id_cliente', how='left')

# Renomear colunas conforme esperado
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

# Lista final de colunas desejadas
colunas_finais = [
    'data_transacao', 'valor', 'tipo_transacao', 'canal', 'dispositivo',
    'cidade_transacao', 'estado_residencia', 'pais_transacao',
    'data_nascimento', 'cidade_residencia', 'estado_residencia', 'pais_residencia',
    'tipo_conta', 'pessoa_fisica', 'score', 'data_cadastro', 'data_emissao_cartao',
    'flag', 'id_cliente'
]

# Ajustar apenas com colunas disponíveis
colunas_existentes = [col for col in colunas_finais if col in df_view.columns]
df_view_final = df_view[colunas_existentes]

# Agora df_view_final contém a "view" em memória
print("✅ Dados carregados na variável df_view_final.")