import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np

#Aquí va la parte lógica previa al Dashbaord
df= pd.read_csv("Datos_Limpios2.csv", encoding="latin-1")
df["Edad Victima"].replace({0:-1},inplace=True)
df["Edad Agresor"].replace({0:-1},inplace=True)

df_ViolenciaExpandido=pd.DataFrame()
for i in df.columns[-10:]:
  df_temp=df[df[i]==1].iloc[:,2:-11]
  df_temp["Tipo Violencia"]=i
  df_ViolenciaExpandido= pd.concat([df_ViolenciaExpandido, df_temp])

figViolencia= px.bar(x= df.sum().index[-9:], y=df.sum()[-9:],text_auto=True, color=df.sum()[-9:].astype(int),
                     color_continuous_scale=px.colors.sequential.Bluered,
                     labels={"x":"Tipo de Violencia", "y":"Cantidad", "color":"Cantidad"})
figViolencia.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"},
                            font_color="white",showlegend=False)

app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO])

############        PRE-DISEÑO  ############  

tabTiempo_content = dbc.Container([

    html.Br(),

    dbc.Row([
        dbc.Col(

            [html.H2("Elección de Periodo"),

            html.Br(),
                
            dcc.RangeSlider(id='slider_anios',
                            min=df["Año"].min(), max=df["Año"].max(), step=1, 
                            value=[df["Año"].min(), df["Año"].max()],
                            marks={i: '{}'.format(i) for i in range(df["Año"].min(), df["Año"].max()+1)}), 

            
            ],
            
            width=3
        ),

        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H1(1, id="CardTiempo1"),
                html.P("Año con más víctimas Fem")]
            ), color="#ff69b4")) ,

        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H1(1, id="CardTiempo2"),
                html.P("Año con más víctimas Mas")]
            ), color="#000080")),

        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H1(1, id="CardTiempo3"),
                html.P("Casos en Total del periodo")]
            ), color="info")),

        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H1(1, id="CardTiempo4"),
                html.P("Casos en Promedio por Año")]
            ), color="info")),

        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H1(1, id="CardTiempo5"),
                html.P("Año con más agresores Mas")]
            ), color="#000080")),

        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H1(1, id="CardTiempo6"),
                html.P("Año con más agresoras Fem")]
            ), color="#ff69b4"))

        

        
    ]),

    html.Hr(),

    dbc.Row([

        dbc.Col([html.H3("Casos por Año y por Sexo de la Victima"),dcc.Graph(id='SunBurstTiempo_SexoV')], width=4),

        dbc.Col([html.H3("Casos por Año"),dcc.Graph(id='LinearTiempo')], width=4),

        dbc.Col([html.H3("Casos por Año y por Sexo del Agresor"),dcc.Graph(id='SunBurstTiempo_SexoA')], width=4)

            ])
], fluid=True)


tabEdad_content = dbc.Container([

    html.Br(),

    dbc.Col([

        dbc.Row([
            dbc.Col([
                html.H3("Rango Edad Víctima"),

                dcc.RangeSlider(0, df["Edad Victima"].max(), value=[0, 18], 
                                id="slider-edadVictima",  tooltip={"placement": "bottom", "always_visible": True}),

                html.Br(),

                dbc.Row([
                    dbc.Col(html.H4("Años por grupo de edad"), width=10),

                    dbc.Col(dcc.Input(id="Años_Victima_Bins",type="number",value=3, style={'width':'40px'}), width=2)

                    
                ])
            ], width=3),

            dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H2(1, id="CardEdad1"),
                html.P("Grupo de edad con más Víctimas")]
            ), color="info")),

            dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H5(1, id="CardEdad2")]
            ), color="warning")),

            dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H2(1, id="CardEdad3"),
                html.P("Grupo de edad con más Agresores")]
            ), color="info")),

            dbc.Col([
                html.H3("Rango Edad Agresor"),

                dcc.RangeSlider(0, df["Edad Agresor"].max(), value=[0, 60], 
                                id="slider-edadAgresor",  tooltip={"placement": "bottom", "always_visible": True}),

                html.Br(),

                dbc.Row([
                    dbc.Col(html.H4("Años por grupo de edad"), width=10),

                    dbc.Col(dcc.Input(id="Años_Agresor_Bins",type="number",value=5, style={'width':'40px'}), width=2)

                    
                ])
            ], width=3),

        ]),

        html.Hr(),

        dbc.Row([
            dbc.Col([
                html.H3("Distribución de edad de Víctimas"),
                dcc.Graph(id='Hist_EdadVictima')
        ], width=4),

        dbc.Col([
                html.H3("Relación edad Víctimas y Agresores"),
                dcc.Graph(id='Heatmap_Edad')
        ], width=4),

        dbc.Col([
                html.H3("Distribución de edad de Agresores"),
                dcc.Graph(id='Hist_EdadAgresor')
        ], width=4)
        ])

        
    ])
], fluid=True)

tabSexo_content = dbc.Container([

    dbc.Col([

        html.Br(),

        dbc.Row([
            dbc.Col([
                html.H4("Elegir sexo"),
                dbc.RadioItems(
                    id="Radio_Victima_Agresor",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=[
                        {"label": "Vícitima", "value": "Victima"},
                        {"label": "Agresor", "value": "Agresor"}
                    ],
                    value="Victima",inline=False
                )
            ], width=2),

            dbc.Col(dbc.Card(dbc.CardBody(html.H6(1, id="CardSexo1")), color="#000080"), width=2),

            dbc.Col(dbc.Card(dbc.CardBody(html.H6(1, id="CardSexo2")), color="#ff69b4"), width=2),

            dbc.Col(dbc.Card(dbc.CardBody(html.H6(1, id="CardSexo3")), color="info"), width=2),

            dbc.Col(dbc.Card(dbc.CardBody(html.H6(1, id="CardSexo4")), color="#ff69b4"), width=2),

            dbc.Col(dbc.Card(dbc.CardBody(html.H6(1, id="CardSexo5")), color="#000080"), width=2)
        ]),

        html.Hr(),

        dbc.Row([

            dbc.Col([
                html.H4("Proporción Sexo - Parentesco Agresor"),
                dcc.Graph(id='SexoParentesco')
            ], width=4),

            dbc.Col([
                html.H4("Proporción Sexo"),
                dcc.Graph(id="PieSexo")
            ], width=4),

            dbc.Col([
                html.H4("Proporción Sexo - Edo. Civil"),
                dcc.Graph(id='SexoEdoCivil')
            ], width=4)

            
        ])
    ])

],fluid=True)

tabViolencia_content = dbc.Container([
    dbc.Col([

        html.Br(),

        dbc.Row([

            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        html.H6("1", id="CardViolencia1")
                    ), color="#000080"
                )
            ], width=2),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        html.H6("1", id="CardViolencia2")
                    ), color="#ff69b4"
                )
            ], width=2),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        html.H6("El tipo de violencia más frecuente es "+
                        df_ViolenciaExpandido["Tipo Violencia"].value_counts().index[0], 
                        id="CardViolencia3")
                    ), color="danger"
                )
            ], width=2),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        html.H6("El tipo de violencia menos frecuente es "+
                        df_ViolenciaExpandido["Tipo Violencia"].value_counts().index[-1], 
                        id="CardViolencia4")
                    ), color="info"
                )
            ], width=2),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        html.H6("1", id="CardViolencia5")
                    ), color="danger"
                )
            ], width=2),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        html.H6("1", id="CardViolencia6")
                    ), color="info"
                )
            ], width=2)

        ]),

        html.Hr(),

        dbc.Row([
            dbc.Col([
                html.H3("Tipo de Violencia por Sexo"),
                dbc.RadioItems(
                    id="Radio_Victima_Agresor2",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=[
                        {"label": "Vícitima", "value": "Victima"},
                        {"label": "Agresor", "value": "Agresor"}
                    ],
                    value="Victima",inline=False
                ),
                dcc.Graph(id="Violencia1")
                
            ],width=4),

            dbc.Col([
                html.H3("Tipos de Violencia más comunes"),
                dcc.Graph(figure=figViolencia)
            ], width=4),

            dbc.Col([
                html.H3("Tipo de Violencia por Otras Variables"),
                dbc.RadioItems(
                    id="Radio_Otros",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=[
                        {"label": "Parentesco", "value": "Parentesco"},
                        {"label": "Estado Civil", "value": "Estado Civil"}
                    ],
                    value="Parentesco",inline=False
                ),
                dcc.Graph(id="Violencia3")

            ], width=4)
        ])
    ])
],fluid=True)

tabs = dbc.Tabs(
    [
        dbc.Tab(tabTiempo_content, label="Análisis de Tiempo"),
        dbc.Tab(tabEdad_content, label="Análisis de Edad"),
        dbc.Tab(tabSexo_content, label="Análisis de Sexo"),
        dbc.Tab(tabViolencia_content, label="Análisis de Violencia")
    ]
)




############        DISEÑO      ############  
app.layout = dbc.Container(
    #Aquí va el diseño del Dashboard
    [html.Br(),
    tabs], fluid=True
)

@app.callback(Output('LinearTiempo', 'figure'),
              [Input('slider_anios', 'value')])
def update_figure(selected_year):
    df_temp= df[(df["Año"]>=selected_year[0]) &(df["Año"]<=selected_year[1])]
    df_temp=df_temp.groupby("Año").count().reset_index()
    df_temp["Año"]=df_temp["Año"].astype(str)
    fig=px.bar(df_temp, x="Año", y="Caja", labels={"Caja":"Casos"}, color="Caja",
    color_continuous_scale=px.colors.sequential.Bluered)
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"},
                        font_color="white",showlegend=False)
    return(fig)

@app.callback(Output('SunBurstTiempo_SexoV', 'figure'),
              [Input('slider_anios', 'value')])
def update_figure(selected_year):
    df_temp= df[(df["Año"]>=selected_year[0]) &(df["Año"]<=selected_year[1])]
    df_temp["Año"]=df_temp["Año"].astype(str)
    fig= px.sunburst(df_temp, path=["Sexo Victima","Año"], color="Sexo Victima",
                     color_discrete_map={"MASCULINO":"navy",
                                         "FEMENINO":"hotpink",
                                         "S/R":"black"})
    fig.update_traces(textinfo="label+percent parent")
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"},
                        font_color="white",showlegend=False)
    return(fig)

@app.callback(Output('SunBurstTiempo_SexoA', 'figure'),
              [Input('slider_anios', 'value')])
def update_figure(selected_year):
    df_temp= df[(df["Año"]>=selected_year[0]) &(df["Año"]<=selected_year[1])]
    df_temp["Año"]=df_temp["Año"].astype(str)
    fig= px.sunburst(df_temp, path=["Sexo Agresor","Año"], color="Sexo Agresor",
                     color_discrete_map={"MASCULINO":"navy",
                                         "FEMENINO":"hotpink",
                                         "S/R":"black"})
    fig.update_traces(textinfo="label+percent parent")
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"},
                        font_color="white",showlegend=False)
    return(fig)
    
@app.callback(Output('CardTiempo1', 'children'),
              [Input('slider_anios', 'value')])
def update_card(selected_year):
    df_temp= df[(df["Año"]>=selected_year[0]) &(df["Año"]<=selected_year[1]) & (df["Sexo Victima"]=="FEMENINO")]
    df_temp=df_temp.groupby(["Año"]).count()
    print(df_temp)
    maximo= df_temp.index[df_temp["Caja"].argmax()]
    return(maximo)

@app.callback(Output('CardTiempo2', 'children'),
              [Input('slider_anios', 'value')])
def update_card(selected_year):
    df_temp= df[(df["Año"]>=selected_year[0]) &(df["Año"]<=selected_year[1]) & (df["Sexo Victima"]=="MASCULINO")]
    df_temp=df_temp.groupby(["Año"]).count()
    print(df_temp)
    maximo= df_temp.index[df_temp["Caja"].argmax()]
    return(maximo)

@app.callback(Output('CardTiempo3', 'children'),
              [Input('slider_anios', 'value')])
def update_card(selected_year):
    df_temp= df[(df["Año"]>=selected_year[0]) &(df["Año"]<=selected_year[1])]
    return(len(df_temp))

@app.callback(Output('CardTiempo4', 'children'),
              [Input('slider_anios', 'value')])
def update_card(selected_year):
    df_temp= df[(df["Año"]>=selected_year[0]) &(df["Año"]<=selected_year[1])]
    df_temp= df_temp.groupby("Año").count()
    return(round(df_temp["Caja"].mean(),2))


@app.callback(Output('CardTiempo5', 'children'),
              [Input('slider_anios', 'value')])
def update_card(selected_year):
    df_temp= df[(df["Año"]>=selected_year[0]) &(df["Año"]<=selected_year[1]) & (df["Sexo Agresor"]=="MASCULINO")]
    df_temp=df_temp.groupby(["Año"]).count()
    print(df_temp)
    maximo= df_temp.index[df_temp["Caja"].argmax()]
    return(maximo)

@app.callback(Output('CardTiempo6', 'children'),
              [Input('slider_anios', 'value')])
def update_card(selected_year):
    df_temp= df[(df["Año"]>=selected_year[0]) &(df["Año"]<=selected_year[1]) & (df["Sexo Agresor"]=="FEMENINO")]
    df_temp=df_temp.groupby(["Año"]).count()
    print(df_temp)
    maximo= df_temp.index[df_temp["Caja"].argmax()]
    return(maximo)

@app.callback(Output('Hist_EdadVictima', 'figure'),
              [Input('slider-edadVictima', 'value'), Input('Años_Victima_Bins', 'value')])
def update_card(rango_edad, cantidad_bins):
    df_temp= df[(df["Edad Victima"]>=rango_edad[0]) & (df["Edad Victima"]<=rango_edad[1])]
    maximo=df_temp["Edad Victima"].max()
    df_temp["Edad Victima Grupos"]= (pd.cut(df_temp["Edad Victima"],np.arange(0,maximo+cantidad_bins,cantidad_bins)).astype(str).str.replace(","," a").str.replace("(","").str.replace("]",""))
    df_temp=df_temp[df_temp["Edad Victima"]!=-1]
    df_temp.sort_values(by="Edad Victima", inplace=True)
    fig= px.histogram(df_temp,x="Edad Victima Grupos", text_auto=True)
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"},
                        font_color="white")
    return(fig)

@app.callback(Output('Heatmap_Edad', 'figure'),
              [Input('slider-edadVictima', 'value'), Input('Años_Victima_Bins', 'value'),
              Input('slider-edadAgresor', 'value'), Input('Años_Agresor_Bins', 'value')])
def update_card(rango_edadV, cantidad_binsV, rango_edadA, cantidad_binsA):
    df_temp= df[(df["Edad Victima"]>=rango_edadV[0]) & (df["Edad Victima"]<=rango_edadV[1])]
    df_temp= df_temp[(df_temp["Edad Agresor"]>=rango_edadA[0]) & (df_temp["Edad Agresor"]<=rango_edadA[1])]
    maximo=df_temp["Edad Victima"].max()
    df_temp["Edad Victima Grupos"]= (pd.cut(df_temp["Edad Victima"],np.arange(0,maximo+cantidad_binsV,cantidad_binsV)).astype(str).str.replace(","," a").str.replace("(","").str.replace("]",""))
    df_temp=df_temp[df_temp["Edad Victima"]!=-1]
    vitimaCat= df_temp.sort_values(by="Edad Victima", ascending=False)["Edad Victima Grupos"].unique()

    maximo=df_temp["Edad Agresor"].max()
    df_temp["Edad Agresor Grupos"]= (pd.cut(df_temp["Edad Agresor"],np.arange(0,maximo+cantidad_binsA,cantidad_binsA)).astype(str).str.replace(","," a").str.replace("(","").str.replace("]",""))
    df_temp=df_temp[df_temp["Edad Agresor"]!=-1]
    agresorCat= df_temp.sort_values(by="Edad Agresor")["Edad Agresor Grupos"].unique()


    fig= px.density_heatmap(df_temp,x="Edad Agresor Grupos", y="Edad Victima Grupos", text_auto=True,
                            category_orders={"Edad Agresor Grupos":agresorCat, "Edad Victima Grupos":vitimaCat})
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"},
                        font_color="white")
    return(fig)

@app.callback(Output('Hist_EdadAgresor', 'figure'),
              [Input('slider-edadAgresor', 'value'), Input('Años_Agresor_Bins', 'value')])
def update_card(rango_edad, cantidad_bins):
    df_temp= df[(df["Edad Agresor"]>=rango_edad[0]) & (df["Edad Agresor"]<=rango_edad[1])]
    maximo=df_temp["Edad Agresor"].max()
    df_temp["Edad Agresor Grupos"]= (pd.cut(df_temp["Edad Agresor"],np.arange(0,maximo+cantidad_bins,cantidad_bins)).astype(str).str.replace(","," a").str.replace("(","").str.replace("]",""))
    df_temp=df_temp[df_temp["Edad Agresor"]!=-1]
    df_temp.sort_values(by="Edad Agresor", inplace=True)
    fig= px.histogram(df_temp,x="Edad Agresor Grupos", text_auto=True)
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"},
                        font_color="white")
    return(fig)

@app.callback(Output('CardEdad1', 'children'),
              [Input('slider-edadVictima', 'value'), Input('Años_Victima_Bins', 'value')])
def update_card(rango_edad, cantidad_bins):
    df_temp= df[(df["Edad Victima"]>=rango_edad[0]) & (df["Edad Victima"]<=rango_edad[1])]
    maximo=df_temp["Edad Victima"].max()
    df_temp["Edad Victima Grupos"]= (pd.cut(df_temp["Edad Victima"],np.arange(0,maximo+cantidad_bins,cantidad_bins)).astype(str).str.replace(","," a").str.replace("(","").str.replace("]",""))
    df_temp=df_temp[df_temp["Edad Victima"]!=-1]
    df_temp.sort_values(by="Edad Victima", inplace=True)
    df_temp= df_temp.groupby(["Edad Victima Grupos"]).count()
    return(df_temp.index[df_temp["Caja"].argmax()]+" años")


@app.callback(Output('CardEdad3', 'children'),
              [Input('slider-edadAgresor', 'value'), Input('Años_Agresor_Bins', 'value')])
def update_card(rango_edad, cantidad_bins):
    df_temp= df[(df["Edad Agresor"]>=rango_edad[0]) & (df["Edad Agresor"]<=rango_edad[1])]
    maximo=df_temp["Edad Agresor"].max()
    df_temp["Edad Agresor Grupos"]= (pd.cut(df_temp["Edad Agresor"],np.arange(0,maximo+cantidad_bins,cantidad_bins)).astype(str).str.replace(","," a").str.replace("(","").str.replace("]",""))
    df_temp=df_temp[df_temp["Edad Agresor"]!=-1]
    df_temp.sort_values(by="Edad Agresor", inplace=True)
    df_temp= df_temp.groupby(["Edad Agresor Grupos"]).count()
    return(df_temp.index[df_temp["Caja"].argmax()]+" años")

@app.callback(Output('CardEdad2', 'children'),
              [Input('slider-edadVictima', 'value'), Input('Años_Victima_Bins', 'value'),
              Input('slider-edadAgresor', 'value'), Input('Años_Agresor_Bins', 'value')])
def update_card(rango_edadV, cantidad_binsV, rango_edadA, cantidad_binsA):
    df_temp= df[(df["Edad Victima"]>=rango_edadV[0]) & (df["Edad Victima"]<=rango_edadV[1])]
    df_temp= df_temp[(df_temp["Edad Agresor"]>=rango_edadA[0]) & (df_temp["Edad Agresor"]<=rango_edadA[1])]
    maximo=df_temp["Edad Victima"].max()
    df_temp["Edad Victima Grupos"]= (pd.cut(df_temp["Edad Victima"],np.arange(0,maximo+cantidad_binsV,cantidad_binsV)).astype(str).str.replace(","," a").str.replace("(","").str.replace("]",""))
    df_temp=df_temp[df_temp["Edad Victima"]!=-1]

    maximo=df_temp["Edad Agresor"].max()
    df_temp["Edad Agresor Grupos"]= (pd.cut(df_temp["Edad Agresor"],np.arange(0,maximo+cantidad_binsA,cantidad_binsA)).astype(str).str.replace(","," a").str.replace("(","").str.replace("]",""))
    df_temp=df_temp[df_temp["Edad Agresor"]!=-1]
    df_temp= df_temp.groupby(["Edad Agresor Grupos", "Edad Victima Grupos"]).count().reset_index()
    grupoAgresor= df_temp["Edad Agresor Grupos"][df_temp["Caja"].argmax()]
    grupoVictima= df_temp["Edad Victima Grupos"][df_temp["Caja"].argmax()]
    return("Victimas de "+grupoVictima+" años y agresores de "+grupoAgresor+" años son el evento más común de casos")

@app.callback(Output('PieSexo', 'figure'),
              [Input('Radio_Victima_Agresor', 'value')])
def update_card(sexo):
    fig= px.sunburst(df, path=["Sexo "+sexo], color=("Sexo "+sexo),
                            color_discrete_map={"MASCULINO":"navy",
                                         "FEMENINO":"hotpink",
                                         "S/R":"black"})
    fig.update_traces(textinfo="label+percent parent")
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"},
                            font_color="white",showlegend=False)
    return(fig)

@app.callback(Output('SexoParentesco', 'figure'),
              [Input('Radio_Victima_Agresor', 'value')])
def update_card(sexo):
    fig=px.sunburst(df, path=["Sexo "+sexo,"Parentesco"],color="Sexo "+sexo,
                    color_discrete_map={"MASCULINO":"navy",
                                         "FEMENINO":"hotpink",
                                         "S/R":"black"})
    fig.update_traces(textinfo="label+percent parent")
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"},
                            font_color="white",showlegend=False)
    return(fig)

@app.callback(Output('SexoEdoCivil', 'figure'),
              [Input('Radio_Victima_Agresor', 'value')])
def update_card(sexo):
    fig=px.sunburst(df, path=["Sexo "+sexo,"Estado Civil"],color="Sexo "+sexo,
                    color_discrete_map={"MASCULINO":"navy",
                                         "FEMENINO":"hotpink",
                                         "S/R":"black"})
    fig.update_traces(textinfo="label+percent parent")
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"},
                            font_color="white",showlegend=False)
    return(fig)

@app.callback(Output('CardSexo1', 'children'),
              [Input('Radio_Victima_Agresor', 'value')])
def update_card(sexo):
    parentesco= df[df["Sexo "+sexo]=="MASCULINO"]["Parentesco"].value_counts().index[0]
    if(sexo=="Victima"):
        return("De las Víctimas masculinas, el mayor parentesco con su agresor es: "+parentesco)
    else:
        return("De los agresores maculinos, la mayoría son el: "+parentesco + " de la Víctima")

@app.callback(Output('CardSexo2', 'children'),
              [Input('Radio_Victima_Agresor', 'value')])
def update_card(sexo):
    parentesco= df[df["Sexo "+sexo]=="FEMENINO"]["Parentesco"].value_counts().index[0]
    if(sexo=="Victima"):
        return("De las Víctimas femeninas, el mayor parentesco con su agresor es: "+parentesco)
    else:
        return("De las agresores femeninas, la mayoría son la: "+parentesco + " de la Víctima")

@app.callback(Output('CardSexo3', 'children'),
              [Input('Radio_Victima_Agresor', 'value')])
def update_card(sexo):
    mayorSexo= df["Sexo "+sexo].value_counts().index[0]
    if(sexo=="Victima"):
        return("El sexo con mayor número de Víctimas es: "+mayorSexo)
    else:
        return("El sexo con mayor número de Agresores es: "+mayorSexo)

@app.callback(Output('CardSexo4', 'children'),
              [Input('Radio_Victima_Agresor', 'value')])
def update_card(sexo):
    edocivil= df[df["Sexo "+sexo]=="FEMENINO"]["Estado Civil"].value_counts().index[0]
    if(sexo=="Victima"):
        return("De las Víctimas femeninas, el mayor estado civil que tienen es: "+edocivil)
    else:
        return("De las Agresoras femeninas, el mayor estado civil que tienen es: "+edocivil)

@app.callback(Output('CardSexo5', 'children'),
              [Input('Radio_Victima_Agresor', 'value')])
def update_card(sexo):
    edocivil= df[df["Sexo "+sexo]=="FEMENINO"]["Estado Civil"].value_counts().index[0]
    if(sexo=="Victima"):
        return("De las Víctimas masculinas, el mayor estado civil que tienen es: "+edocivil)
    else:
        return("De los Agresores masculinos, el mayor estado civil que tienen es: "+edocivil)

@app.callback(Output('Violencia1', 'figure'),
              [Input('Radio_Victima_Agresor2', 'value')])
def update_card(sexo):
    fig=px.sunburst(df_ViolenciaExpandido, path=["Sexo "+sexo,"Tipo Violencia"],color="Sexo "+sexo,
                    color_discrete_map={"MASCULINO":"navy",
                                         "FEMENINO":"hotpink",
                                         "S/R":"black"})
    fig.update_traces(textinfo="label+percent parent")
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"},
                            font_color="white",showlegend=False)
    return(fig)


@app.callback(Output('Violencia3', 'figure'),
              [Input('Radio_Otros', 'value')])
def update_card(variable):
    fig=px.sunburst(df_ViolenciaExpandido, path=[variable,"Tipo Violencia"],color=variable)
    fig.update_traces(textinfo="label+percent parent")
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(0, 0, 0, 0)"},
                            font_color="white",showlegend=False)
    return(fig)

@app.callback(Output('CardViolencia1', 'children'),
              [Input('Radio_Victima_Agresor2', 'value')])
def update_card(sexo):
    if(sexo=="Victima"):
        tipoViolencia= df[df["Sexo Victima"]=="MASCULINO"]["Tipo Violencia"].value_counts().index[0]
        return("Para víctimas masculinas, la violencia más frecuente es "+tipoViolencia)
    else:
        tipoViolencia= df[df["Sexo Agresor"]=="MASCULINO"]["Tipo Violencia"].value_counts().index[0]
        return("Para agresores masculinos, la violencia más frecuente es "+tipoViolencia)


@app.callback(Output('CardViolencia2', 'children'),
              [Input('Radio_Victima_Agresor2', 'value')])
def update_card(sexo):
    if(sexo=="Victima"):
        tipoViolencia= df[df["Sexo Victima"]=="FEMENINO"]["Tipo Violencia"].value_counts().index[0]
        return("Para víctimas femeninas, la violencia más frecuente es "+tipoViolencia)
    else:
        tipoViolencia= df[df["Sexo Agresor"]=="FEMENINO"]["Tipo Violencia"].value_counts().index[0]
        return("Para agresoras femeninas, la violencia más frecuente es "+tipoViolencia)

@app.callback(Output('CardViolencia5', 'children'),
              [Input('Radio_Otros', 'value')])
def update_card(variable):
    if(variable=="Parentesco"):
        parentesco= df["Parentesco"].value_counts().index[0]
        resultado= df[df["Parentesco"]==parentesco]["Tipo Violencia"].value_counts().index[0]
        return("Cuando el parentsco es "+parentesco + ", la violencia más frecuente es "+resultado)
    else:
        estado= df["Estado Civil"].value_counts().index[0]
        resultado= df[df["Estado Civil"]==estado]["Tipo Violencia"].value_counts().index[0]
        return("Cuando el edo. civil es "+estado + ", la violencia más frecuente es "+resultado)

@app.callback(Output('CardViolencia6', 'children'),
              [Input('Radio_Otros', 'value')])
def update_card(variable):
    if(variable=="Parentesco"):
        parentesco= df["Parentesco"].value_counts().index[0]
        resultado= df[df["Parentesco"]==parentesco]["Tipo Violencia"].value_counts().index[-1]
        return("Cuando el parentsco es "+parentesco + ", la violencia menos frecuente es "+resultado)
    else:
        estado= df["Estado Civil"].value_counts().index[0]
        resultado= df[df["Estado Civil"]==estado]["Tipo Violencia"].value_counts().index[-1]
        return("Cuando el edo. civil es "+estado + ", la violencia menos frecuente es "+resultado)

if __name__ == '__main__':
    app.run_server()

