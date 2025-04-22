import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Relatório de Vendas por Categoria",
    layout="wide",
    page_icon="📊"
)

# Título do relatório
st.markdown("""
<div style="background-color: #34495e; padding: 2rem; border-radius: 8px; text-align: center; margin-bottom: 2rem;">
    <h1 style="color: white; font-size: 3rem;">📊 Relatório: Vendas por Categoria de Produto</h1>
    <p style="color: #bdc3c7; font-size: 1.5rem;">Análise do desempenho de vendas com base nas categorias de produtos</p>
</div>
""", unsafe_allow_html=True)

# Função de análise
def analisar_vendas_por_categoria(dados, coluna_categoria='Product_Category', coluna_vendas='Sales_Amount'):
    if coluna_categoria not in dados.columns or coluna_vendas not in dados.columns:
        raise ValueError(f"As colunas '{coluna_categoria}' e/ou '{coluna_vendas}' não estão presentes no DataFrame.")
    
    # Agrupamento por categoria e cálculo de estatísticas
    vendas_por_categoria = dados.groupby(coluna_categoria)[coluna_vendas].agg(['sum', 'mean', 'count']).reset_index()
    vendas_por_categoria.rename(columns={'sum': 'Total_Vendas', 'mean': 'Media_Vendas', 'count': 'Quantidade_Vendas'}, inplace=True)
    vendas_por_categoria.sort_values(by='Total_Vendas', ascending=False, inplace=True)
    
    # Identificar a categoria com maior e menor volume de vendas
    categoria_maior_venda = vendas_por_categoria.iloc[0]
    categoria_menor_venda = vendas_por_categoria.iloc[-1]
    
    # Gráfico de barras horizontal interativo
    bar_chart = px.bar(
        vendas_por_categoria, y=coluna_categoria, x='Total_Vendas', 
        title='Total de Vendas por Categoria de Produto',
        text='Total_Vendas', orientation='h', color=coluna_categoria,
        color_discrete_sequence=px.colors.sequential.Greys  # Paleta em preto e branco
    )
    bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    bar_chart.update_layout(xaxis_title="Total de Vendas (R$)", yaxis_title="Categoria de Produto")
    
    # Construção de insights
    insights = {
        "Resumo": "A análise evidencia quais categorias de produtos apresentam o maior e o menor desempenho em vendas.",
        "Observações": [
            f"A categoria com maior volume de vendas foi '{categoria_maior_venda[coluna_categoria]}', totalizando R$ {categoria_maior_venda['Total_Vendas']:.2f}.",
            f"A categoria com menor volume de vendas foi '{categoria_menor_venda[coluna_categoria]}', com R$ {categoria_menor_venda['Total_Vendas']:.2f}."
        ],
        "Recomendações": [
            "Invista em campanhas publicitárias para a categoria com maior potencial de vendas.",
            "Implemente promoções estratégicas para melhorar o desempenho da categoria menos vendida.",
            "Realize análises contínuas para acompanhar o desempenho das categorias e ajustar as ações conforme necessário."
        ]
    }
    
    return bar_chart, insights

# Entrada de dados
CAMINHO_DADOS = '../data/processed/sales_data_atualizado.csv'

try:
    dados = pd.read_csv(CAMINHO_DADOS)
    
    with st.spinner("Carregando os dados e gerando análise..."):
        bar_chart, insights = analisar_vendas_por_categoria(dados)
    
    # Exibição do gráfico
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