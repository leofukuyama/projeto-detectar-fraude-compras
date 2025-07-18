import pandas as pd
from datetime import datetime


def tratar_colunas_df(df):
    # Converter todas as colunas data em datetime
    df['data_transacao'] = pd.to_datetime(df['data_transacao'])
    df['data_nascimento'] = pd.to_datetime(df['data_nascimento'])
    df['data_cadastro'] = pd.to_datetime(df['data_cadastro'])
    df['data_emissao_cartao'] = pd.to_datetime(df['data_emissao_cartao'])

    # Converter o campo de valor para float
    df['valor'] = df['valor'].astype(float)

    # Converter o campo de pessoa_fisica para booleano
    df['pessoa_fisica'] = df['pessoa_fisica'].astype(bool)

    # Converter o campo de flag para booleano
    df['flag'] = df['flag'].astype(bool)

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

    # Criar DataFrame com flags de possíveis fraudes
    df_flag = pd.DataFrame()
    df_flag["possivel_fraude_valor_alto"] = df["valor"] > df["valor"].quantile(0.85)
    df_flag["possivel_fraude_valor_baixo"] = df["valor"] < df["valor"].quantile(0.15)
    df_flag["possivel_fraude_pos_online"] = (df["dispositivo"] == "POS") & (df["tipo_transacao"] == "Online")
    df_flag["possivel_fraude_dispositivo_desconhecido"] = df["dispositivo"] == "Desconhecido"
    df_flag["possivel_fraude_local_diferente"] = (df["eh_mesmo_estado_transacao"] == 0) | (df["eh_mesmo_pais_transacao"] == 0)
    df_flag["transacao_madrugada"] = df["hora_transacao"].between(0, 5) & (df["valor"] > df["valor"].quantile(0.85))
    df_flag["possivel_fraude_ultima_rapida"] = df["intervalo_ultima_transacao"] < 60
    df_flag["possivel_fraude_proxima_rapida"] = df["intervalo_proxima_transacao"] < 60
    df_flag["possivel_fraude_score_baixo"] = df["score"] < df["score"].quantile(0.15)
    df_flag["possivel_fraude_score_alto"] = df["score"] > df["score"].quantile(0.85)
    df_flag["possivel_fraude_idade_alta"] = df["idade_cliente"] > df["idade_cliente"].quantile(0.85)
    df_flag["possivel_fraude_quantidade_transacoes"] = df["quantidade_transacoes"] > df["quantidade_transacoes"].quantile(0.85)
    df_flag["cliente_novo_valor_alto"] = (df["dias_desde_cadastro_cliente"] < 30) & (df["valor"] > df["valor"].quantile(0.85))
    df_flag["cliente_novo_valor_baixo"] = (df["dias_desde_cadastro_cliente"] < 30) & (df["valor"] < df["valor"].quantile(0.15))
    df_flag["cliente_antigo_valor_alto"] = (df["dias_desde_cadastro_cliente"] >= 30) & (df["valor"] > df["valor"].quantile(0.85))
    df_flag["cliente_antigo_valor_baixo"] = (df["dias_desde_cadastro_cliente"] >= 30) & (df["valor"] < df["valor"].quantile(0.15))
    df_flag["canal_raro_valor_alto"] = (df["canal"] == "Cartão de Crédito") & (df["valor"] > df["valor"].quantile(0.85))
    df_flag["transacoes_rapidas_duplas"] = (df["intervalo_ultima_transacao"] < 60) | (df["intervalo_proxima_transacao"] < 60)

    # Soma de sinais de fraude
    df_flag["score_risco_fraude"] = df_flag.sum(axis=1).astype(int)

    # Flag final: somente se houver 3 ou mais sinais
    df["indicativo_flag"] = (df_flag["score_risco_fraude"] >= 3).astype(int)

    # Dropar a coluna flag original
    df.drop("flag", axis=1, inplace=True)

    # Dropar a coluna id_cliente para treinar o modelo
    df.drop("id_cliente", axis=1, inplace=True)

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