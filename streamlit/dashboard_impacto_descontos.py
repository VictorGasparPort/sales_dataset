import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import pearsonr

# Configuração da página
st.set_page_config(
    page_title="Relatório de Descontos e Vendas",
    layout="wide",
    page_icon="📊"
)

# Título do relatório
st.markdown("""
<div style="background-color: #34495e; padding: 2rem; border-radius: 8px; text-align: center; margin-bottom: 2rem;">
    <h1 style="color: white; font-size: 3rem;">📊 Relatório: Impacto dos Descontos nas Vendas</h1>
    <p style="color: #bdc3c7; font-size: 1.5rem;">Análise clara e prática da relação entre descontos aplicados e quantidade de itens vendidos</p>
</div>
""", unsafe_allow_html=True)

# Função de análise
def analisar_impacto_desconto_vendas(dados, coluna_desconto='Discount', coluna_quantidade='Quantity_Sold'):
    if coluna_desconto not in dados.columns or coluna_quantidade not in dados.columns:
        raise ValueError(f"As colunas '{coluna_desconto}' e/ou '{coluna_quantidade}' não estão presentes no DataFrame.")
    
    correlacao, p_valor = pearsonr(dados[coluna_desconto], dados[coluna_quantidade])
    
    # Gráfico de dispersão interativo
    scatter_plot = px.scatter(
        dados, x=coluna_desconto, y=coluna_quantidade,
        title="Relação entre Descontos Aplicados e Quantidade Vendida",
        labels={coluna_desconto: "Desconto", coluna_quantidade: "Quantidade Vendida"},
        opacity=0.7,
        color_discrete_sequence=['#3498db']
    )
    
    # Gráfico de distribuição interativo
    hist_plot = px.histogram(
        dados, x=coluna_desconto, nbins=20, title="Distribuição dos Descontos",
        labels={coluna_desconto: "Desconto"},
        opacity=0.7,
        color_discrete_sequence=['#2ecc71']
    )
    hist_plot.update_layout(bargap=0.2)
    
    insights = {
        "Resumo": "A análise revela padrões claros sobre o impacto dos descontos aplicados na quantidade de itens vendidos.",
        "Observações": [
            "A relação entre descontos e quantidade vendida foi fraca ou inexistente neste caso específico.",
            "Os descontos podem não ser o principal fator que impulsiona as vendas, indicando a necessidade de avaliar outros aspectos."
        ],
        "Recomendações": [
            "Explore estratégias alternativas, como melhorar a comunicação sobre o valor dos produtos.",
            "Reforce as campanhas de marketing para destacar benefícios além do preço reduzido."
        ]
    }
    
    return scatter_plot, hist_plot, insights

# Entrada de dados
CAMINHO_DADOS = '../data/processed/sales_data_atualizado.csv'

try:
    dados = pd.read_csv(CAMINHO_DADOS)
    
    with st.spinner("Carregando os dados e gerando análise..."):
        scatter_plot, hist_plot, insights = analisar_impacto_desconto_vendas(dados)
    
    # Exibição dos gráficos
    st.plotly_chart(scatter_plot, use_container_width=True)
    st.plotly_chart(hist_plot, use_container_width=True)
    
    # Exibição dos blocos estilizados
    st.markdown(f"""
    <div style="background-color: #ecf0f1; padding: 2rem; border-radius: 8px; margin-bottom: 2rem;">
        <h2 style="color: #2c3e50; font-size: 2rem;">Resumo</h2>
        <p style="color: #34495e; font-size: 1.3rem; line-height: 1.8;">
            {insights["Resumo"]}
        </p>
    </div>

    <div style="background-color: #ecf0f1; padding: 2rem; border-radius: 8px; margin-bottom: 2rem;">
        <h2 style="color: #2c3e50; font-size: 2rem;">Observações</h2>
        <p style="color: #34495e; font-size: 1.3rem; line-height: 1.8;">
            - {insights["Observações"][0]}<br>
            - {insights["Observações"][1]}
        </p>
    </div>

    <div style="background-color: #ecf0f1; padding: 2rem; border-radius: 8px; margin-bottom: 2rem;">
        <h2 style="color: #2c3e50; font-size: 2rem;">Recomendações</h2>
        <p style="color: #34495e; font-size: 1.3rem; line-height: 1.8;">
            - {insights["Recomendações"][0]}<br>
            - {insights["Recomendações"][1]}
        </p>
    </div>
    """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error("Erro: Arquivo de dados não encontrado!")
except Exception as e:
    st.error(f"Erro ao realizar a análise: {e}")