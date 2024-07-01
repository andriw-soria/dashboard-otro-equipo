import streamlit as st
import pandas as pd
import plotly.express as px
from login import login, logout

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

if not st.session_state["logged_in"]:
    login()
else:

    st.set_page_config(page_title="Gráficos")
    st.markdown("# DASHBOARD 2024 - PARA OTRO GRUPO")
    st.sidebar.markdown("# Main Page")


    data_path = 'data/ventas_corto_eliminar.xlsx'
    data = pd.read_excel(data_path)


    st.title("Análisis Gráfico de Ventas")



    # Preparar datos para el gráfico de línea
    ventas_por_cliente = data.groupby('IdCliente')['Total'].sum().nlargest(5)
    line_data = pd.DataFrame(ventas_por_cliente).reset_index()
    line_data.columns = ['Cliente', 'Ventas Totales']

    # Gráfica de ventas por país
    st.header("Ventas Totales por País")
    ventas_por_pais = data.groupby('Pais')['Total'].sum()
    st.bar_chart(ventas_por_pais)

    # Gráfico de línea v2
    st.header("Ventas Totales por Cliente")
    st.line_chart(line_data.set_index('Cliente'))


    ventas_por_pais = data.groupby('Pais')['Total'].sum().reset_index()

    st.header("Ventas por País")
    pie_chart = px.pie(ventas_por_pais,
                    values='Total',
                    names='Pais',
                    hole=0.4)  # Centro hueco para el efecto de dona

    st.plotly_chart(pie_chart)

    # Gráfico de área
    st.header("Ventas por País")
    st.area_chart(ventas_por_pais.set_index('Pais'))


