import mysql.connector

# Conexão com o banco
conn = mysql.connector.connect(
    host='localhost',
    user='seu_usuario',
    password='sua_senha',
    database='nome_do_banco'
)

# Script SQL do ETL
etl_sql = """
-- ETL SQL COMPLETO
REPLACE INTO paises_cleaned (id_pais, nome_pais)
SELECT DISTINCT fk_id_pais, nome_pais FROM clientes_raw;

REPLACE INTO estados_cleaned (id_estado, uf_estado)
SELECT DISTINCT fk_id_estado, uf_estado FROM clientes_raw;

REPLACE INTO cidades_cleaned (id_cidade, nome_cidade, fk_id_estado)
SELECT DISTINCT fk_id_cidade, nome_cidade, fk_id_estado FROM clientes_raw;

REPLACE INTO clientes_conta_cleaned (id_conta, tipo_conta)
SELECT DISTINCT id_conta, tipo_conta FROM clientes_raw;

REPLACE INTO transacoes_canais_cleaned (id_canal, nome_canal)
SELECT DISTINCT fk_id_canal, nome_canal FROM transacoes_raw;

REPLACE INTO transacoes_dispositivos_cleaned (id_dispositivo, nome_dispositivo)
SELECT DISTINCT fk_id_dispositivo, nome_dispositivo FROM transacoes_raw;

REPLACE INTO transacoes_tipo_transacao_cleaned (id_tipo_transacao, nome_tipo_transacao)
SELECT DISTINCT fk_id_tipo_transacao, nome_tipo_transacao FROM transacoes_raw;

REPLACE INTO clientes_cleaned (
    id_cliente, nome, data_nasc, fk_id_cidade, id_conta,
    pessoa_fisica, score, data_cadastro, data_emissao_cartao,
    fk_id_estado_clientes, fk_id_pais
)
SELECT
    id_cliente, nome, data_nasc, fk_id_cidade, id_conta,
    pessoa_fisica, score, data_cadastro, data_emissao_cartao,
    fk_id_estado, fk_id_pais
FROM clientes_raw;

REPLACE INTO transacoes_cleaned (
    id_transacao, id_cliente, data_transacao, valor,
    fk_id_tipo_transacao, fk_id_canal, fk_id_cidade_transacao,
    fk_id_pais_transacao, fk_id_dispositivo, flag, fk_id_estado
)
SELECT
    id_transacao, id_cliente, data_transacao, valor,
    fk_id_tipo_transacao, fk_id_canal, fk_id_cidade_transacao,
    fk_id_pais_transacao, fk_id_dispositivo, flag, fk_id_estado
FROM transacoes_raw;
"""

# Executar o script
try:
    cursor = conn.cursor()
    for statement in etl_sql.strip().split(';'):
        stmt = statement.strip()
        if stmt:
            cursor.execute(stmt)
    conn.commit()
    print("ETL executado com sucesso!")
except mysql.connector.Error as err:
    print("Erro ao executar ETL:", err)
finally:
    cursor.close()
    conn.close()
