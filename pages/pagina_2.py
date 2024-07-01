import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from login import login, logout

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

if not st.session_state["logged_in"]:
    login()
else:

    st.set_page_config(page_title="Dashboard")
    st.markdown("# DASHBOARD 2024 - PARA OTRO GRUPO")
    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 20px;">
            <span style="font-size: 18px; margin-right: 10px;">Bienvenido - {st.session_state['username']}</span>
        </div>
        <style>
            button:hover {{
                background-color: #d32f2f;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Cerrar Sesión"):
        logout()

    st.sidebar.markdown("# Página  2️⃣")


    data_path = 'data/ventas_corto_eliminar.xlsx'
    data = pd.read_excel(data_path)

    

    st.title("Análisis Gráfico de Ventas")

    # Gráfico de dispersión
    st.header("Gráfico de Dispersión")
    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x='Cantidad', y='Total', hue='Pais', ax=ax)
    st.pyplot(fig)

    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de barras
        st.header("Gráfico de Barras")
        fig, ax = plt.subplots()
        ventas_por_cliente = data.groupby('IdCliente')['Total'].sum().nlargest(5)
        ventas_por_cliente.plot(kind='bar', ax=ax, color=['blue', 'orange'])
        st.pyplot(fig)

    with col2:
        # Preparar datos para el gráfico de línea
        ventas_por_cliente = data.groupby('IdCliente')['Total'].sum().nlargest(5)
        line_data = pd.DataFrame(ventas_por_cliente).reset_index()
        line_data.columns = ['Cliente', 'Ventas Totales']

        # Gráfico de dona
        st.header("Gráfico de Dona")
        fig, ax = plt.subplots()
        ventas_por_pais = data.groupby('Pais')['Total'].sum()
        ventas_por_pais.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
        ax.axis('equal')  # Para hacer un gráfico circular
        st.pyplot(fig)


