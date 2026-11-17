import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", page_title="Dashboard del Clima con Predicción")
st.title("🌤️ Dashboard del Clima con Predicciones")

CSV_PATH = "weather_data.csv"

try:
    df = pd.read_csv(CSV_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601", errors="coerce")  # ✅ ISO8601 robusto
except Exception as e:
    st.error(f"No se pudo cargar el archivo CSV: {e}")
    st.stop()

if df.empty:
    st.warning("El archivo está vacío. Esperando datos...")
    st.stop()

# Asegurar que las columnas esperadas existen
expected_cols = {"timestamp", "temperature", "dew_point", "humidity", "wind_speed", "pressure", "uv_index", "pred_temp_plus_1h", "pred_temp_plus_3h"}
if not expected_cols.issubset(set(df.columns)):
    st.error("Faltan columnas necesarias en el archivo CSV.")
    st.stop()

# Eliminar fechas inválidas
df = df.dropna(subset=["timestamp"])
df.sort_values("timestamp", inplace=True)
df.drop_duplicates("timestamp", inplace=True)

# Sidebar filtros
min_date = df["timestamp"].min()
max_date = df["timestamp"].max()

if min_date == max_date:
    st.sidebar.warning("No hay suficiente rango de fechas para aplicar el filtro.")
    df_filtered = df
else:
    date_range = st.sidebar.slider("🗓️ Rango de fechas", min_value=min_date.to_pydatetime(), max_value=max_date.to_pydatetime(),
                                   value=(min_date.to_pydatetime(), max_date.to_pydatetime()))
    df_filtered = df[(df["timestamp"] >= date_range[0]) & (df["timestamp"] <= date_range[1])]

# Gráficos principales
st.subheader("🌡️ Temperatura actual y predicciones (+1h y +3h)")
fig1, ax1 = plt.subplots(figsize=(15, 5))
sns.lineplot(data=df_filtered, x="timestamp", y="temperature", label="Temperatura actual (°F)", ax=ax1)
sns.lineplot(data=df_filtered, x="timestamp", y="pred_temp_plus_1h", label="Predicción +1h", ax=ax1)
sns.lineplot(data=df_filtered, x="timestamp", y="pred_temp_plus_3h", label="Predicción +3h", ax=ax1)
ax1.set_ylabel("°F")
ax1.legend()
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("💧 Punto de rocío, Humedad, Presión y UV")
fig2, ax2 = plt.subplots(figsize=(15, 5))
sns.lineplot(data=df_filtered, x="timestamp", y="dew_point", label="Punto de Rocío", ax=ax2)
sns.lineplot(data=df_filtered, x="timestamp", y="humidity", label="Humedad (%)", ax=ax2)
sns.lineplot(data=df_filtered, x="timestamp", y="pressure", label="Presión (inHg)", ax=ax2)
sns.lineplot(data=df_filtered, x="timestamp", y="uv_index", label="Índice UV", ax=ax2)
ax2.legend()
plt.xticks(rotation=45)
st.pyplot(fig2)

st.subheader("📊 Tabla de datos completos")
st.dataframe(df_filtered, use_container_width=True)
