import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Statistics Dashboard"

# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast': 'center'}
        )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': str(i), 'value': i} for i in range(1980, 2024)],
            placeholder='Select a year',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast': 'center'},
            disabled=True
        )),
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ])
])

# Callback to enable/disable input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Callback for plotting
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Average Automobile sales during the recession period
        recession_sales = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(recession_sales, x='Year', y='Automobile_Sales', title='Average Automobile Sales during Recession Period')
        )

        # Plot 2: Average number of vehicles sold by vehicle type during recession
        recession_vehicle_sales = recession_data.groupby(['Year', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(recession_vehicle_sales, x='Year', y='Automobile_Sales', color='Vehicle_Type', barmode='group', title='Average Vehicles Sold by Vehicle Type during Recession Period')
        )

        # Plot 3: Total expenditure share by vehicle type during recession
        exp_vehicle_recession = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_vehicle_recession, values='Advertising_Expenditure', names='Vehicle_Type', title='Total Expenditure Share by Vehicle Type during Recession Period')
        )

        # Plot 4: Effect of unemployment rate on vehicle type and sales during recession
        R_chart4 = dcc.Graph(
            figure=px.bar(recession_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type', barmode='group', title='Effect of Unemployment Rate on Vehicle Type and Sales during Recession')
        )

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2]),
            html.Div(className='chart-item', children=[R_chart3, R_chart4])
        ]

    elif (selected_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == selected_year]

        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yearly_sales = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yearly_sales, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales')
        )

        # Plot 2: Total Monthly Automobile sales using line chart
        monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(monthly_sales, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales')
        )

        # Plot 3: Average Monthly Automobile sales of each vehicle type using bar chart
        average_monthly_sales = yearly_data.groupby(['Month', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(average_monthly_sales, x='Month', y='Automobile_Sales', color='Vehicle_Type', barmode='group', title='Average Monthly Automobile Sales by Vehicle Type')
        )

        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_vehicle = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_vehicle, values='Advertising_Expenditure', names='Vehicle_Type', title='Total Advertisement Expenditure by Vehicle Type')
        )

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2]),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4])
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
