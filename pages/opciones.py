import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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


    file_path = 'data/ventas_corto_eliminar.xlsx'
    df = pd.read_excel(file_path)

    df['Date'] = pd.to_datetime(df['Date'])

    st.title('Dashboard de Ventas')

    # Filtros
    paises = ['Todos'] + df['Pais'].unique().tolist()
    clientes = ['Todos'] + df['IdCliente'].unique().tolist()

    pais = st.sidebar.selectbox('Selecciona un país', paises)
    cliente = st.sidebar.selectbox('Selecciona un cliente', clientes)
    fecha_inicio = st.sidebar.date_input('Fecha de inicio', df['Date'].min())
    fecha_fin = st.sidebar.date_input('Fecha de fin', df['Date'].max())

    # Convertir las fechas a datetime
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    # Filtrar los datos
    df_filtered = df[(df['Date'] >= fecha_inicio) & (df['Date'] <= fecha_fin)]

    if pais != 'Todos':
        df_filtered = df_filtered[df_filtered['Pais'] == pais]

    if cliente != 'Todos':
        df_filtered = df_filtered[df_filtered['IdCliente'] == cliente]

    # Datos para las gráficas
    ventas_por_pais = df_filtered.groupby('Pais')['Total'].sum().reset_index().sort_values(by='Total', ascending=False)

    # Mostrar datos filtrados
    st.subheader('Datos filtrados')
    st.write(df_filtered)

    # Gráfica Evolución de las ventas
    st.subheader('Evolución de las ventas')
    ventas_por_fecha = df_filtered.groupby('Date')['Total'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.plot(ventas_por_fecha['Date'], ventas_por_fecha['Total'], marker='o')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Total Ventas')
    ax.set_title('Evolución de las ventas')
    st.pyplot(fig)

    # Gráfico de pastel
    st.subheader('Distribución de las ventas por país - Gráfico de Pastel')
    fig, ax = plt.subplots()
    ax.pie(ventas_por_pais['Total'], labels=ventas_por_pais['Pais'], autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    ax.set_title('Distribución de las ventas por país')
    st.pyplot(fig)

    # Gráfico de dona
    st.subheader('Distribución de las ventas por país - Gráfico de Dona')
    fig, ax = plt.subplots()
    ax.pie(ventas_por_pais['Total'], labels=ventas_por_pais['Pais'], autopct='%1.1f%%', colors=plt.cm.Paired.colors, wedgeprops=dict(width=0.3))
    ax.set_title('Distribución de las ventas por país')
    st.pyplot(fig)

    # Gráfico de barras
    st.subheader('Distribución de las ventas por país - Gráfico de Barras')
    fig, ax = plt.subplots()
    ax.bar(ventas_por_pais['Pais'], ventas_por_pais['Total'], color=plt.cm.Paired.colors)
    ax.set_title('Distribución de las ventas por país')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
