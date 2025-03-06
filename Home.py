import streamlit as st

st.set_page_config(page_title='Home')

st.markdown(
    """
    ### Dashboard construído para acompanhar as métricas de Vendas e Pedidos.
    ### Como utilizar esse Dashboard?
    - **Visão Vendas por Estado:**          
        - Indicadores Gerais: Vendas Totais, Clientes Únicos, Vendedores Únicos
        - Visão Geral das Vendas por Estado: 
        - Visão Temporal por Estado 
    - **Visão Pedidos e Faturamento por Categoria:**            
        - Indicadores Gerais: Total de Pedidos, Faturamento Total, Ticket Médio
        - Visão Pedidos por Categoria
        - Visão Faturamento por Categoria    pip freeze
        - **Importante:** Nessa visão, como padrão, será exibido as 30 categorias que mais tiveram pedidos ou mais faturarem. Você poderá escolher mais ou menos categorias pelo menu lateral. 
""")
