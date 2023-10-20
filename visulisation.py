# import libraries
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import openpyxl

#* Load excel file from computer 
#! Change the path below
xl = pd.ExcelFile('/Users/lauchunhin/miniforge3/US_HIN.xlsx')

#! Load a sheet into a DataFrame by name -> df = xl.parse('Sheet1')
df = xl.parse()
# Make a copy of the DataFrame for testing
df_testing = df.copy()
# Convert the dataframe from wide to long format, keeping 'DATE' as id_vars
df_melted = df_testing.melt(id_vars='DATE', var_name='Metrics', value_name='VALUE')
# Swap 'DATE' and 'Metrics' column names
df_melted.rename(columns={'DATE': 'Metrics', 'Metrics': 'DATE'}, inplace=True)
# Convert 'DATE' to datetime format
df_melted['DATE'] = pd.to_datetime(df_melted['DATE']).dt.date
# Handle NA values by deleting the entire row
df_melted.dropna(inplace=True)


#* Visualization
# Incorporate data
df = df_melted
# Define your color sequence
colors = ['black', 'orange', 'dimgrey', 'skyblue', 'darkgreen','red', 'gold', 'navy']
colors_ind = ['forestgreen', 'darkred', 'lightgrey']

# Define your groups of metrics
metric_groups = {
    'CUMULATIVE BULL/BEAR POWER TRIGGER': ['SPX CLOSE', 'BULL/BEAR POWER TRIGGER POSITION%', 'AVERAGE BO INDICATOR', 'CUMULATIVE BULL/BEAR POWER TRIGGER', 'CUMULATIVE BULL/BEAR POWER TRIGGER(5MA)', 'CUMULATIVE BULL/BEAR POWER TRIGGER(20MA)', 'CUMULATIVE BULL/BEAR POWER TRIGGER(50MA)', 'CUMULATIVE BULL/BEAR POWER TRIGGER LAST to 5MA', 'CUMULATIVE BULL/BEAR POWER TRIGGER LAST to 20MA', 'CUMULATIVE BULL/BEAR POWER TRIGGER LAST to 50MA'],
    'CUMULATIVE Net Number of P/C Ratio 20D-HL': ['SPX CLOSE', 'BULL/BEAR POWER TRIGGER POSITION%', 'AVERAGE BO INDICATOR', 'CUMULATIVE NET Number of P/C Ratio 20D-HL', 'CUMULATIVE NET Number of P/C Ratio 20D-HL(5MA)', 'CUMULATIVE NET Number of P/C Ratio 20D-HL(20MA)', 'CUMULATIVE NET Number of P/C Ratio 20D-HL-LAST to 5MA', 'CUMULATIVE NET Number of P/C Ratio 20D-HL-LAST to 20MA'],
    'CUMULATIVE Net Number of P/C Ratio 5D-HL': ['SPX CLOSE', 'BULL/BEAR POWER TRIGGER POSITION%', 'AVERAGE BO INDICATOR', 'CUMULATIVE NET Number of P/C Ratio 5D-HL', 'CUMULATIVE NET Number of P/C Ratio 5D-HL(5MA)', 'CUMULATIVE NET Number of P/C Ratio 5D-HL(20MA)', 'CUMULATIVE NET Number of P/C Ratio 5D-HL-LAST to 5MA', 'CUMULATIVE NET Number of P/C Ratio 5D-HL-LAST to 20MA'],
    'STOCK-AVERAGE-POS-5D': ['SPX CLOSE', 'BULL/BEAR POWER TRIGGER POSITION%', 'AVERAGE BO INDICATOR', 'STOCK-AVERAGE-POS-5D CUMULATIVE NET 5D-HL', 'STOCK-AVERAGE-POS-5D CUMULATIVE NET 5D-HL(5MA)', 'STOCK-AVERAGE-POS-5D CUMULATIVE NET 5D-HL(20MA)', 'STOCK-AVERAGE-POS-5D LAST to 5MA', 'STOCK-AVERAGE-POS-5D LAST to 20MA'],
    'STOCK-AVERAGE-POS-20D': ['SPX CLOSE', 'BULL/BEAR POWER TRIGGER POSITION%', 'AVERAGE BO INDICATOR', 'STOCK-AVERAGE-POS-20D CUMULATIVE NET 20D-HL', 'STOCK-AVERAGE-POS-20D CUMULATIVE NET 20D-HL(5MA)', 'STOCK-AVERAGE-POS-20D CUMULATIVE NET 20D-HL(20MA)', 'STOCK-AVERAGE-POS-20D LAST to 5MA', 'STOCK-AVERAGE-POS-20DLAST to 20MA'],
    'CUMULATIVE Net Number of DMI BULL/BEAR': ['SPX CLOSE', 'BULL/BEAR POWER TRIGGER POSITION%', 'AVERAGE BO INDICATOR', 'CUMULATIVE NET Number of DMI BULL/BEAR', 'CUMULATIVE NET Number of DMI BULL/BEAR(5MA)', 'CUMULATIVE NET Number of DMI BULL/BEAR(20MA)', 'CUMULATIVE NET Number of DMI BULL/BEAR(50MA)', 'CUMULATIVE NET Number of DMI BULL/BEAR LAST to 5MA', 'CUMULATIVE NET Number of DMI BULL/BEAR LAST to 20MA', 'CUMULATIVE NET Number of DMI BULL/BEAR LAST to 20MA'],
    'CUMULATIVE TURNOVER Z-SCORE': ['SPX CLOSE', 'BULL/BEAR POWER TRIGGER POSITION%', 'AVERAGE BO INDICATOR', 'CUMULATIVE TURNOVER Z-SCORE', 'CUMULATIVE TURNOVER Z-SCORE(5MA)', 'CUMULATIVE TURNOVER Z-SCORE(20MA)', 'TURNOVER Z-SCORE LAST to 5MA', 'TURNOVER Z-SCORE LAST to 20MA'],
    'CUMULATIVE Net Number of 5D +VE RETURN': ['SPX CLOSE', 'BULL/BEAR POWER TRIGGER POSITION%', 'AVERAGE BO INDICATOR', 'CUMULATIVE NET NUMBER of 5D +VE RETURN', 'CUMULATIVE NET NUMBER of 5D +VE RETURN(5MA)', 'CUMULATIVE NET NUMBER of 5D +VE RETURN(20MA)', 'CUMULATIVE NET NUMBER of 5D +VE RETURN LAST to 5MA', 'CUMULATIVE NET NUMBER of 5D +VE RETURN LAST to 20MA'],
    'CUMULATIVE Net Number of 10D +VE RETURN': ['SPX CLOSE', 'BULL/BEAR POWER TRIGGER POSITION%', 'AVERAGE BO INDICATOR', 'CUMULATIVE NET NUMBER of 10D +VE RETURN', 'CUMULATIVE NET NUMBER of 10D +VE RETURN(5MA)', 'CUMULATIVE NET NUMBER of 10D +VE RETURN(20MA)', 'CUMULATIVE NET NUMBER of 10D +VE RETURN LAST to 5MA', 'CUMULATIVE NET NUMBER of 10D +VE RETURN LAST to 20MA'],
}

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)

#* App layout
app.layout = dbc.Container([
    # Add space above the title
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    
    dbc.Row([
        html.Div('US Analyser', className="text-primary text-center fs-3")
    ]),
    
    # Add space above the title
    html.Br(),
    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                options=[{'label': k, 'value': k} for k in metric_groups.keys()],
                value=list(metric_groups.keys())[0],
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

#* Add controls to build the interaction
@callback(
    Output(component_id='graph-content', component_property='figure'),
    Input(component_id='dropdown-selection', component_property='value')
)

def update_graph(value):
    metrics = metric_groups[value]

    # Filter the DataFrame to only include rows with a metric in the selected group
    dff = df[df.Metrics.isin(metrics)]
    
    # Create a line plot for each metric in the group
    fig = go.Figure()
    
    
    for i, metric in enumerate(metrics):
        df_metric = dff[dff.Metrics == metric]
        if metric in ['SPX CLOSE','BULL/BEAR POWER TRIGGER POSITION%', 'AVERAGE BO INDICATOR']:
            fig.add_trace(go.Scatter(
                x=df_metric['DATE'], 
                y=df_metric['VALUE'], 
                name=metric,
                hovertemplate = 
                '<b>%{fullData.name}</b><br>' + 
                '<i>Date</i>: %{x|%d %b, %Y}' +
                '<br><b>Value</b>: %{y:.2f}<br>' +
                '<extra></extra>',
                yaxis='y2',
                visible='legendonly',  # This line hides the trace by default
                line=dict(color=colors_ind[i % len(colors)])  # Apply color sequence
            ))
        else:
            fig.add_trace(go.Scatter(
                x=df_metric['DATE'], 
                y=df_metric['VALUE'], 
                name=metric,
                hovertemplate = 
                '<b>%{fullData.name}</b><br>' + 
                '<i>Date</i>: %{x|%d %b, %Y}' +
                '<br><b>Value</b>: %{y:.2f}<br>' +
                '<extra></extra>',
                line=dict(color=colors[i % len(colors)])
            ))

    
    # Manage range 
    df_filtered = dff[dff['Metrics'].str.startswith(value)]
    # Set y-axis limits
    fig.update_yaxes(
        range=[df_filtered['VALUE'].min(),df_filtered['VALUE'].max()],
        showgrid=True,  # This shows the horizontal grid lines
        gridcolor='LightGrey',  # This changes the gridline color
        tickformat=","  # This line changes the y-axis tick labels to show exact numbers
    )
    
    
    # Set the size of the graph
    fig.update_layout(
        autosize=False,  
        height=800,
        legend=dict(
            x=0.1,
            y=-0.2,
            orientation="h",
            borderwidth=1
        ),
        plot_bgcolor='white',
        # Add secondary y-axis
        yaxis2=dict(
            title='INDICATORS',
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        # Add crosshair lines
        xaxis=dict(showspikes=True, spikemode='across', spikesnap='cursor', spikecolor='rgba(128,128,128,0.5)', spikethickness=1),
        yaxis=dict(showspikes=True, spikemode='across', spikesnap='cursor', spikecolor='rgba(128,128,128,0.5)', spikethickness=1)
    )
    
    # Set x-axis to be monthly
    fig.update_xaxes(
        nticks=25,
        tickformat="%d %b, %Y",
        showgrid=False,  # This removes the vertical grid lines
    )
    
    return fig
    
# Run the app
if __name__ == '__main__':
    app.run(debug=True)