# The code is importing various libraries and modules in Python.
import numpy as np
import pandas as pd
import flask
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

URL = ('https://raw.githubusercontent.com/mayukudore/SpaceX_Success/main/spacex_launch_dash.csv')
spacex_df = pd.read_csv(URL)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
temp_payload = spacex_df['Payload Mass (kg)'].apply(np.floor).copy()
index_payload_dict = []
for work in temp_payload:
    index_payload_dict.append(str(work))

temp_payload = temp_payload.set_axis(index_payload_dict)
payload_as_dict = temp_payload.to_dict()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': 'green',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label':ALL, 'value':ALL} for ALL in spacex_df['Launch Site'].unique()], value='Site'
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=min_payload, max=max_payload, step=None, marks=payload_as_dict, value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
    if entered_site == 'Site':
        fig = px.pie(data_frame=filtered_df, values='class', 
        names='Launch Site'
       )
        return fig
    else:
            one_site = spacex_df.loc[(spacex_df['Launch Site'] == entered_site)]
            chosen_site = one_site.groupby('class')['class'].count()
            chosen_site= chosen_site.to_frame()
            fig = px.pie(values=[chosen_site['class'][1], chosen_site['class'][0]], names = ['Success', 'Failure'])
            return fig
        
@app.callback(
              Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='payload-slider', component_property='value'), Input(component_id="site-dropdown", component_property="value")])
                 
def get_scatter_graph(payload_slider, site_dropdown):
    working_df = spacex_df[['Payload Mass (kg)', 'class', 'Booster Version Category']].copy()
    if payload_slider == [min_payload, max_payload]:
        fig = px.scatter(data_frame= working_df, x = 'Payload Mass (kg)', y = 'class', color="Booster Version Category")
        return fig
    
  
       
        
   

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run()
