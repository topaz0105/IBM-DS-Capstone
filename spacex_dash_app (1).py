# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# get the launch sites from the data
unique_sites = spacex_df['Launch Site'].unique().tolist()
launch_sites = []
launch_sites.append({'label':  'All Sites', 'value': 'ALL'})
for launch_site in unique_sites:
    launch_sites.append({'label': launch_site, 'value': launch_site})


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options = launch_sites,
                                    placeholder = 'Select a Launch Site here',
                                    searchable = True,
                                    clearable = False,
                                    value = 'ALL'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min = 0,
                                    max = 10000,
                                    step = 1000,
                                    value = [min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ]
                        )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value')
)
def display_pie_graph(entered_site):
    if (entered_site == 'ALL' or entered_site == 'None'):
        all_sites = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(
                all_sites,
                names = 'Launch Site',
                title = 'Launch Site Successes',
        )
    else:
        specific_site = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
                specific_site,
                names = 'class',
                title = 'Launch Site Successes',
        )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id = 'success-payload-scatter-chart',component_property = 'figure'),
    [Input(component_id = 'site-dropdown', component_property = 'value'),
    Input(component_id = "payload-slider", component_property = "value")]
)
def display_scattergraph(entered_site,slider_range):
    low, high = slider_range
    masks = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    df_scatter = spacex_df[masks]
    
    if (entered_site == 'ALL' or entered_site == 'None'):
        fig = px.scatter(
            df_scatter,
            x = "Payload Mass (kg)",
            y = "class",
            title = 'Correlation Between Payload and Success for all sites',
            color = "Booster Version Category",
        )
    else:
        filtered_scatter = df_scatter[df_scatter['Launch Site'] == entered_site]
        fig = px.scatter(
            filtered_scatter,
            x = "Payload Mass (kg)",
            y = "class",
            title = 'Correlation Between Payload and Success for Site',
            color = "Booster Version Category",
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
