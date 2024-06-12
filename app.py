import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine

# Configurações do Banco de Dados
DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/DesafioDNCbd'

# Crie a aplicação Dash
app = dash.Dash(__name__)

# Conexão ao banco de dados para leitura de dados
engine = create_engine(DATABASE_URI)
weather_df = pd.read_sql('clima', engine)
traffic_df = pd.read_sql('traffic', engine)

# Layout da aplicação Dash
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Clima e Trânsito'),

    html.Div(children='''
        Visualize os dados de clima e trânsito.
    '''),

    html.Label('Selecione a Localização:'),
    dcc.Dropdown(
        id='location-dropdown',
        options=[
            {'label': location, 'value': location} for location in weather_df['city'].unique()
        ],
        value=weather_df['city'].unique()[0]
    ),

    dcc.Graph(id='weather-graph'),

    html.Label('Selecione a Origem e Destino:'),
    dcc.Dropdown(
        id='route-dropdown',
        options=[
            {'label': f"{row['origin']} para {row['destination']}", 'value': index}
            for index, row in traffic_df.iterrows()
        ],
        value=traffic_df.index[0]
    ),

    dcc.Graph(id='traffic-graph')
])

# Callbacks para atualizar os gráficos com base nas seleções do usuário
@app.callback(
    Output('weather-graph', 'figure'),
    Input('location-dropdown', 'value')
)
def update_weather_graph(selected_location):
    filtered_df = weather_df[weather_df['city'] == selected_location]
    
    # Criação do gráfico de barras com temperatura e umidade
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=filtered_df['timestamp'],
        y=filtered_df['temperature'],
        name='Temperatura (°C)',
        marker_color='blue',
        yaxis='y'
    ))

    fig.add_trace(go.Bar(
        x=filtered_df['timestamp'],
        y=filtered_df['humidity'],
        name='Umidade (%)',
        marker_color='orange',
        yaxis='y2'
    ))

    # Atualização do layout do gráfico para incluir um eixo y secundário
    fig.update_layout(
        title=f'Temperatura e Umidade em {selected_location}',
        xaxis_title='Data',
        yaxis=dict(
            title='Temperatura (°C)',
            side='left'
        ),
        yaxis2=dict(
            title='Umidade (%)',
            side='right',
            overlaying='y',
            showgrid=False
        ),
        barmode='relative',
        legend=dict(x=0, y=1.2)
    )
    
    return fig

@app.callback(
    Output('traffic-graph', 'figure'),
    Input('route-dropdown', 'value')
)
def update_traffic_graph(selected_route):
    selected_row = traffic_df.loc[selected_route]
    route_data = traffic_df[(traffic_df['origin'] == selected_row['origin']) & 
                            (traffic_df['destination'] == selected_row['destination'])]
    fig = go.Figure(go.Bar(
        x=route_data['timestamp'],
        y=route_data['duration'],
        name='Duração da Viagem',
        marker_color='green'
    ))
    
    fig.update_layout(
        title=f'Duração da Viagem de {selected_row["origin"]} para {selected_row["destination"]}',
        xaxis_title='Data',
        yaxis_title='Duração (s)',
        legend=dict(x=0, y=1.2)
    )
    
    return fig

# Executa a aplicação Dash
if __name__ == '__main__':
    app.run_server(debug=True)
