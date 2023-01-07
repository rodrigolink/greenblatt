import streamlit as st
import pandas as pd
import requests

st.set_page_config(
   page_title="Fórmula Mágica de Greenblatt",
   layout="wide",

)


url = 'http://www.fundamentus.com.br/resultado.php'
header = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"  
 }



st.title('Fórmula Mágica de Greenblatt')
st.write('Ordenação dos dados divulgados pelas empresas disponíveis na Bolsa de \
            Valores, segundo os critérios de Joel Greenblatt, de modo a facilitar \
            a escolha de novos investimentos.')
st.write('Dados obtidos da Fundamentus.')
r = requests.get(url, headers=header)
df = pd.read_html(r.text,  decimal=',', thousands='.')[0]

for coluna in ['Div.Yield', 'Mrg Ebit', 'Mrg. Líq.', 'ROIC', 'ROE', 'Cresc. Rec.5a']:
  df[coluna] = df[coluna].str.replace('.', '')
  df[coluna] = df[coluna].str.replace(',', '.')
  df[coluna] = df[coluna].str.rstrip('%').astype(float) / 100

# Filtro de Liquidez: > 1 Milhão/2 meses
df = df[df['Liq.2meses'] > 1000000]

# Rankeamento - P/L (>0) e ROE

df['Ranking_P/L'] = df[df['P/L']>0]['P/L'].rank()
df['Ranking_ROE'] = df['ROE'].rank(ascending=False)

df['Primeiro_rank'] = df['Ranking_P/L']+df['Ranking_ROE']
st.write('Ranking usando P/L>0 e ROE')
st.table(df[['Primeiro_rank','Papel','P/L','Ranking_P/L','ROE','Ranking_ROE']].sort_values(by=['Primeiro_rank']).head(15))

df['Ranking_EV/EBIT'] = df[df['EV/EBIT'] > 0]['EV/EBIT'].rank()
df['Ranking_ROIC'] = df['ROE'].rank(ascending=False)
df['Segundo_rank'] = df['Ranking_EV/EBIT']+df['Ranking_ROIC']
st.write('Ranking usando EV/EBIT>0 e ROIC, (NÃO VALE PARA FINANCEIRAS E BANCOS!!!)')
st.table(df[['Segundo_rank','Papel','EV/EBIT','Ranking_EV/EBIT','ROIC','Ranking_ROIC']].sort_values(by=['Segundo_rank']).head(15))

df['Final_rank'] = df['Primeiro_rank']+df['Segundo_rank']
st.write('Ranking usando P/L>0, ROE, EV/EBIT>0 e ROIC')
st.table(df[['Final_rank','Papel','Primeiro_rank','P/L','Ranking_P/L','ROE','Ranking_ROE','Segundo_rank','EV/EBIT','Ranking_EV/EBIT','ROIC','Ranking_ROIC']].dropna().sort_values(by=['Final_rank']).head(15))



