import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import pandas as pd

app = dash.Dash(__name__)

# Define your weather API endpoint and API key
api_endpoint = "http://api.weatherapi.com/v1/history.json?key=891762cdedce4c408cc61510231909&q=Angeles City&dt=2023-07-01"  # Replace with the actual API endpoint
api_key = "891762cdedce4c408cc61510231909"  # Replace with your API key

# Function to fetch weather data from the API
def fetch_weather_data():
    params = {
        'location': 'Angeles City',  # Specify the location
        'start_date': '2023-07-01',  # Specify the start date
        'end_date': '2023-10-31',    # Specify the end date
        'api_key': '891762cdedce4c408cc61510231909'
    }
    
    response = requests.get(api_endpoint, params=params)
    
    if response.status_code == 403:
        weather_data = response.json()  # Parse JSON response
        return weather_data
    else:
        return None

# Define CSS styles for layout and components
app.layout = html.Div([
    html.H1("Angeles City Weather Time Series", style={'textAlign': 'center', 'color': '#333', 'font-size': '24px'}),
    
    dcc.Graph(
        id='graph',
        config={'displayModeBar': False},
        style={'height': '400px', 'margin': '20px'},
    ),
    
    dcc.Interval(
        id='interval',
        interval=10000,  # Update every 10 seconds
        disabled=False
    )
])

@app.callback(
    Output('graph', 'figure'),
    [Input('interval', 'n_intervals')]
)
def update_graph(n):
    # Fetch weather data from the API
    weather_data = fetch_weather_data()

    if weather_data:
        # Extract temperature data and dates from the API response
        dates = [entry['date'] for entry in weather_data]
        temperatures = [entry['temperature'] for entry in weather_data]

        # Create a bar graph
        trace = go.Bar(
            x=dates,
            y=temperatures,
            name='Temperature Bar Chart',
            marker={'color': '#007BFF'}  # Customize the bar color
        )
        layout = go.Layout(
            title='Angeles City Weather Time Series (Bar Chart)',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Temperature (°C)'),
            font=dict(color='#3c0008')  # Customize font color
        )
        return {'data': [trace], 'layout': layout}
    else:
        # Handle API request error
        return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)
