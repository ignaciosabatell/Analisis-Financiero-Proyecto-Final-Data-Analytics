
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt

#Estilo Streamlit

st.markdown("""
<style>

/* ======== MODO CLARO ======== */
@media (prefers-color-scheme: light) {
    .main {
        background: linear-gradient(135deg, #0a2540, #193b63);
    }
    .block-container {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(8px);
        padding: 2.2rem;
        border-radius: 18px;
        color: black;
    }
    h1, h2, h3 {
        color: #000000;
    }
    .stButton>button {
        background-color: #4da3ff;
        color: #0a2540;
        border: none;
        padding: 0.7rem 1.4rem;
        border-radius: 10px;
        font-weight: 700;
    }
    input {
        background-color: #e9f2ff !important;
        border-radius: 6px !important;
        color: #000000 !important;
    }
    .stSelectbox div, .stNumberInput input {
        color: #000 !important;
    }
}

/* ======== MODO OSCURO ======== */
@media (prefers-color-scheme: dark) {
    .main {
        background: linear-gradient(135deg, #0d1a2b, #0f233d);
    }
    .block-container {
        background: rgba(0,0,0,0.35);
        backdrop-filter: blur(10px);
        padding: 2.2rem;
        border-radius: 18px;
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .stButton>button {
        background-color: #4da3ff;
        color: #000000;
        border: none;
        padding: 0.7rem 1.4rem;
        border-radius: 10px;
        font-weight: 700;
    }
    input {
        background-color: #1e2a3a !important;
        color: #ffffff !important;
        border-radius: 6px !important;
    }
    .stSelectbox div, .stNumberInput input {
        color: #ffffff !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Limitar ancho y centrar solo en la página calculadora */
.block-container {
    max-width: 750px;      /* AJUSTA AQUÍ el ancho deseado */
    margin-left: auto;     /* Centrado horizontal */
    margin-right: auto;
}

</style>
""", unsafe_allow_html=True)

#Comienza la calculadora

btc = pd.read_csv("datos limpios/btc_limpio.csv")
oro = pd.read_csv("datos limpios/oro_limpio.csv")
sp500 = pd.read_csv("datos limpios/sp500_limpio.csv")


#Analisis historico


st.markdown("""
<h2 style='text-align:center; color:#001f3f;'>Análisis histórico de inversión mensual
""", unsafe_allow_html=True)

for df in [btc, oro, sp500]:
    df["open_time"] = pd.to_datetime(df["open_time"])

activo = st.selectbox("Elige el activo", ["S&P 500", "Bitcoin", "Oro"], key="activo_dca_fecha")

inversion_mensual = st.number_input("Cantidad a invertir cada mes (€)", value=100, step=10)
fecha_inicio = st.date_input("Fecha de inicio", value=pd.to_datetime("2015-01-01"))
fecha_fin = st.date_input("Fecha de fin", value=pd.to_datetime("2025-01-01"))

if activo == "S&P 500":
    df_activo = sp500
    columna_precio = "high"
elif activo == "Bitcoin":
    df_activo = btc
    columna_precio = "high"
else:
    df_activo = oro
    columna_precio = "high_oz"

df_filtrado = df_activo[(df_activo["open_time"] >= pd.to_datetime(fecha_inicio)) &
                        (df_activo["open_time"] <= pd.to_datetime(fecha_fin))]
df_filtrado = df_filtrado.set_index("open_time")[columna_precio].resample("M").last().ffill()
ultimo_precio = df_filtrado.iloc[-1]

serie_mensual = df_filtrado

valor_acumulado = []
acumulado = 0
for precio in serie_mensual:
    acumulado += inversion_mensual / precio
    valor_acumulado.append(acumulado * precio)

df_dca = pd.DataFrame({
    "Fecha": serie_mensual.index,
    "Valor acumulado": valor_acumulado,
    "Invertido acumulado": [inversion_mensual*(i+1) for i in range(len(serie_mensual))]
})

fig = px.line(
    df_dca,
    x="Fecha",
    y=["Valor acumulado", "Invertido acumulado"],
    title=f"Simulación DCA: {inversion_mensual} €/mes en {activo}",
    labels={"value": "Euros", "variable": "Serie"},
    color_discrete_map={"Valor acumulado": "green", "Invertido acumulado": "blue"}
)
fig.update_layout(template="plotly_white", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

total_invertido = df_dca["Invertido acumulado"].iloc[-1]
valor_final = df_dca["Valor acumulado"].iloc[-1]
ganancia = valor_final - total_invertido

st.write(f"**Total invertido:** {total_invertido:,.2f} €")
st.write(f"**Valor final de la inversión:** {valor_final:,.2f} €")
st.write(f"**Ganancia/Pérdida:** {ganancia:,.2f} €")

st.markdown("--------------------------")

#calculadora

for df in [btc, oro, sp500]:
    df["open_time"] = pd.to_datetime(df["open_time"])

st.markdown("""
<h2 style='text-align:center; color:#0d47a1;'>Calculadora de inversión
""", unsafe_allow_html=True)

activo = st.selectbox("Elige el activo", ["S&P 500", "Bitcoin", "Oro"], key="activo_inversion")


deposito_inicial = st.number_input("Depósito inicial (€)", value=0, step=100, key="deposito_inicial")
inversion_mensual = st.number_input("Cantidad a invertir cada mes (€)", value=100, step=10, key="inversion_mensual")
años_inversion = st.number_input("Periodo de inversión (años)", value=5, step=1, key="periodo_anios")

# Rendimiento anual esperado 
if activo == "S&P 500":
    rendimiento_por_defecto = 9.71
elif activo == "Oro":
    rendimiento_por_defecto = 11.64
else:  
    rendimiento_por_defecto = 7.0

rendimiento_anual = st.number_input(
    f"Rendimiento anual esperado para {activo} (%)",
    value=rendimiento_por_defecto,
    step=0.1,
    key="rendimiento_anual"
)

st.markdown(f"Rendimiento anual utilizado: {rendimiento_anual}%")


if activo == "S&P 500":
    df_activo = sp500
    columna_precio = "high"
elif activo == "Bitcoin":
    df_activo = btc
    columna_precio = "high"
else:
    df_activo = oro
    columna_precio = "high_oz"


df_filtrado = df_activo.set_index("open_time")[columna_precio].resample("M").last().ffill()
ultimo_precio = df_filtrado.iloc[-1]


total_meses = años_inversion * 12
rendimiento_mensual = (1 + rendimiento_anual/100)**(1/12) - 1

fecha_inicio_futura = pd.to_datetime("2026-01-01")
meses_futuros = pd.date_range(fecha_inicio_futura, periods=total_meses, freq="M")

precios_futuros = [ultimo_precio * (1 + rendimiento_mensual)**i for i in range(1, total_meses+1)]
serie_mensual = pd.Series(precios_futuros, index=meses_futuros)

valor_acumulado = []
acumulado = deposito_inicial / serie_mensual.iloc[0]  

for precio in serie_mensual:
    acumulado += inversion_mensual / precio
    valor_acumulado.append(acumulado * precio)

df_dca = pd.DataFrame({
    "Fecha": serie_mensual.index,
    "Valor acumulado": valor_acumulado,
    "Invertido acumulado": [deposito_inicial + inversion_mensual*(i+1) for i in range(len(serie_mensual))]
})


fig = px.line(
    df_dca,
    x="Fecha",
    y=["Valor acumulado", "Invertido acumulado"],
    title=f"Simulación inversión: depósito inicial + {inversion_mensual} €/mes en {activo}",
    labels={"value": "Euros", "variable": "Serie"}
)
fig.update_layout(
    legend_title_text="",
    hovermode="x unified",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)


total_invertido = df_dca["Invertido acumulado"].iloc[-1]
valor_final = df_dca["Valor acumulado"].iloc[-1]
ganancia = valor_final - total_invertido

st.write(f"Total invertido: {total_invertido:.2f} €")
st.write(f"Valor final de la inversión: {valor_final:.2f} €")
st.write(f"Ganancia/pérdida: {ganancia:.2f} €")


st.markdown(f"### EN {años_inversion} AÑOS TENDRÁS UN CAPITAL FINAL DE {valor_final:,.2f} €")
st.markdown("**Rentabilidades pasadas no aseguran rentabilidades futuras*")
