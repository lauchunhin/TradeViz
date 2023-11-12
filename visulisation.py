#* Implemented DataVisualizer Class
#* Import libraries
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

class DataVisualizer:
    def __init__(self, data_interface, title='Data Visualizer', xaxis_title='Date', colors=None):
        self.data_interface = data_interface
        self.title = title
        self.xaxis_title = xaxis_title
        self.colors = colors if colors is not None else ['orange', 'black', 'dimgrey', 'skyblue', 'darkgreen','red', 'gold', 'navy']

    def visualize_data(self):
        #* Fetch and refine the data
        data = self.data_interface.fetch_data()

        #* Create a Dash app with external stylesheets
        external_stylesheets = [dbc.themes.LUX]
        app = Dash(__name__, external_stylesheets=external_stylesheets)

        #* Create a layout with a dropdown menu and a graph
        app.layout = dbc.Container([
            #* Add space above the title
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),

            dbc.Row([
                html.Div(self.title, className="text-primary text-center fs-3")
            ]),

            #* Add space above the title
            html.Br(),
            html.Br(),
            html.Br(),

            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        options=[{'label': k, 'value': k} for k in data.columns],
                        value=data.columns[0],
                        id='dropdown-selection',
                        style={'width': '85%', 'display': 'inline-block'}
                    )
                ], width={'size': 6, 'offset': 4}),  # Adjust the size and offset to suit your needs
            ]),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure={}, id='graph-content')
                ]),
            ]),

        ], fluid=True)

        #* Define a callback to update the graph
        @app.callback(
            Output('graph-content', 'figure'),
            [Input('dropdown-selection', 'value')]
        )
        def update_graph(selected_dropdown_value):
            fig = go.Figure()
            for i, metric in enumerate(data.columns):
                df_metric = data[[selected_dropdown_value]]
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=df_metric[selected_dropdown_value],
                    name=metric,
                    hovertemplate = 
                    '<b>%{fullData.name}</b><br>' + 
                    '<i>Date</i>: %{x|%d %b, %Y}' +
                    '<br><b>Value</b>: %{y:.2f}<br>' +
                    '<extra></extra>',
                    line=dict(color=self.colors[i % len(self.colors)])
                ))

            fig.update_layout(
                autosize=True,  
                legend=dict(
                    x=0.1,
                    y=-0.2,
                    orientation="h",
                    borderwidth=1
                ),
                plot_bgcolor='white',
                
                hovermode='x unified',
                xaxis=dict(showspikes=True, spikemode='across', spikesnap='cursor', spikecolor='rgba(128,128,128,0.5)', spikethickness=1),
                yaxis=dict(showspikes=True, spikemode='across', spikesnap='cursor', spikecolor='rgba(128,128,128,0.5)', spikethickness=1)
            )

            fig.update_xaxes(
                nticks=15,
                tickformat="%d %b, %Y",
                showgrid=False,
            )

            return fig

        #* Run the app at http://127.0.0.1:8050/
        app.run_server(debug=True)
