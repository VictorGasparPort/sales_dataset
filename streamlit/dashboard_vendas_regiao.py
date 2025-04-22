import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(
    page_title="Relatório de Vendas Corporativo",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📈"
)

def analisar_vendas_por_regiao(dados, coluna_regiao='Region', coluna_vendas='Sales_Amount'):
    """
    Função original mantida com integridade
    """
    if coluna_regiao not in dados.columns or coluna_vendas not in dados.columns:
        raise ValueError(f"Colunas '{coluna_regiao}' ou '{coluna_vendas}' não encontradas")
    
    vendas_por_regiao = dados.groupby(coluna_regiao)[coluna_vendas].agg(['sum', 'mean']).reset_index()
    vendas_por_regiao.rename(columns={'sum': 'Total_Vendas', 'mean': 'Media_Vendas'}, inplace=True)
    
    regiao_maior = vendas_por_regiao.loc[vendas_por_regiao['Total_Vendas'].idxmax()]
    regiao_menor = vendas_por_regiao.loc[vendas_por_regiao['Total_Vendas'].idxmin()]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(vendas_por_regiao[coluna_regiao], vendas_por_regiao['Total_Vendas'], 
           color='#2ecc71', edgecolor='#27ae60', linewidth=0.7)
    ax.set_title('Distribuição de Vendas por Região', fontsize=18, pad=20)
    ax.set_xlabel('', fontsize=12)
    ax.set_ylabel('Valor Total (R$)', fontsize=12, labelpad=15)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle=':', alpha=0.7)
    plt.tight_layout()
    
    insights = {
        "Resumo": "Análise comparativa do desempenho comercial por região geográfica",
        "Topo": {
            "Região": regiao_maior[coluna_regiao],
            "Total": regiao_maior['Total_Vendas'],
            "Média": regiao_maior['Media_Vendas']
        },
        "Base": {
            "Região": regiao_menor[coluna_regiao],
            "Total": regiao_menor['Total_Vendas'],
            "Média": regiao_menor['Media_Vendas']
        },
        "Detalhes": vendas_por_regiao.to_dict(orient='records')
    }
    
    return fig, insights

# Implementação do relatório
CAMINHO_DADOS = '../data/processed/sales_data_atualizado.csv'

try:
    # Cabeçalho corporativo
    st.markdown("""
    <div style="background:#34495e;padding:2rem;border-radius:10px;margin-bottom:3rem">
        <h1 style="color:white;text-align:center;margin:0">Relatório de Performance Comercial</h1>
        <p style="color:#bdc3c7;text-align:center;margin:0.5rem 0">Análise Trimestral - Dados Atualizados</p>
    </div>
    """, unsafe_allow_html=True)

    # Processamento dos dados
    dados = pd.read_csv(CAMINHO_DADOS)
    figura, metricas = analisar_vendas_por_regiao(dados)
    
    # Seção gráfica
    with st.container():
        st.pyplot(figura)
        st.markdown("---")
    
    # Painel de métricas
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🏅 Região Destaque", help="Maior volume absoluto de vendas")
        st.metric(
            label=f"**{metricas['Topo']['Região']}**",
            value=f"R$ {metricas['Topo']['Total']:,.2f}",
            delta=f"Média: R$ {metricas['Topo']['Média']:,.2f}",
            delta_color="normal"
        )
    
    with col2:
        st.markdown("### 📉 Região com Desafios", help="Menor volume absoluto de vendas")
        st.metric(
            label=f"**{metricas['Base']['Região']}**",
            value=f"R$ {metricas['Base']['Total']:,.2f}",
            delta=f"Média: R$ {metricas['Base']['Média']:,.2f}",
            delta_color="inverse"
        )
    
    # Tabela analítica
    st.markdown("### 📊 Comparativo Regional Detalhado")
    df_detalhes = pd.DataFrame(metricas['Detalhes'])
    st.dataframe(
        df_detalhes.style.format({
            'Total_Vendas': 'R$ {:.2f}',
            'Media_Vendas': 'R$ {:.2f}'
        }).applymap(lambda x: 'color: #2ecc71' if x == df_detalhes['Total_Vendas'].max() else 'color: #e74c3c', 
                   subset=['Total_Vendas']),
        column_config={
            "Region": st.column_config.TextColumn("Região", width="medium"),
            "Total_Vendas": st.column_config.ProgressColumn(
                "Faturamento Total",
                format="R$ %.2f",
                min_value=0,
                max_value=df_detalhes['Total_Vendas'].max()
            ),
            "Media_Vendas": st.column_config.NumberColumn(
                "Média por Operação",
                format="R$ %.2f",
                help="Valor médio por transação comercial"
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Análise estratégica
    with st.expander("🔍 Insights Analíticos Avançados"):
        diferenca_total = metricas['Topo']['Total'] - metricas['Base']['Total']
        variacao_media = ((df_detalhes['Media_Vendas'].max() / df_detalhes['Media_Vendas'].min() - 1) * 100)
        
        st.markdown(f"""
        #### Principais Observações:
        - **Disparidade Comercial:** Diferença de R$ {diferenca_total:,.2f} entre regiões extremas
        - **Variação de Eficiência:** {variacao_media:.1f}% na comparação de médias regionais
        - **Concentração de Receita:** {metricas['Topo']['Total']/df_detalhes['Total_Vendas'].sum()*100:.1f}% do total faturado pela região líder
        
        #### Recomendações Estratégicas:
        1. Implementar plano de capacitação para equipe da região **{metricas['Base']['Região']}**
        2. Replicar boas práticas da região **{metricas['Topo']['Região']}**
        3. Realizar estudo de mercado para potencial de crescimento regional
        """)
    
except FileNotFoundError:
    st.error("Arquivo de dados não encontrado no caminho especificado")
except Exception as e:
    st.error(f"Erro crítico durante a análise: {str(e)}")

# Estilos customizados
st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        color: #2c3e50;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.2rem !important;
    }
    .st-emotion-cache-1y4p8pa {
        padding: 2rem 1rem;
    }
    .stDataFrame {
        border: 1px solid #ecf0f1 !important;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)