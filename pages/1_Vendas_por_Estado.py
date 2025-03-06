
# importação de bibliotecas
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


def definicao_parametros_graficos(): 
    # Configurações gerais
    sns.set_theme()
    plt.rcParams['figure.figsize'] = (6, 3) # Tamanho da figura
    plt.rcParams['axes.titlesize'] = 10     # Tamanho do título
    plt.rcParams['axes.labelsize'] = 8      # Tamanho dos rótulos
    plt.rcParams['xtick.labelsize'] = 7     # Tamanho dos ticks eixo x
    plt.rcParams['ytick.labelsize'] = 7     # Tamanho dos ticks eixo y
    plt.rcParams['legend.fontsize'] = 8     # Tamanho de legenda
    plt.rcParams['lines.markersize'] = 4    # Tamanho dos marcadores das linhas

    st.set_page_config(page_title= 'Análise de Vendas por Estado', layout= 'wide')

    return None

def filtra_df(df):
    # Side Bar
    st.sidebar.header('Filtros')

    lista_estados = sorted(list(df['seller_state'].unique()))

    estados_selecionados = st.sidebar.multiselect('Selecione um Estado', 
                                                  options = lista_estados,
                                                  default=lista_estados)

    customer_df_filtered = df[df['customer_state'].isin(estados_selecionados)]
    sellers_df_filtered = df[df['seller_state'].isin(estados_selecionados)]

    return customer_df_filtered, sellers_df_filtered

def big_numbers(c_df, s_df):
    st.subheader('Indicadores Gerais')

    total_vendas = c_df['total_price'].sum()
    total_customer = c_df['customer_unique_id'].nunique()
    total_sellers = s_df['seller_id'].nunique()

    # Cria 3 colunas
    col1, col2, col3 = st.columns(3)

    col1.metric('Vendas Totais', f'R$ {total_vendas:,.2f}')
    col2.metric('Clientes Únicos', f'{total_customer:,.0f}')
    col3.metric('Vendedores Únicos', f'{total_sellers:,.0f}')

    return None

def visoes_gerais(c_df, s_df):
    st.subheader('Visão Geral das Vendas por Estado')

    col1, col2, col3 = st.columns(3)

    # Gráfico Vendas x Estado

    vendas_estado = c_df[['customer_state', 'total_price']].groupby('customer_state').sum().sort_values('total_price', ascending=False).reset_index()

    fig1, ax1 = plt.subplots()
    sns.barplot(data = vendas_estado, x= 'customer_state', y= 'total_price', ax=ax1)
    ax1.set_title('Vendas Totais por Estado') 
    plt.xlabel('Estado')
    plt.ylabel('Vendas (R$)')
    col1.pyplot(fig1)

    # Gráfico Clientes x Estado

    clientes_estado = c_df[['customer_state', 'customer_unique_id']].groupby('customer_state').nunique().sort_values('customer_unique_id', ascending=False).reset_index()
    fig2, ax2 = plt.subplots()
    sns.barplot(data = clientes_estado, x= 'customer_state', y= 'customer_unique_id', ax=ax2)
    ax2.set_title('Clientes Únicos por Estado') 
    plt.xlabel('Estado')
    plt.ylabel('Clientes Únicos')
    col2.pyplot(fig2)

    # Gráfico Vendedores x Estado

    vendedores_estado = s_df[['seller_state', 'seller_id']].groupby('seller_state').nunique().sort_values('seller_id', ascending=False).reset_index()
    fig3, ax3 = plt.subplots()
    sns.barplot(data= vendedores_estado, x= 'seller_state', y='seller_id', ax=ax3)
    ax3.set_title('Vendedores Únicos por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Vendedores Únicos')
    col3.pyplot(fig3)

    return None

def visoes_temporais(c_df, s_df):
    st.subheader('Visão Temporal por Estado')

    col1, col2, col3 = st.columns(3)

    # Gráfico Venda x Tempo

    vendas_temporal = c_df[['order_purchase_year_month', 'total_price']].groupby('order_purchase_year_month').sum().reset_index()

    fig1, ax1 = plt.subplots()
    sns.lineplot(data= vendas_temporal, x= 'order_purchase_year_month', y= 'total_price', ax= ax1)
    ax1.set_title(f'Vendas (R$) por mês')
    plt.xlabel('Ano-Mês')
    plt.ylabel('Vendas (R$)')
    plt.xticks(rotation=60)
    col1.pyplot(fig1)

    # Gráfico Clientes x Tempo

    clientes_temporal = c_df[['order_purchase_year_month', 'customer_unique_id']].groupby('order_purchase_year_month').nunique().reset_index()

    fig2, ax2 = plt.subplots()
    sns.lineplot(data = clientes_temporal, x = 'order_purchase_year_month', y = 'customer_unique_id', ax = ax2)
    ax2.set_title(f'Clientes Únicos por mês')
    plt.xlabel('Ano-Mês')
    plt.ylabel('Clientes Únicos')
    plt.xticks(rotation=60)
    col2.pyplot(fig2)

    # Gráfico Vendedores x Tempo

    vendedores_temporal = s_df[['order_purchase_year_month', 'seller_id']].groupby('order_purchase_year_month').nunique().reset_index()

    fig3, ax3 = plt.subplots()
    sns.lineplot(data = vendedores_temporal, x = 'order_purchase_year_month', y = 'seller_id', ax = ax3)
    ax3.set_title(f'Vendedores Únicos por mês')
    plt.xlabel('Ano-Mês')
    plt.ylabel('Vendedores Únicos')
    plt.xticks(rotation=60)
    col3.pyplot(fig3)

    return None

if __name__ == '__main__':

    # Definindo parâmetros
    definicao_parametros_graficos()

    # Leitura do arquivo csv
    order_items_df = pd.read_csv('datasets/order_items_cleaned.csv.gz', compression='gzip')

    # Título
    st.title('Análise de Vendas por Estado')

    # Side Bar (Filtros)

    customer_df_filtered, sellers_df_filtered = filtra_df(order_items_df)

    # Big Numbers

    big_numbers(customer_df_filtered, sellers_df_filtered)

    # Visões Gerais

    visoes_gerais(customer_df_filtered, sellers_df_filtered)

    # Visões Temporais (mês) para os Estados Selecionados

    visoes_temporais(customer_df_filtered, sellers_df_filtered)
