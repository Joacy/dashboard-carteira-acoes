import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys

st.set_page_config(
  page_title="Carteira de Ações",
  page_icon="📈",
  layout="wide"
)

df_posicao = pd.read_csv("posicao.csv")

carteira = {}
for line in df_posicao.index:
  if df_posicao.iloc[line]['Código de Negociação'] not in carteira:
    carteira[df_posicao.iloc[line]['Código de Negociação']] = {'preco': float(df_posicao.iloc[line]['Preço de Fechamento']), 'quantidade': int(df_posicao.iloc[line]['Quantidade'])}
  else:
    carteira[df_posicao.iloc[line]['Código de Negociação']]['quantidade'] = carteira[df_posicao.iloc[line]['Código de Negociação']]['quantidade'] + int(df_posicao.iloc[line]['Quantidade'])

st.markdown("# Carteira de Ações")

st.markdown("##")

st.markdown("### Indicadores")

col1, col2, col3, col4 = st.columns(4)
col5, col6, col7, col8 = st.columns(4)

total = 0
valor_carteira = 0
for acao in carteira:
    total += carteira[acao]["quantidade"]
    valor_carteira += carteira[acao]["quantidade"] * carteira[acao]["preco"]

maior_qtd = 0
ticker_maior_qtd = ""
menor_qtd = sys.maxsize
ticker_menor_qtd = ""
for acao in carteira:
    if carteira[acao]["quantidade"] > maior_qtd:
        maior_qtd = carteira[acao]["quantidade"]
        ticker_maior_qtd = acao
    if carteira[acao]["quantidade"] < menor_qtd:
        menor_qtd = carteira[acao]["quantidade"]
        ticker_menor_qtd = acao

for acao in carteira:
  valor_acao = carteira[acao]['preco'] * carteira[acao]['quantidade']
  carteira[acao]["percentual"] = valor_acao / valor_carteira * 100

maior_perc = 0
ticker_maior_perc = ""
menor_perc = sys.maxsize
ticker_menor_perc = ""
for acao in carteira:
    if carteira[acao]["percentual"] > maior_perc:
        maior_perc = carteira[acao]["percentual"]
        ticker_maior_perc = acao
    if carteira[acao]["percentual"] / valor_carteira < menor_perc:
        menor_perc = carteira[acao]["percentual"]
        ticker_menor_perc = acao

col1.metric("Total de Empresas:", len(carteira))
col2.metric("Total de Cotas", total)
col3.metric("Maior quantidade: " + ticker_maior_qtd, str(maior_qtd) + " cotas")
col4.metric("Menor quantidade: " + ticker_menor_qtd, str(menor_qtd) + " cotas")
col5.metric("Quantidade média de ações: ", round(total / len(carteira), 2))
col6.metric("Valor da Carteira", "R$ " + str(valor_carteira))
col7.metric("Maior percentual: " + ticker_maior_perc, str(round(maior_perc, 2)) + " %")
col8.metric("Menor percentual: " + ticker_menor_perc, str(round(menor_perc, 2)) + " %")

df = pd.DataFrame.from_dict(carteira, orient='index')

st.markdown("##")

st.markdown("### Percentual de Ações")
chart_data = df["percentual"]
st.bar_chart(chart_data, width=0, height=360)