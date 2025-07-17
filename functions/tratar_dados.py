import pandas as pd
from datetime import datetime


def tratar_colunas_df(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo)

    # Ordenar por data_transacao
    df = df.sort_values(by=['data_transacao', "id_cliente"])

    # Converter o campo de valor para float
    df['valor'] = df['valor'].astype(float)

    # Converter o campo de pessoa_fisica para booleano
    df['pessoa_fisica'] = df['pessoa_fisica'].astype(bool)

    # Criar campo hora, minuto e segundo com base na data_transacao
    df_hora = df['data_transacao'].dt.hour
    df_minuto = df['data_transacao'].dt.minute
    df_segundo = df['data_transacao'].dt.second
    df.insert(1, "hora_transacao", df_hora)
    df.insert(2, "minuto_transacao", df_minuto)
    df.insert(3, "segundo_transacao", df_segundo)

    # Criar campo mes_transacao com base na data_transacao
    df_mes = df['data_transacao'].dt.month
    df.insert(4, "mes_transacao", df_mes)

    # Criar campo dia_transacao com base na data_transacao
    df_dia = df['data_transacao'].dt.day
    df.insert(5, "dia_transacao", df_dia)

    # Criar campo dia_da_semana com base na data_transacao
    df_dia_semana = df['data_transacao'].dt.weekday
    df.insert(6, "dia_da_semana_transacao", df_dia_semana)

    # Criar campo final_de_semana com base na data_transacao
    df_final_de_semana = df['data_transacao'].dt.weekday >= 5
    df.insert(7, "eh_final_de_semana_transacao", df_final_de_semana)

    # Criar campo idade com base em data_nascimento
    df_idade = (datetime.now() - df['data_nascimento']).dt.days // 365
    df.insert(17, "idade_cliente", df_idade)

    # Criar campo dias_desde_cadastro com base em data_cadastro
    df_cadastro = (datetime.now() - df['data_cadastro']).dt.days
    df.insert(24, "dias_desde_cadastro_cliente", df_cadastro)

    # Criar campo dias_com_cartao com base na data_emissao_cartao
    df_cartao = (datetime.now() - df['data_emissao_cartao']).dt.days
    df.insert(26, "dias_com_cartao_cliente", df_cartao)

    # Criar campo quantidade de transações por cliente
    df_quantidade_transacoes = df.groupby('id_cliente').cumcount() + 1
    df.insert(27, "quantidade_transacoes", df_quantidade_transacoes)

    # Criar campos para verificar se é mesma cidade, estado e país
    df["eh_mesma_cidade_transacao"] = df["cidade_residencia"].eq(df["cidade_transacao"]).astype('bool')
    df["eh_mesmo_estado_transacao"] = df["estado_residencia"].eq(df["UF_transacao"]).astype('bool')
    df["eh_mesmo_pais_transacao"] = df["pais_residencia"].eq(df["pais_transacao"]).astype('bool')

    # Calculando o intervalo de tempo desde a última transação e até a próxima transação e armazenando em colunas para análise
    df['intervalo_ultima_transacao'] = df.groupby('id_cliente')['data_transacao'].diff()
    df['intervalo_proxima_transacao'] = df.groupby('id_cliente')['data_transacao'].diff(-1).abs()

    # Convertendo o intervalo de tempo para segundos para permitir maior precisão na análise de transações suspeitas
    df['intervalo_ultima_transacao'] = df['intervalo_ultima_transacao'].dt.total_seconds()
    df['intervalo_proxima_transacao'] = df['intervalo_proxima_transacao'].dt.total_seconds()

    # Tratando os valores nulos do intervalo de tempo
    df["intervalo_ultima_transacao"] = df["intervalo_ultima_transacao"].fillna(0)
    df["intervalo_proxima_transacao"] = df["intervalo_proxima_transacao"].fillna(0)

    # Dropar a coluna id_cliente para treinar o modelo
    df.drop("id_cliente", axis=1, inplace=True)

    # Dropar a coluna flag para treinar o modelo
    df.drop("flag", axis=1, inplace=True)

    # Dropar as colunas data_transacao, data_nascimento, data_cadastro, data_emissao_cartao para treinar o modelo
    df.drop(["data_transacao", "data_nascimento", "data_cadastro", "data_emissao_cartao"], axis=1, inplace=True)

    # Dropar colunas de localização
    colunas_localizacao = ["cidade_transacao", "UF_transacao", "pais_transacao",
                        "cidade_residencia", "estado_residencia", "pais_residencia"]

    df.drop(colunas_localizacao, axis=1, inplace=True)

    # Tratamento Categóricos
    categorical_features = ["tipo_transacao", "canal", "dispositivo", "tipo_conta"]

    df = pd.get_dummies(df, columns=categorical_features)

    return df