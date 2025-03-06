import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

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

    st.set_page_config(page_title= 'Análise de Pedidos e Faturamento por Categoria', layout= 'wide')

    return None

def filtra_df(df):
    # Side Bar

    st.sidebar.header('Filtros')

    lista_categoria = list(df['product_category_name'].unique())

    categorias_selecionados = st.sidebar.multiselect('Selecione uma Categoria', 
                                                    options = lista_categoria,
                                                    default=lista_categoria[0:30])

    order_items_df = df[df['product_category_name'].isin(categorias_selecionados)]

    return order_items_df

def big_numbers(df):
    st.subheader('Indicadores Gerais')

    total_pedidos = df['order_id'].nunique()
    total_faturamento = df['total_price'].sum()
    ticket_medio = total_faturamento / total_pedidos

    # Cria 3 colunas
    col1, col2, col3 = st.columns(3)

    col1.metric("Total de Pedidos", total_pedidos)
    col2.metric("Faturamento Total", f"R${total_faturamento:,.2f}")
    col3.metric("Ticket Médio", f"R${ticket_medio:,.2f}")

    return None

def visao_pedido(df):
    st.subheader('Visão Pedidos por Categoria')

    col1, col2= st.columns(2)

    # Gráfico Pedidos x Mês

    pedidos_mes = df[['order_purchase_year_month', 'order_id']].groupby('order_purchase_year_month').count().reset_index()

    fig1, ax1 = plt.subplots()
    sns.lineplot(data = pedidos_mes, x= 'order_purchase_year_month', y= 'order_id', ax=ax1)
    ax1.set_title('Qtd. Pedidos por Mês') 
    plt.xlabel('Ano-Mês')
    plt.ylabel('Qtd. Pedidos')
    plt.xticks(rotation=60)
    col1.pyplot(fig1)

    # Gráfico Pedidos x Categoria
    categoria_pedidos = df[['product_category_name', 'order_id']].groupby('product_category_name').nunique().sort_values('order_id', ascending=False)
    fig2, ax2 = plt.subplots()
    sns.barplot(data=categoria_pedidos, x='product_category_name', y='order_id', ax=ax2)
    plt.title('Qtd. Pedidos por Categoria')
    plt.xlabel('Categoria')
    plt.ylabel('Qtd. Pedidos')
    plt.xticks(rotation=80)
    col2.pyplot(fig2)

    return None

def visao_faturamento(df):
    st.subheader('Visão Faturamento por Categoria')

    col1, col2= st.columns(2)

    # Gráfico Faturamento x Mês

    faturamento_mes = order_items_df[['order_purchase_year_month', 'total_price']].groupby('order_purchase_year_month').sum().reset_index()

    fig1, ax1 = plt.subplots()
    sns.lineplot(data = faturamento_mes, x='order_purchase_year_month', y='total_price', ax=ax1)
    plt.title('Faturamento Mensal')
    plt.xlabel('Mês')
    plt.ylabel('Faturamento (R$)')
    plt.xticks(rotation=60)
    col1.pyplot(fig1)


    # Gráfico Faturamento x Categoria

    faturamento_categoria = order_items_df[['product_category_name', 'total_price', 'product_id']].groupby('product_category_name').agg({'total_price': 'sum',
                                                                                                                'product_id': 'nunique'}).sort_values('total_price', ascending=False).reset_index()

    fig2, ax2 = plt.subplots()
    sns.barplot(data=faturamento_categoria, x='product_category_name', y='total_price', ax=ax2)
    plt.title('Faturamento por Categoria')
    plt.xlabel('Categoria')
    plt.ylabel('Faturamento (R$)')
    plt.xticks(rotation=80)
    col2.pyplot(fig2)

    return None

if __name__ == '__main__':

    # Definindo parâmetros
    definicao_parametros_graficos()

    # Carregar os dados
    order_items_df = pd.read_csv('datasets/order_items_cleaned.csv.gz', compression='gzip')

    # Título
    st.title('Análise de Pedidos e Faturamento por Categoria')

    # Side Bar (Filtros)

    order_items_df = filtra_df(order_items_df)

    # Big Numbers

    big_numbers(order_items_df)

    # Visão Pedidos

    visao_pedido(order_items_df)

    # Visão Faturamento

    visao_faturamento(order_items_df)



