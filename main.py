# Importar bibliotecas

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta

# Criar funções de carregamento de dados
  # Cotações do Itáu ITUB4 - 2010-2026
@st.cache_data # Cache para otimizar o carregamento dos dados
def carregar_dados(empresas):
  texto_tickers = " ".join(empresas)
  dados_acao = yf.Tickers(texto_tickers)
  cotacoes_acao = dados_acao.history(start="2010-01-01", end="2026-01-01")
  # print(cotacoes_acao)
  cotacoes_acao = cotacoes_acao["Close"]
  return cotacoes_acao

acoes = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "GGBR4.SA"]
dados = carregar_dados(acoes) # Carregar os dados das ações selecionadas

# Criar a interface do Streamlit
st.write("""
# App Preço de Ações
O gráfico abaixo mostra a evolução do preço das ações ao longo dos anos.
""") # Markdown

# Preparar as visualizações
st.sidebar.header("Filtros")
# Filtros de ações
lista_acoes = st.sidebar.multiselect("Escolha as ações para visualizar", dados.columns)
# print(lista_acoes)
if lista_acoes:
  dados = dados[lista_acoes] # Filtrar os dados para mostrar apenas as ações selecionadas
  if len(lista_acoes) == 1:
    dados = dados[lista_acoes] # Filtrar os dados para mostrar apenas as ações selecionadas
    acao_unica = lista_acoes[0]
    dados = dados.rename(columns={acao_unica: "Close"})
# Filtro de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_datas = st.sidebar.slider("Selecione o período", min_value = data_inicial , max_value = data_final, value = (data_inicial, data_final), step = timedelta(days=1))
# print(intervalo_datas[1])
dados = dados.loc[intervalo_datas[0]:intervalo_datas[1]] # Filtrar os dados para mostrar apenas o período selecionado
# Criação do gráfico
st.line_chart(dados) # Gráfico de linha para mostrar a evolução do preço das ações

st.write(""" ## Fim do App""")