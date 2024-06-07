import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
print("Funcionandoooo")
# reading the data from excel file
df = pd.read_excel("Agencia.xlsx")
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:2.5rem;}</style>', unsafe_allow_html=True)
#image = Image.open('agenciaViaje4.jpg')

#col1, col2 = st.columns([0.2,0.9])
#with col1:
#    st.image( image,width=250)

# Open the image
image = Image.open('agenciaViaje4.jpg')

# CSS to make the image circular
st.markdown(
    """
    <style>
    .circle-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 50%;
        width: 250px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([0.2,0.9])
with col1:
    st.markdown(f'<img src="data:image/png;base64,{st.image(image, use_column_width=True)}" class="circle-img">', unsafe_allow_html=True)
   
              
html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    margin-top: 15px;
    
    }
    </style>
    <center><h1 class="title-test">Agencia De Viajes UrpiTours</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.1,0.45,0.45])

#with col3:
#   box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
#    st.write(f"Last updated by:  \n {box_date}")

with col4:
    fig = px.bar(df, x = "Cliente", y = "VentasTotales", labels={"VentasTotales" : "Ventas Totales {Bs}"},
                 title = "Ventas Totales por Categorias", hover_data=["VentasTotales"],
                 template="gridon",height=500)
    st.plotly_chart(fig,use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Ventas por Categoria")
    data = df[["Cliente","VentasTotales"]].groupby(by="Cliente")["VentasTotales"].sum()
    expander.write(data)
with dwn1:
    st.download_button("Descargar Archivo", data = data.to_csv().encode("utf-8"),
                       file_name="VentasClienteRegion.csv", mime="text/csv")

df["Mes_Año"] = df["FechaFactura"].dt.strftime("%b'%y")
result = df.groupby(by = df["Mes_Año"])["VentasTotales"].sum().reset_index()

with col5:
    fig1 = px.line(result, x = "Mes_Año", y = "VentasTotales", title="Ventas Totales a lo largo del Tiempo",
                   template="gridon")
    st.plotly_chart(fig1,use_container_width=True)

with view2:
    expander = st.expander("Ventas mensuales")
    data = result
    expander.write(data)
with dwn2:
    st.download_button("Descargar Archivo", data = result.to_csv().encode("utf-8"),
                       file_name="Ventas mensuales.csv", mime="text/csv")
    
st.divider()

result1 = df.groupby(by="Destino")[["VentasTotales","UnitsSold"]].sum().reset_index()

# add the units sold as a line chart on a secondary y-axis
fig3 = go.Figure()
fig3.add_trace(go.Bar(x = result1["Destino"], y = result1["VentasTotales"], name = "Total Sales"))
fig3.add_trace(go.Scatter(x=result1["Destino"], y = result1["UnitsSold"], mode = "lines",
                          name ="Units Sold", yaxis="y2"))
fig3.update_layout(
    title = "Total Sales and Units Sold by Destino",
    xaxis = dict(title="Destino"),
    yaxis = dict(title="Total Sales", showgrid = False),
    yaxis2 = dict(title="Units Sold", overlaying = "y", side = "right"),
    template = "gridon",
    legend = dict(x=1,y=1.1)
)
_, col6 = st.columns([0.1,1])
with col6:
    st.plotly_chart(fig3,use_container_width=True)

_, view3, dwn3 = st.columns([0.5,0.45,0.45])
with view3:
    expander = st.expander("Ver datos de ventas por unidades vendidas")
    expander.write(result1)
with dwn3:
    st.download_button("Descargar Archivo", data = result1.to_csv().encode("utf-8"), 
                       file_name = "Sales_by_UnitsSold.csv", mime="text/csv")
st.divider()

_, col7 = st.columns([0.1,1])
treemap = df[["Region","Ciudad","VentasTotales"]].groupby(by = ["Region","Ciudad"])["VentasTotales"].sum().reset_index()

def format_sales(value):
    if value >= 0:
        return '{:.2f} Lakh'.format(value / 1_000_00)

treemap["VentasTotales (Formatted)"] = treemap["VentasTotales"].apply(format_sales)

fig4 = px.treemap(treemap, path = ["Region","Ciudad"], values = "VentasTotales",
                  hover_name = "VentasTotales (Formatted)",
                  hover_data = ["VentasTotales (Formatted)"],
                  color = "Ciudad", height = 700, width = 600)
fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Ventas totales por región y ciudad")
    st.plotly_chart(fig4,use_container_width=True)

_, view4, dwn4 = st.columns([0.5,0.45,0.45])
with view4:
    result2 = df[["Region","Ciudad","VentasTotales"]].groupby(by=["Region","Ciudad"])["VentasTotales"].sum()
    expander = st.expander("Ver datos de Ventas Totales por Región y Ciudad")
    expander.write(result2)
with dwn4:
    st.download_button("Descargar Archivo", data = result2.to_csv().encode("utf-8"),
                                        file_name="Sales_by_Region.csv", mime="text.csv")

_,view5, dwn5 = st.columns([0.5,0.45,0.45])
with view5:
    expander = st.expander("Ver datos sin procesar de ventas")
    expander.write(df)
with dwn5:
    st.download_button("Descargar Archivo", data = df.to_csv().encode("utf-8"),
                       file_name = "SalesRawData.csv", mime="text/csv")
st.divider()