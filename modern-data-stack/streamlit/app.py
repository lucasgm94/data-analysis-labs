import streamlit as st
import duckdb
import pandas as pd
import os
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(
    page_title="Dashboard de Ventas | Modern Data Stack",
    page_icon="📊",
    layout="wide"
)

# --- CABECERA CON TU FIRMA ✍️ ---
st.title("📊 Reporte Ejecutivo de Ventas")
st.markdown("##### **Desarrollado por Lucas Martinez** 🚀")
st.markdown("---")

# 2. Ruta a la base de datos
db_path = os.path.join(os.path.dirname(__file__), '..', 'duckdb', 'local_warehouse.db')

try:
    con = duckdb.connect(db_path)
    df = con.execute("SELECT * FROM reporte_ventas").df()
    df.columns = [c.lower() for c in df.columns]
    
    ventas_col = 'total_ventas' if 'total_ventas' in df.columns else 'ventas'
    unidades_col = 'total_unidades' if 'total_unidades' in df.columns else 'unidades'

    # --- 🛠️ SECCIÓN DE FILTROS (SIDEBAR) ---
    st.sidebar.header("Filtros de Búsqueda 🔍")
    lista_regiones = sorted(df['region'].unique().tolist())
    regiones_seleccionadas = st.sidebar.multiselect(
        "Selecciona una o más regiones 🌍",
        options=lista_regiones,
        default=lista_regiones 
    )

    df_filtrado = df[df['region'].isin(regiones_seleccionadas)]

    # --- 📈 SECCIÓN DE MÉTRICAS ---
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("📄 Total de Registros", f"{len(df_filtrado)}")
    with col2: st.metric("💰 Ventas Totales", f"$ {df_filtrado[ventas_col].sum():,.0f}")
    with col3: st.metric("📦 Unidades Vendidas", f"{df_filtrado[unidades_col].sum():,}")

    st.markdown("---")

    # --- 📊 SECCIÓN DE GRÁFICOS (BARRAS Y TORTA) ---
    col_barras, col_torta = st.columns(2)

    # Definimos un mapa de colores fijo para que coincidan en ambos gráficos
    # Plotly usará estos colores según el nombre de la región
    color_map = {
        'Buenos Aires': '#00a3ff', 
        'Centro': '#ff4b4b', 
        'Cuyo': '#36d399', 
        'NEA': '#fbbd23', 
        'NOA': '#a991f7', 
        'Patagonia': '#f87272'
    }

    with col_barras:
        st.subheader("📍 Ventas por Región")
        df_region = df_filtrado.groupby('region')[ventas_col].sum().reset_index()
        fig_bar = px.bar(
            df_region, x='region', y=ventas_col, color='region',
            color_discrete_map=color_map, # Aplicamos el mapa de colores
            labels={'region': 'Región', ventas_col: 'Ventas ($)'}
        )
        fig_bar.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_torta:
        st.subheader("🍰 Participación por Región (%)")
        fig_pie = px.pie(
            df_filtrado, values=ventas_col, names='region',
            color='region', color_discrete_map=color_map, # Misma lógica de colores
            hole=0.4 # Estilo "Donut" para que sea más moderno
        )
        # Forzamos que muestre el porcentaje y el nombre
        fig_pie.update_traces(textinfo='percent+label')
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- 📑 TABLAS ---
    st.markdown("---")
    t1, t2 = st.columns([1, 2])

    with t1:
        st.subheader("🏆 Top Clientes")
        top_clientes = df_filtrado.sort_values(by=ventas_col, ascending=False).head(10)
        cols_honor = [c for c in ['nombre', 'apellido', ventas_col] if c in df_filtrado.columns]
        st.dataframe(top_clientes[cols_honor], use_container_width=True, hide_index=True)

    with t2:
        st.subheader("📑 Detalle (Orden Unidades ⬇️)")
        df_ordenado = df_filtrado.sort_values(by=unidades_col, ascending=False)
        st.dataframe(df_ordenado, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"❌ Error al cargar los datos.")
    st.warning(f"⚠️ Detalle técnico: {e}")

finally:
    if 'con' in locals(): con.close()