import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
st.set_page_config(layout="wide")

#Estilo visual Streamlit
st.markdown("""
<style>

/* =======================================================
   MODO CLARO 
======================================================= */
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
    h1, h2, h3, h4 {
        color: #000000 !important;
    }
    [data-testid="stMetric"] * {
        color: #000000 !important;
    }
    div[data-baseweb="select"] * {
        color: #000000 !important;
    }
    ul[role="listbox"] {
        background: white !important;
        color: black !important;
    }
}

/* =======================================================
   MODO OSCURO 
======================================================= */
@media (prefers-color-scheme: dark) {
    .main {
        background: linear-gradient(135deg, #020b18, #0c1626);
    }
    .block-container {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(12px);
        padding: 2.2rem;
        border-radius: 18px;
        color: #e5e5e5;
    }

    h1, h2, h3, h4 {
        color: #ffffff !important;
    }

    /* Texto general */
    span, p, label, div, .stMarkdown {
        color: #e5e5e5 !important;
    }

    /* Inputs */
    input {
        background-color: #1d2a39 !important;
        color: white !important;
        border-radius: 6px !important;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: #1d2a39 !important;
        color: #ffffff !important;
    }
    div[data-baseweb="select"] svg {
        fill: #ffffff !important;
    }
    ul[role="listbox"] {
        background-color: #1d2a39 !important;
        color: #ffffff !important;
    }

    /* Métricas */
    [data-testid="stMetric"] * {
        color: #ffffff !important;
    }

    /* Botón */
    .stButton>button {
        background-color: #4da3ff;
        color: #001322;
    }
}

</style>
""", unsafe_allow_html=True)


#Comienza el análisis

st.image("imagenes/1.png", use_container_width=True)
st.image("imagenes/2.png", use_container_width=True)

btc=pd.read_csv("datos limpios/btc_limpio.csv")
oro=pd.read_csv("datos limpios/oro_limpio.csv")
sp500 = pd.read_csv("datos limpios/sp500_limpio.csv")
letras= pd.read_csv("datos limpios/letras_limpias.csv")

for df in [sp500, btc, oro]:
    df["open_time"] = pd.to_datetime(df["open_time"])

st.markdown("""
<h1 style='text-align:center;'>Análisis económico de diferentes activos de inversión</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h2 style='text-align:center; color: #2F4F4F;'>Necesitamos al menos un 2.21% de beneficio para proteger nuestro dinero de la inflación</h2>
""", unsafe_allow_html=True)

ipc = pd.read_excel("datos originales/IPC.xlsx", skiprows=1) 
ipc = ipc[["Periodo", "Total"]]
ipc["Total"] = ipc["Total"].astype(float)
ipc["Periodo"] = pd.to_datetime(ipc["Periodo"], format="%YM%m")

fig = px.line(
    ipc,
    x="Periodo",
    y="Total",
    markers=True,
    title="Evolución del IPC en base 2021",
    labels={"Total": "IPC Total", "Periodo": "Periodo"}
)

fig.update_layout(
    xaxis_title="Periodo",
    yaxis_title="IPC Total",
    hovermode="x unified",
    template="plotly_white",
    width=1900,  
    height=500  
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("El incremento medio anual ha sido un 2.21%")

# Dashboard Tableau Comparacion activos

import streamlit.components.v1 as components

st.markdown("""
<h2 style='text-align:center; color:#2F4F4F;'>Comparación de activos
""", unsafe_allow_html=True)

tableau_url = "https://public.tableau.com/views/TableauActivos/Dashboard3?publish=yes"

html_code = f"""
<div class='tableauPlaceholder' style='width:100%; height:800px;'>
    <object class='tableauViz' width='100%' height='800' style='display:none;'>
        <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
        <param name='embed_code_version' value='3' />
        <param name='site_root' value='' />
        <param name='name' value='TableauActivos/Dashboard3' />
        <param name='tabs' value='no' />
        <param name='toolbar' value='yes' />
        <param name='showAppBanner' value='false' />
    </object>
</div>
<script type='text/javascript' src='https://public.tableau.com/javascripts/api/viz_v1.js'></script>
"""

components.html(html_code, height=800)

# COMPARATIVA HISTORICA DATOS NORMALIZADOS

st.markdown("""
<h2 style='text-align:center; color:#2F4F4F;'>Comparación de activos vs IPC</h2>
""", unsafe_allow_html=True)
btc_norm = btc["high"].astype(float) / float(btc["high"].iloc[0])
sp500_norm = sp500["high"].astype(float) / float(sp500["high"].iloc[0])
oro_norm = oro["high_oz"].astype(float) / float(oro["high_oz"].iloc[0])
letras_norm = letras["interes_medio"].astype(float) / float(letras["interes_medio"].iloc[0])
ipc_norm = ipc["Total"].astype(float) / float(ipc["Total"].iloc[0])

df_plot = pd.DataFrame({
    "Fecha BTC": btc["open_time"],
    "Bitcoin": btc_norm,
    "Fecha SP500": sp500["open_time"],
    "SP500": sp500_norm,
    "Fecha Oro": oro["open_time"],
    "Oro": oro_norm,
    "Fecha Letras": letras["fecha_vencimiento"],
    "Letras": letras_norm,
    "Fecha IPC": ipc["Periodo"],
    "IPC": ipc_norm
})

fig = px.line()
fig.add_scatter(x=btc["open_time"], y=btc_norm, mode='lines', name='Bitcoin', line=dict(width=1))
fig.add_scatter(x=sp500["open_time"], y=sp500_norm, mode='lines', name='SP500', line=dict(width=1))
fig.add_scatter(x=oro["open_time"], y=oro_norm, mode='lines', name='Oro', line=dict(width=1))
fig.add_scatter(x=letras["fecha_vencimiento"], y=letras_norm, mode='lines', name='Letras del Tesoro', line=dict(width=1))
fig.add_scatter(x=ipc["Periodo"], y=ipc_norm, mode='lines', name='IPC', line=dict(width=2, dash='dash', color='black'))

fig.update_layout(
    title="Comparativa histórica: BTC, SP500, Oro, Letras del Tesoro vs IPC (normalizado)",
    xaxis_title="Fecha",
    yaxis_title="Valor normalizado (inicio = 1)",
    hovermode="x unified",
    template="plotly_white",
    width=1200,
    height=600
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("--------------------------")

#Rentabilidad

st.markdown("""
<h2 style='text-align:center; color:#2F4F4F;'>Rendimiento anual histórico
""", unsafe_allow_html=True)

sp500 = pd.read_csv("datos limpios/sp500_limpio.csv")
btc = pd.read_csv("datos limpios/btc_limpio.csv")
oro = pd.read_csv("datos limpios/oro_limpio.csv")

for df in [sp500, btc, oro]:
    df["open_time"] = pd.to_datetime(df["open_time"])
    df.sort_values("open_time", inplace=True)
    df.set_index("open_time", inplace=True)

def rendimiento_anual(df, precio_col):
    precios_mensuales = df[precio_col].resample("ME").last()
    retornos = precios_mensuales.pct_change(fill_method=None).dropna()
    retorno_medio_mensual = retornos.mean()
    retorno_anual = (1 + retorno_medio_mensual)**12 - 1
    return retorno_anual

rendimiento_sp500 = rendimiento_anual(sp500, precio_col="high")
rendimiento_oro = rendimiento_anual(oro, precio_col="high_oz")
rendimiento_btc = rendimiento_anual(btc, precio_col="high")

col1, col2, col3,col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style='display:flex; flex-direction:column; gap:2px;'>
        <div style='background:#f7931a; color:black; padding:2px 6px; border-radius:5px; display:inline-block; font-weight:bold; font-size:14px;'>
            🔶 Bitcoin
        </div>
        <div style='font-size:30px; font-weight:600; margin-top:0px;'>{rendimiento_btc:.2%}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='display:flex; flex-direction:column; gap:2px; align-items:flex-start;'>
        <div style='background:#FFD700; color:black; padding:2px 6px; border-radius:5px; font-weight:bold; font-size:14px;'>
            🟡 Oro
        </div>
        <div style='font-size:28px; font-weight:600; margin-top:0px;'>{rendimiento_oro:.2%}</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("El oro no genera dividendos ni flujos de caja. Su rendimiento total es igual a su rendimiento por precio.")

TASA_DIVIDENDOS = 0.025

with col3:
    st.markdown(f"""
    <div style='display:flex; flex-direction:column; gap:2px; align-items:flex-start;'>
        <div style='background:#4CAF50; color:black; padding:2px 6px; border-radius:5px; font-weight:bold; font-size:14px;'>
            📊 S&P 500
        </div>
        <div style='font-size:28px; font-weight:600; margin-top:0px;'>{(rendimiento_sp500 + TASA_DIVIDENDOS):.2%}</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("*(Incluye +2.5% estimado por dividendos reinvertidos)*\nEl Oro y Bitcoin no requieren este ajuste porque no generan dividendos.")

letras_ret= letras["interes_medio"].mean()

with col4:
    st.markdown(f"""
    <div style='display:flex; flex-direction:column; gap:4px;'>
        <div style='background:#fff3d2; padding:4px 8px; border-radius:6px; font-weight:bold; font-size:16px; color:black;'>
            🏦 Letras del Tesoro
        </div>
        <div style='font-size:28px; font-weight:600; margin-top:0px;'>{letras_ret :.2%}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("--------------------------")


#Volatilidad

btc["ret"] = btc["close"].pct_change()
sp500["ret"] = sp500["close"].pct_change()
oro["ret"] = oro["close_oz"].pct_change()
letras["ret"] = letras["interes_medio"].diff()

vol_diaria_btc = btc["ret"].std()
vol_diaria_sp500 = sp500["ret"].std()
vol_diaria_oro = oro["ret"].std()
vol_diaria_letras = letras["ret"].std()

vol_anual_btc = vol_diaria_btc * (365 ** 0.5)      # BTC diario
vol_anual_oro = vol_diaria_oro * (365 ** 0.5)      # Oro diario
vol_anual_sp500 = vol_diaria_sp500 * (252 ** 0.5)  # SP500 252 días hábiles
vol_anual_letras = vol_diaria_letras * (365 ** 0.5) # Letras diario

st.markdown("""
<h2 style='text-align:center; color:#2F4F4F;'>Volatilidad de los activos
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Bitcoin (BTC)", value=f"{vol_anual_btc:.2%}", delta=f"Diaria: {vol_diaria_btc:.2%}")
with col2:
    st.metric(label="Oro (XAU)", value=f"{vol_anual_oro:.2%}", delta=f"Diaria: {vol_diaria_oro:.2%}")
with col3:
    st.metric(label="S&P 500", value=f"{vol_anual_sp500:.2%}", delta=f"Diaria: {vol_diaria_sp500:.2%}")
with col4:
    st.metric(label="Letras del Tesoro", value=f"{vol_anual_letras:.2%}", delta=f"Diaria: {vol_diaria_letras:.2%}")

st.markdown("--------------------------")

#Ratio de SHARPE
btc['ret'] = btc['high'].pct_change()
sp500['ret'] = sp500['high'].pct_change()
oro['ret'] = oro['high_oz'].pct_change()
letras['ret'] = letras['interes_medio'].diff()

rf = 0  

sharpe_btc = ((btc['ret'].mean() - rf) / btc['ret'].std()) * (365**0.5)   # Crypto opera diario
sharpe_sp500 = ((sp500['ret'].mean() - rf) / sp500['ret'].std()) * (252**0.5)
sharpe_oro = ((oro['ret'].mean() - rf) / oro['ret'].std()) * (252**0.5)
sharpe_letras = ((letras['ret'].mean() - rf) / letras['ret'].std()) * (365**0.5)  # Diario → anualizado


st.markdown("""
<h2 style='text-align:center; color:#2F4F4F;'>Ratio Sharpe
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; font-size:16px; color:#000000;'>El ratio de Sharpe es un indicador que mide la rentabilidad ajustada al riesgo de una inversión.  En otras palabras, te dice cuánto rendimiento obtienes por cada unidad de riesgo que asumes.
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; font-size:16px; color:#2F4F4F;'>
Sharpe = (Rendimiento del activo - Tasa libre de riesgo) / Volatilidad del activo
</p>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Bitcoin (BTC)", f"{sharpe_btc:.2f}")
col2.metric("Oro (XAU)", f"{sharpe_oro:.2f}")
col3.metric("S&P 500", f"{sharpe_sp500:.2f}")
col4.metric("Letras del Tesoro", f"{sharpe_letras:.2f}")

st.markdown(""" Sharpe BTC ≈ 2.34 → **Bitcoin** ha tenido **mucha volatilidad**, pero sus retornos han sido altos comparados con su riesgo.

 Sharpe SP500 ≈ 1.18 → **El S&P 500** es **más estable** que BTC, pero también ofrece retornos más moderados respecto a su riesgo.

 Sharpe Oro ≈ 3.36 → **El oro** ha sido **muy estable** en comparación con sus retornos, por eso el ratio es alto; poca volatilidad relativa.

Sharpe Letras ≈ 0.31 → Baja volatilidad y retornos bajos, **ratio pequeño pero positivo** """)


st.markdown("--------------------------")


st.markdown("""
<h2 style='text-align:center; color:#2F4F4F;'>¿Cuál es la mejor solución ante la inflación?
""", unsafe_allow_html=True)
st.markdown(
    "#### Analizando la Volatilidad y la tendencia de todos los activos:\n\n")
st.markdown(
    """
    <p style='font-size:18px;'>
    El estudio recomienda invertir un % de tus ganancias a partes iguales entre <b>SP500</b> y <b>Oro</b>, 
    reservando una parte al <b>BTC</b> si lo deseamos. Su gran volatilidad no permite tomar conclusiones tan precisas como los otros activos.
    </p>
    """, unsafe_allow_html=True
)



st.markdown("--------------------------")

st.markdown("""
<h2 style='text-align:center; color:#2F4F4F;'>¿Cómo invertir?
""", unsafe_allow_html=True)

st.markdown(
    """
    <p style='font-size:18px;'>
    Para protegernos de las subidas y bajadas del mercado, se recomienda realizar aportaciones de forma 
    <b>semanal o mensual</b>. De esta manera, se va construyendo una media ponderada de precios y 
    podemos aumentar nuestra cartera con el tiempo, reduciendo el riesgo de invertir todo de golpe en un momento desfavorable.
    </p>
    """, unsafe_allow_html=True
)


st.markdown("--------------------------")

st.markdown("""
<h2 style='text-align:center; color:#2F4F4F;'>Plataformas recomendadas:
""", unsafe_allow_html=True)
st.markdown("")
cols = st.columns(4)

with cols[0]:
   
    st.image("https://forbes.es/wp-content/uploads/2023/09/fotonoticia_20230918181846_9999.jpg", width=150)
    st.markdown("""
    - Compra y venta de ETFs y acciones.
    - Muy fácil de usar, ideal para principiantes.
    - Inversiones periódicas y planes automáticos.
    """)

with cols[1]:
    
    st.image("https://myinvestor.es/images/logo-myinvestor.svg", width=150)
    st.markdown("""
    - Broker/banco español regulado.
    - Acceso a acciones, ETFs, fondos indexados y pensiones.
    - Buenas condiciones para inversión pasiva y bajas comisiones.
    [Web oficial](https://myinvestor.es)
    """)

with cols[2]:
   
    st.image("https://freedom24.com/layout/img/logo/logo-f24.light.svg", width=150)
    st.markdown("""
    - Acceso a mercados globales, acciones internacionales y ETFs.
    - Opción interesante para diversificación global.
    [Web oficial](https://freedom24.com)
    """)

with cols[3]:
    
    st.image("https://1000logos.net/wp-content/uploads/2022/08/Revolut-Logo.png", width=150)
    st.markdown("""
    - Muy fácil de usar, ideal para principiantes.
    - Permite inversiones fraccionadas o pequeñas cantidades.
    - Útil si ya usas la app para finanzas personales.
    [Web oficial](https://www.revolut.com)
    """)
