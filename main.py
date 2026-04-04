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

@st.cache_data
def carregar_tickers_acoes():
  base_tickers = pd.read_csv("IBOV.csv", sep=";")
  tickers = list(base_tickers["Código"])
  tickers = [item + ".SA" for item in tickers] # Adicionar o sufixo ".SA" para os tickers do Yahoo Finance
  return tickers

acoes = carregar_tickers_acoes()
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

# Calculo de performance
texto_performance_ativos = ""

if len(lista_acoes) == 0:
  lista_acoes = dados.columns
elif len(lista_acoes) == 1:
  dados = dados.rename(columns={"Close": acao_unica})

carteira = [1000 for acao in lista_acoes]
total_inical_carteira = sum(carteira)

for i, acao in enumerate(lista_acoes):
  performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1 # Como calcular o valor de um ativo (VALOR_FINAL / VALOR_INCIAL -1)
  performance_ativo = float(performance_ativo)
  # print(performance_ativo)
  carteira[i] = carteira[i] * (1 + performance_ativo)

  if performance_ativo > 0:
    # :cor[texto]
    texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :green[{performance_ativo:.1%}]"
  elif performance_ativo < 0:
    texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :red[{performance_ativo:.1%}]"
  else:
    texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: {performance_ativo:.1%}"

total_final_carteira = sum(carteira)
performance_carteira = total_final_carteira / total_inical_carteira - 1

if performance_carteira > 0:
    texto_performance_carteira = f"Performance da carteira com todos os ativos: :green[{performance_carteira:.1%}]"
elif performance_carteira < 0:
    texto_performance_carteira = f"Performance da carteira com todos os ativos: :red[{performance_carteira:.1%}]"
else:
    texto_performance_carteira = f"Performance da carteira com todos os ativos: {performance_carteira:.1%}"

st.write(f"""
### Performance dos Ativos
A tabela abaixo mostra a performance dos ativos selecionados no período escolhido.
{texto_performance_ativos}

{texto_performance_carteira}
""") # Variável dentro de um texto add um "f" para formatar o texto e colocar a variável dentro de chaves {}