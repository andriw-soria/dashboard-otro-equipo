import streamlit as st
import pandas as pd
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

    data_path = 'data/ventas_corto_eliminar.xlsx'
    data = pd.read_excel(data_path)


    paises = ['Todos'] + data['Pais'].unique().tolist()
    pais = st.sidebar.selectbox('Selecciona un país', paises)

    if pais == 'Todos':
        df_filtered = data
    else :
        df_filtered = data[data['Pais'] == pais]

    st.title("Dashboard de Ventas")
    st.header("Datos de Ventas")
    st.dataframe(df_filtered)



    total_ventas = data['Total'].sum()
    total_cantidad = data['Cantidad'].sum()



    # Análisis de categorías
    if 'Descripcion' in df_filtered.columns:
        st.subheader("Análisis de Categorías")
        Descripcions_mas_vendidas = df_filtered.groupby('Descripcion')['Cantidad'].sum().nlargest(3)
        st.write("Top 3 Descripciones más vendidas:")
        st.table(Descripcions_mas_vendidas)
    else:
        st.warning("No se encontró la columna 'Descripcion' en los datos filtrados.")


    # Análisis geográfico
    st.subheader("Análisis Geográfico")
    paises_mas_ventas = df_filtered.groupby('Pais')['Total'].sum().nlargest(5)
    st.write("Ventas totales (Top 5 países con mejores ventas):")
    st.table(paises_mas_ventas)


    st.header("Métricas")

    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Total de Ventas en todos los países", value=f"${total_ventas:,.2f}")
    
    with col2:
        st.metric(label="Total de productos Vendidos en todos los países", value=total_cantidad)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Número de Clientes", value=df_filtered['IdCliente'].nunique())

    with col2:
        st.metric(label="Ventas Promedio por Cliente", value=f"${total_ventas / df_filtered['IdCliente'].nunique():,.2f}")

