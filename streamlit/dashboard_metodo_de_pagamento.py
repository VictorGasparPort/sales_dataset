import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Relatório de Métodos de Pagamento e Vendas",
    layout="wide",
    page_icon="💳"
)

# Título do relatório
st.markdown("""
<div style="background-color: #34495e; padding: 2rem; border-radius: 8px; text-align: center; margin-bottom: 2rem;">
    <h1 style="color: white; font-size: 3rem;">💳 Relatório: Impacto dos Métodos de Pagamento nas Vendas</h1>
    <p style="color: #bdc3c7; font-size: 1.5rem;">Explorando como os diferentes métodos de pagamento influenciam o total de vendas</p>
</div>
""", unsafe_allow_html=True)

# Função de análise
def analisar_metodo_pagamento(dados, coluna_pagamento='Payment_Method', coluna_vendas='Sales_Amount'):
    if coluna_pagamento not in dados.columns or coluna_vendas not in dados.columns:
        raise ValueError(f"As colunas '{coluna_pagamento}' e/ou '{coluna_vendas}' não estão presentes no DataFrame.")
    
    # Agrupamento por método de pagamento e cálculo de estatísticas
    vendas_por_pagamento = dados.groupby(coluna_pagamento)[coluna_vendas].agg(['sum', 'mean', 'count']).reset_index()
    vendas_por_pagamento.rename(columns={'sum': 'Total_Vendas', 'mean': 'Media_Vendas', 'count': 'Quantidade_Transacoes'}, inplace=True)
    vendas_por_pagamento.sort_values(by='Total_Vendas', ascending=False, inplace=True)
    
    # Identificar o método com maior e menor volume de vendas
    metodo_maior_venda = vendas_por_pagamento.iloc[0]
    metodo_menor_venda = vendas_por_pagamento.iloc[-1]
    
    # Gráfico de pizza interativo
    pie_chart = px.pie(
        vendas_por_pagamento, values='Total_Vendas', names=coluna_pagamento,
        title='Distribuição dos Métodos de Pagamento por Total de Vendas',
        color_discrete_sequence=px.colors.qualitative.Plotly  # Correção para uma paleta válida
    )
    
    # Gráfico de barras interativo
    bar_chart = px.bar(
        vendas_por_pagamento, x=coluna_pagamento, y='Total_Vendas', 
        title='Total de Vendas por Método de Pagamento',
        text='Total_Vendas', color=coluna_pagamento,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    bar_chart.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    bar_chart.update_layout(xaxis_title="Método de Pagamento", yaxis_title="Total de Vendas (R$)")
    
    # Construção de insights
    insights = {
        "Resumo": "A análise dos métodos de pagamento revela padrões importantes para estratégias de vendas.",
        "Observações": [
            f"O método de pagamento com maior volume de vendas foi '{metodo_maior_venda[coluna_pagamento]}', representando R$ {metodo_maior_venda['Total_Vendas']:.2f}.",
            f"O método de pagamento com menor volume de vendas foi '{metodo_menor_venda[coluna_pagamento]}', com R$ {metodo_menor_venda['Total_Vendas']:.2f}."
        ],
        "Recomendações": [
            "Incentive o método mais popular para maximizar vendas.",
            "Desenvolva campanhas que promovam os métodos menos utilizados.",
            "Monitore continuamente os métodos de pagamento para ajustar estratégias conforme necessário."
        ]
    }
    
    return pie_chart, bar_chart, insights

# Entrada de dados
CAMINHO_DADOS = '../data/processed/sales_data_atualizado.csv'

try:
    dados = pd.read_csv(CAMINHO_DADOS)
    
    with st.spinner("Carregando dados e gerando análise..."):
        pie_chart, bar_chart, insights = analisar_metodo_pagamento(dados)
    
    # Exibição dos gráficos
    st.plotly_chart(pie_chart, use_container_width=True)
    st.plotly_chart(bar_chart, use_container_width=True)
    
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
            - {insights["Recomendações"][1]}<br>
            - {insights["Recomendações"][2]}
        </p>
    </div>
    """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error("Erro: Arquivo de dados não encontrado!")
except Exception as e:
    st.error(f"Erro ao realizar a análise: {e}")