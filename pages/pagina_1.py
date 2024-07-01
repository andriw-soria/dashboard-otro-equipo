import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
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

    st.sidebar.markdown("# Página  1️⃣")


    # Leer los datos
    file_path = 'data/ventas_corto_eliminar.xlsx'  # Actualiza esta ruta con la ubicación correcta del archivo
    df = pd.read_excel(file_path)

    df['Date'] = pd.to_datetime(df['Date'])

    # Configurar la aplicación de Streamlit
    st.title('Dashboard de Ventas')


    ventas_por_pais = df.groupby('Pais')['Total'].sum().reset_index()

    col1, col2 = st.columns(2)


    # Gráfica 1: Ventas por país
    with col1:
        st.header("Ventas por País")
        st.area_chart(ventas_por_pais.set_index('Pais'))

    # Gráfica 2: Evolución de las ventas
    with col2:
        st.header('‎ ')
        ventas_por_pais = df.groupby('Pais')['Total'].sum().reset_index().sort_values(by='Total', ascending=False)
        fig1, ax1 = plt.subplots()
        ax1.barh(ventas_por_pais['Pais'], ventas_por_pais['Total'], color='skyblue')
        ax1.set_xlabel('Total Ventas')
        ax1.set_title('Ventas por país')
        st.pyplot(fig1)

    # Gráfica 3: Ventas por país
    st.header("Gráfico de Dona")
    pie_chart = px.pie(ventas_por_pais,
                    title='Ventas por País',
                    values='Total',
                    names='Pais',
                    hole=0.4)
    st.plotly_chart(pie_chart)