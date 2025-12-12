import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Encuesta Helados", layout="centered")
st.title("🍦 Encuesta de Preferencia")

# Lista de sabores
OPCIONES = [
    "Vaso 1 Litro Vainilla",
    "Vaso 1 Litro Vainilla Chips",
    "Vaso 1 Litro Jet",
    "Vaso Litro Chiks Vainilla x 324g",
    "Vaso 1 Litro Vainilla Fresa"
]

# --- CONEXIÓN A GOOGLE SHEETS ---
# Establecemos la conexión usando los secretos que configuraremos luego
conn = st.connection("gsheets", type=GSheetsConnection)

# Función para obtener datos actualizados
def obtener_datos():
    try:
        # Leemos la hoja (si está vacía, creamos la estructura)
        df = conn.read(worksheet="Hoja 1", usecols=[0, 1], ttl=0)
        # Si el archivo está vacío o no tiene las columnas correctas, lo inicializamos
        if df.empty or "Sabor" not in df.columns:
            df = pd.DataFrame({'Sabor': OPCIONES, 'Votos': 0})
        return df.dropna()
    except:
        # En caso de error (hoja nueva), devolvemos estructura base
        return pd.DataFrame({'Sabor': OPCIONES, 'Votos': 0})

# --- LÓGICA DE VOTACIÓN ---
df = obtener_datos()

st.write("Selecciona tu favorito y los resultados se guardarán en la nube:")

with st.form("voto_form"):
    eleccion = st.radio("Opciones:", OPCIONES)
    boton_enviar = st.form_submit_button("Votar y Guardar")

    if boton_enviar:
        # 1. Buscamos la fila del sabor elegido y sumamos 1
        # Aseguramos que 'Votos' sea numérico para evitar errores
        df['Votos'] = pd.to_numeric(df['Votos'], errors='coerce').fillna(0)
        
        # Incrementamos el voto
        df.loc[df['Sabor'] == eleccion, 'Votos'] += 1
        
        # 2. Escribimos de vuelta en Google Sheets
        conn.update(worksheet="Hoja 1", data=df)
        
        st.success("✅ ¡Voto guardado en Google Sheets correctamente!")
        st.balloons()
        
        # Recargamos los datos para mostrar la gráfica actualizada inmediatamente
        df = obtener_datos()

# --- RESULTADOS ---
st.divider()
st.subheader("📊 Resultados en Vivo")

col1, col2 = st.columns([1, 2])

with col1:
    st.dataframe(df, hide_index=True)
    total = df['Votos'].sum()
    st.metric("Total Votos", int(total))

with col2:
    st.bar_chart(df, x="Sabor", y="Votos", color="#4BFF4B")
