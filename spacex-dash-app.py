# # Import required libraries
# import pandas as pd
# import dash
# from dash import html
# from dash import dcc
# from dash.dependencies import Input, Output
# import plotly.express as px

# # Read the airline data into pandas dataframe
# spacex_df = pd.read_csv("spacex_launch_dash.csv")
# max_payload = spacex_df['Payload Mass (kg)'].max()
# min_payload = spacex_df['Payload Mass (kg)'].min()

# # Create a dash application
# app = dash.Dash(__name__)

# # Create an app layout
# app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
#                                         style={'textAlign': 'center', 'color': '#503D36',
#                                                'font-size': 40}),
#                                 # TASK 1: Add a dropdown list to enable Launch Site selection
#                                 # The default select value is for ALL sites
#                                 # dcc.Dropdown(id='site-dropdown',...)
#                                 html.Br(),

#                                 # TASK 2: Add a pie chart to show the total successful launches count for all sites
#                                 # If a specific launch site was selected, show the Success vs. Failed counts for the site
#                                 html.Div(dcc.Graph(id='success-pie-chart')),
#                                 html.Br(),

#                                 html.P("Payload range (Kg):"),
#                                 # TASK 3: Add a slider to select payload range
#                                 #dcc.RangeSlider(id='payload-slider',...)

#                                 # TASK 4: Add a scatter chart to show the correlation between payload and launch success
#                                 html.Div(dcc.Graph(id='success-payload-scatter-chart')),
#                                 ])

# # TASK 2:
# # Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# # TASK 4:
# # Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# # Run the app
# if __name__ == '__main__':
#     app.run()

# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get min and max payload values
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Get list of unique launch sites
launch_sites = spacex_df['Launch Site'].unique().tolist()

# Create dropdown options
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}]
dropdown_options += [{'label': site, 'value': site} for site in launch_sites]

# Create Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),

    # TASK 1: Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=dropdown_options,
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    html.Br(),

    # Pie chart for launch success
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # Scatter plot for success vs payload
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Success Launches by Site'
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        outcome_counts = filtered_df['class'].value_counts().reset_index()
        outcome_counts.columns = ['Outcome', 'Count']
        outcome_counts['Outcome'] = outcome_counts['Outcome'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(
            outcome_counts,
            names='Outcome',
            values='Count',
            title=f'Total Success vs Failure for site {entered_site}'
        )
        return fig

# TASK 4: Callback for scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_plot(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Success Rate by Payload for All Sites'
        )
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Success Rate by Payload for site {entered_site}'
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
