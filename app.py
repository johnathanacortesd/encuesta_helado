import streamlit as st
import pandas as pd
import os

# 1. Configuración de la página
st.set_page_config(page_title="Encuesta de Helados", layout="centered")

# 2. Definir los sabores (La lista limpia)
OPCIONES = [
    "Vaso 1 Litro Vainilla",
    "Vaso 1 Litro Vainilla Chips",
    "Vaso 1 Litro Jet",
    "Vaso Litro Chiks Vainilla x 324g",
    "Vaso 1 Litro Vainilla Fresa"
]

# 3. Función para manejar el archivo de datos (Persistencia)
ARCHIVO_DATOS = 'resultados_encuesta.csv'

def cargar_datos():
    if not os.path.exists(ARCHIVO_DATOS):
        # Si no existe, creamos un DataFrame vacío con las opciones en 0
        df = pd.DataFrame({'Sabor': OPCIONES, 'Votos': 0})
        df.to_csv(ARCHIVO_DATOS, index=False)
        return df
    return pd.read_csv(ARCHIVO_DATOS)

def guardar_voto(opcion_elegida):
    df = pd.read_csv(ARCHIVO_DATOS)
    # Sumar 1 al sabor elegido
    df.loc[df['Sabor'] == opcion_elegida, 'Votos'] += 1
    df.to_csv(ARCHIVO_DATOS, index=False)
    return df

# --- INTERFAZ DE USUARIO ---

st.title("🍦 Encuesta de Preferencia")
st.write("Selecciona tu presentación favorita de 1 Litro:")

# Formulario de votación
with st.form("voto_form"):
    eleccion = st.radio("Opciones:", OPCIONES)
    boton_enviar = st.form_submit_button("Votar")

    if boton_enviar:
        guardar_voto(eleccion)
        st.success(f"¡Gracias! Has votado por: **{eleccion}**")
        st.balloons()

# --- RESULTADOS EN TIEMPO REAL ---
st.divider()
st.subheader("📊 Resultados actuales")

# Cargar datos actualizados
df_resultados = cargar_datos()

# Mostrar métricas y gráfica
col1, col2 = st.columns([1, 2])

with col1:
    # Mostrar tabla simple
    st.dataframe(df_resultados, hide_index=True)
    total_votos = df_resultados['Votos'].sum()
    st.metric("Total de Votos", total_votos)

with col2:
    # Mostrar gráfico de barras
    st.bar_chart(df_resultados, x="Sabor", y="Votos", color="#FF4B4B")
