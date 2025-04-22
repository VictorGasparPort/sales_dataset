import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Relatório de Eficácia dos Canais de Vendas",
    layout="wide",
    page_icon="📊"
)

# Título do relatório
st.markdown("""
<div style="background-color: #1e90ff; padding: 2rem; border-radius: 8px; text-align: center; margin-bottom: 2rem;">
    <h1 style="color: white; font-size: 3rem;">📊 Relatório: Eficácia dos Canais de Vendas</h1>
    <p style="color: #f0f8ff; font-size: 1.5rem;">Analisando o desempenho de vendas entre os diferentes canais</p>
</div>
""", unsafe_allow_html=True)

# Função de análise
def analisar_eficacia_canal_vendas(dados, coluna_canal='Sales_Channel', coluna_vendas='Sales_Amount'):
    if coluna_canal not in dados.columns or coluna_vendas not in dados.columns:
        raise ValueError(f"As colunas '{coluna_canal}' e/ou '{coluna_vendas}' não estão presentes no DataFrame.")
    
    # Agrupamento por canal de vendas e cálculo de estatísticas
    vendas_por_canal = dados.groupby(coluna_canal)[coluna_vendas].agg(['sum', 'mean', 'count']).reset_index()
    vendas_por_canal.rename(columns={'sum': 'Total_Vendas', 'mean': 'Media_Vendas', 'count': 'Quantidade_Vendas'}, inplace=True)
    
    # Identificar o canal com maior e menor volume de vendas
    canal_maior_venda = vendas_por_canal.iloc[vendas_por_canal['Total_Vendas'].idxmax()]
    canal_menor_venda = vendas_por_canal.iloc[vendas_por_canal['Total_Vendas'].idxmin()]
    
    # Gráfico de barras horizontal interativo
    bar_chart = px.bar(
        vendas_por_canal, x='Total_Vendas', y=coluna_canal,
        title="Total de Vendas por Canal de Vendas",
        text='Total_Vendas', orientation='h', color=coluna_canal,
        color_discrete_sequence=px.colors.sequential.Blues  # Paleta em tons de azul
    )
    bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    bar_chart.update_layout(xaxis_title="Total de Vendas (R$)", yaxis_title="Canal de Vendas")
    
    # Construção de insights
    insights = {
        "Resumo": "A análise compara o desempenho de diferentes canais de vendas, identificando oportunidades estratégicas.",
        "Observações": [
            f"O canal com maior volume de vendas foi '{canal_maior_venda[coluna_canal]}', totalizando R$ {canal_maior_venda['Total_Vendas']:.2f}.",
            f"O canal com menor volume de vendas foi '{canal_menor_venda[coluna_canal]}', com R$ {canal_menor_venda['Total_Vendas']:.2f}."
        ],
        "Recomendações": [
            "Expanda os esforços no canal mais eficaz para maximizar os lucros.",
            "Implemente iniciativas para melhorar o desempenho do canal menos eficaz.",
            "Monitore regularmente o desempenho dos canais para otimizar estratégias ao longo do tempo."
        ]
    }
    
    return bar_chart, insights

# Entrada de dados
CAMINHO_DADOS = '../data/processed/sales_data_atualizado.csv'

try:
    dados = pd.read_csv(CAMINHO_DADOS)
    
    with st.spinner("Carregando os dados e gerando análise..."):
        bar_chart, insights = analisar_eficacia_canal_vendas(dados)
    
    # Exibição do gráfico
    st.plotly_chart(bar_chart, use_container_width=True)
    
    # Exibição dos blocos estilizados
    st.markdown(f"""
    <div style="background-color: #f0f8ff; padding: 2rem; border-radius: 8px; margin-bottom: 2rem;">
        <h2 style="color: #000000; font-size: 2rem;">Resumo</h2>
        <p style="color: #000000; font-size: 1.3rem; line-height: 1.8;">
            {insights["Resumo"]}
        </p>
    </div>

    <div style="background-color: #f0f8ff; padding: 2rem; border-radius: 8px; margin-bottom: 2rem;">
        <h2 style="color: #000000; font-size: 2rem;">Observações</h2>
        <p style="color: #000000; font-size: 1.3rem; line-height: 1.8;">
            - {insights["Observações"][0]}<br>
            - {insights["Observações"][1]}
        </p>
    </div>

    <div style="background-color: #f0f8ff; padding: 2rem; border-radius: 8px; margin-bottom: 2rem;">
        <h2 style="color: #000000; font-size: 2rem;">Recomendações</h2>
        <p style="color: #000000; font-size: 1.3rem; line-height: 1.8;">
            - {insights["Recomendações"][0]}<br>
            - {insights["Recomendações"][1]}<br>
            - {insights["Recomendações"][2]}
        </p>
    </div>
    """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error("Erro: Arquivo de dados não encontrado!")
except Exception as e:
    st.error(f"Erro ao realizar a análise: {e}")