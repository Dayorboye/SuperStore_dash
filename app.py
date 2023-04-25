
import dash
import pandas as pd
import numpy as np
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash import no_update


# Dash Application

app = dash.Dash(__name__,  external_stylesheets=[dbc.themes.VAPOR])
server = app.server

Sup_clean = pd.read_csv('Sup_clean1.csv')

state_code = {'Kentucky': 'KY', 'California': 'CA', 'Florida': 'FL', 'North Carolina': 'NC',
       'Washington': 'WA', 'Texas': 'TX', 'Wisconsin': 'WI', 'Utah': 'UT', 'Nebraska': 'NE',
       'Pennsylvania': 'PA', 'Illinois': 'IL', 'Minnesota': 'MN', 'Michigan': 'MI', 'Delaware': 'DE',
       'Indiana': 'IN', 'New York': 'NY', 'Arizona': 'AZ', 'Virginia': 'VA', 'Tennessee': 'TN',
       'Alabama': 'AL', 'South Carolina': 'SC', 'Oregon': 'OR', 'Colorado': 'CO', 'Iowa': 'IA', 'Ohio': 'OH',
       'Missouri': 'MO', 'Oklahoma': 'OK', 'New Mexico': 'NM', 'Louisiana': 'LA', 'Connecticut': 'CT',
       'New Jersey': 'NJ', 'Massachusetts': 'MA', 'Georgia': 'GA', 'Nevada': 'NA', 'Rhode Island': 'RI',
       'Mississippi': 'MS', 'Arkansas': 'AR', 'Montana': 'MT', 'New Hampshire': 'NH', 'Maryland': 'MD',
       'District of Columbia': 'DC', 'Kansas': 'KS', 'Vermont': 'VT', 'Maine': 'ME',
       'South Dakota': 'SD', 'Idaho': 'ID', 'North Dakota': 'ND', 'Wyoming': 'WY',
       'West Virginia': 'WV'}

Sup_clean['state_code'] = Sup_clean.State.apply(lambda X: state_code[X])

state_data = Sup_clean[['Sales', 'Profit', 'state_code']].groupby('state_code').sum()


def choropleth2():
    fig = go.Figure(data = go.Choropleth(
    locations = state_data.index, # Spartial coordinates
    z = state_data.Profit, #Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries i  ''
    colorscale = [[0, 'rgb(255,0,0)'],[0.25, 'rgb(255,255,255)'], [0.45, 'rgb(124, 208, 247)'], [0.6, 'rgb(97,255,140)'],[1, 'rgb(8,181,0)']],
    colorbar_title = 'Profit In USD',
    
    ))


    fig.update_layout(
    title_text =' Total State Wise Profit/Loss',
    geo_scope = 'usa',
    height = 600,
    )
    return fig


def choropleth():
    fig = go.Figure(data=go.Choropleth(
      locations = state_data.index,
      z = state_data.Sales,
      locationmode = 'USA-states',
      colorscale = 'Reds',
      colorbar_title = 'Sales in USD',
    ))

    fig.update_layout(
    title_text = 'Total State_Wise Sales',
    geo_scope = 'usa',
    height = 600,
    )
    
    return fig

Sup_cl = pd.read_csv('SampleSuperstore.csv')
Customer_option = Sup_cl['Category'].unique()
print(Customer_option)
Sup_cl['price_per_product'] = Sup_cl.Sales / Sup_cl.Quantity

Sup_cl['profit_per_product'] = Sup_cl.Profit / Sup_cl.Quantity



# data = Sup_clean.groupby(['Category'])

def scatgrap_profprdt(data):
    sizes = np.absolute(data.profit_per_product)
    fig = px.scatter(data, x = 'price_per_product',
                         color = 'Sub-Category',
                         size = sizes, hover_data = ['Sub-Category'])
    
    fig.update_layout(
        autosize = True,    
        height = 500,
        xaxis = dict(title = 'Price per Product'),
        yaxis = dict(title = ''),
    )
    
    return fig
        


def scatgrap_profloss(data):
    sizes = np.absolute(data.profit_per_product)
    fig = px.scatter(data, x = 'profit_per_product',
                         color = 'Sub-Category',
                         size = sizes, hover_data = ['Sub-Category'])
    
    fig.update_layout(
        autosize = True,    
        height = 500,
        xaxis = dict(title = 'Profit/loss per Product'),
        yaxis = dict(title = ''),
    )
    
    return fig

    

def loss_grah():
    Sup_clean['loss'] = Sup_clean.Profit.apply(lambda x: x if (x < 0) else 0)
    
    fig = px.bar(Sup_clean, x = 'Ship Mode', y = 'loss', title = 'Losses in Each Shipping Category'.upper(),
                color = 'Ship Mode', hover_data = ['loss', 'Sub-Category'])
    
    fig.update_layout(
                autosize = True,
                width = 800,
                yaxis = dict(title = 'Total Loss'),
                xaxis = dict(title = 'Shipping Class'),
           )
    return fig


def dropdow():
     return html.Div([
          dbc.Card(
          dbc.CardBody([
                                   dcc.Dropdown(id='customer_type', 
                                                 # Update dropdown values using list comphrehension
                                                 options=[{
                                                        'label': i,
                                                        'value': i
                                                        } for i in Customer_option ],
                                                 placeholder="Select Product Sub Category", searchable = True , value = 'All Customers',
                                                 style={'font-size': '20px', 'text-align-last' : 'center','color':'#7570b3'})


          
          ])
          )
     ])

def drawTitle(title):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                                        html.Div(children=[html.Div(
                                        html.Div(html.H1(title, 
                                                                style={'textAlign':'center','color':'#7570b3','font-size':'48'}),)),                       

                                                                ],), 
            ])
        ),
    ])

        


def choropleth_fig():
       return  html.Div([
       dbc.Card(
       dbc.CardBody([
              dcc.Graph(figure = choropleth(),) 
       ])
       ),  
])


def choropleth2_fig():
       return  html.Div([
       dbc.Card(
       dbc.CardBody([
              dcc.Graph(figure=choropleth2(),) 
       ])
       ),  
])

def loss_fig():
       return  html.Div([
       dbc.Card(
       dbc.CardBody([
              dcc.Graph(figure=loss_grah(),) 
       ])
       ),  
])

def scatgrap_profprdt_fig():
       return  html.Div([
       dbc.Card(
       dbc.CardBody([
              dcc.Graph(id='plot1') 
       ])
       ),  
])

def scatgrap_profloss_fig():
       return  html.Div([
       dbc.Card(
       dbc.CardBody([
              dcc.Graph(id ='plot3',) 
       ])
       ),  
])

header = "SUPERSTORE PERFORMANCE"

     
# # Application layout
# Build App

app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    drawTitle(header)
                ], width=12),                
            ], align='center'),
            html.Br(),
            dbc.Row([
               dbc.Col([
                    loss_fig()
                ], width=12),
            ], align='center'), 
            html.Br(),            
            dbc.Row([
                dbc.Col([
                  choropleth2_fig() 
                ], width=6),
                dbc.Col([
                    choropleth_fig()
                ], width=6),
            ], align='center'),  
            html.Br(),
            dbc.Row([
               dbc.Col([
                    dropdow()
                ], width=6),
            ], align='center'), 
            html.Br(),            
            dbc.Row([
                dbc.Col([
                   scatgrap_profprdt_fig() 
                ], width=6),
                dbc.Col([
                    scatgrap_profloss_fig()
                ], width=6),
            ], align='center'),      
        ]), color = 'dark'
    )
])



@app.callback( [Output(component_id='plot1', component_property='figure'),
               Output(component_id='plot3',component_property='figure'),],
               [Input(component_id='customer_type', component_property='value'),],
              
              )

# Add computation to callback function and return graph
def get_graph(Customer_type):
       
       if Customer_type == "All Customers":
            
            Sup_cleans = Sup_cl.copy()
            scatgra_profprdt = scatgrap_profprdt(Sup_cl)
            scatgra_profloss = scatgrap_profloss(Sup_cl)
       else:
             Sup_cleans = Sup_cl[Sup_cl['Category'] == Customer_type]
             scatgra_profprdt = scatgrap_profprdt(Sup_cleans)
             scatgra_profloss = scatgrap_profloss(Sup_cleans)
              
       return scatgra_profprdt, scatgra_profloss





# Run the app
if __name__ == '__main__':
      app.run_server()



# import pandas as pd
# import numpy as np
# import dash
# import dash_html_components as html
# import dash_core_components as dcc
# from dash.dependencies import Input, Output, State
# import plotly.graph_objects as go
# import plotly.express as px
# from dash import no_update


# # Dash Application

# app = dash.Dash(__name__)


# server = app.server

# Sup_clean = pd.read_csv('Sup_clean1.csv')

# state_code = {'Kentucky': 'KY', 'California': 'CA', 'Florida': 'FL', 'North Carolina': 'NC',
#        'Washington': 'WA', 'Texas': 'TX', 'Wisconsin': 'WI', 'Utah': 'UT', 'Nebraska': 'NE',
#        'Pennsylvania': 'PA', 'Illinois': 'IL', 'Minnesota': 'MN', 'Michigan': 'MI', 'Delaware': 'DE',
#        'Indiana': 'IN', 'New York': 'NY', 'Arizona': 'AZ', 'Virginia': 'VA', 'Tennessee': 'TN',
#        'Alabama': 'AL', 'South Carolina': 'SC', 'Oregon': 'OR', 'Colorado': 'CO', 'Iowa': 'IA', 'Ohio': 'OH',
#        'Missouri': 'MO', 'Oklahoma': 'OK', 'New Mexico': 'NM', 'Louisiana': 'LA', 'Connecticut': 'CT',
#        'New Jersey': 'NJ', 'Massachusetts': 'MA', 'Georgia': 'GA', 'Nevada': 'NA', 'Rhode Island': 'RI',
#        'Mississippi': 'MS', 'Arkansas': 'AR', 'Montana': 'MT', 'New Hampshire': 'NH', 'Maryland': 'MD',
#        'District of Columbia': 'DC', 'Kansas': 'KS', 'Vermont': 'VT', 'Maine': 'ME',
#        'South Dakota': 'SD', 'Idaho': 'ID', 'North Dakota': 'ND', 'Wyoming': 'WY',
#        'West Virginia': 'WV'}

# Sup_clean['state_code'] = Sup_clean.State.apply(lambda X: state_code[X])

# state_data = Sup_clean[['Sales', 'Profit', 'state_code']].groupby('state_code').sum()

# def choropleth():
#     fig = go.Figure(data=go.Choropleth(
#       locations = state_data.index,
#       z = state_data.Sales,
#       locationmode = 'USA-states',
#       colorscale = 'Reds',
#       colorbar_title = 'Sales in USD',
#     ))

#     fig.update_layout(
#     title_text = 'Total State_Wise Sales',
#     geo_scope = 'usa',
#     height = 800,
#     )
    
#     return fig

# def choropleth2():
#     fig = go.Figure(data = go.Choropleth(
#     locations = state_data.index, # Spartial coordinates
#     z = state_data.Profit, #Data to be color-coded
#     locationmode = 'USA-states', # set of locations match entries i  ''
#     colorscale = [[0, 'rgb(255,0,0)'],[0.25, 'rgb(255,255,255)'], [0.45, 'rgb(124, 208, 247)'], [0.6, 'rgb(97,255,140)'],[1, 'rgb(8,181,0)']],
#     colorbar_title = 'Profit In USD',
    
#     ))


#     fig.update_layout(
#     title_text =' Total State Wise Profit/Loss',
#     geo_scope = 'usa',
#     height = 600,
#     )
#     return fig

# Sup_cl = pd.read_csv('SampleSuperstore.csv')
# Customer_option = Sup_cl['Category'].unique()
# print(Customer_option)
# Sup_cl['price_per_product'] = Sup_cl.Sales / Sup_cl.Quantity

# Sup_cl['profit_per_product'] = Sup_cl.Profit / Sup_cl.Quantity



# # data = Sup_clean.groupby(['Category'])

# def scatgrap_profprdt(data):
#     sizes = np.absolute(data.profit_per_product)
#     fig = px.scatter(data, x = 'price_per_product',
#                          color = 'Sub-Category',
#                          size = sizes, hover_data = ['Sub-Category'])
    
#     fig.update_layout(
#         autosize = True,    
#         height = 500,
#         xaxis = dict(title = 'Price per Product'),
#         yaxis = dict(title = ''),
#     )
    
#     return fig
        


# def scatgrap_profloss(data):
#     sizes = np.absolute(data.profit_per_product)
#     fig = px.scatter(data, x = 'profit_per_product',
#                          color = 'Sub-Category',
#                          size = sizes, hover_data = ['Sub-Category'])
    
#     fig.update_layout(
#         autosize = True,    
#         height = 500,
#         xaxis = dict(title = 'Profit/loss per Product'),
#         yaxis = dict(title = ''),
#     )
    
#     return fig

    

# def loss_grah():
#     Sup_clean['loss'] = Sup_clean.Profit.apply(lambda x: x if (x < 0) else 0)
    
#     fig = px.bar(Sup_clean, x = 'Ship Mode', y = 'loss', title = 'Losses in Each Shipping Category'.upper(),
#                 color = 'Ship Mode', hover_data = ['loss', 'Sub-Category'])
    
#     fig.update_layout(
#                 autosize = True,
#                 width = 800,
#                 yaxis = dict(title = 'Total Loss'),
#                 xaxis = dict(title = 'Shipping Class'),
#            )
#     return fig



     

# # Application layout
# app.layout = html.Div(children=[ 
#                                 # TASK1: Add title to the dashboard

#                                 html.H1('SUPERSTORE PERFORMANCE',style={'textAlign':'center','color':'#7570b3','font-size':'48'}),


         
         
#         html.Div(dcc.Graph(figure=loss_grah() ),
#                                                 style={"background-color": "#161A1D",
#                                                "padding": "60px",},),   
       
#         dcc.Dropdown(id='customer_type', 
#                                                      # Update dropdown values using list comphrehension
#                                    options=[{
#                                           'label': i,
#                                           'value': i
#                                           } for i in Customer_option ],
#                                    placeholder="Select Product Sub Category", searchable = True , value = 'All Customers',
#                                    style={'width':'50%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}), 
        
#         html.Div(children=[
                        
#                         html.Div(dcc.Graph(id = 'plot1', 
#                                                 style={"background-color": "#161A1D","text-align": "center",
#                                                 "height":"70vh"}),),
#                         html.Div(dcc.Graph(id = 'plot3',
#                                                 style={"background-color": "#161A1D","text-align": "center",
#                                                 "height":"70vh"}),),],
#                         style={"display": "flex","background-color": "#0e1012","padding-bottom": "60px","justify-content": "space-around"}),                                                                                # Create an outer division 
                            
#         html.Div(children=[
                        
#                         html.Div(dcc.Graph(figure=choropleth(), 
#                                                 style={"background-color": "#161A1D","text-align": "center",
#                                                 "height":"70vh"}),),
#                         html.Div(dcc.Graph(figure=choropleth2(),
#                                                 style={"background-color": "#161A1D","text-align": "center",
#                                                 "height":"70vh"}),),],
#                         style={"display": "flex","background-color": "#0e1012","padding-bottom": "60px","justify-content": "space-around"}),
                  
                    
#                                 # Graph layout
                               
#                                 # html.Div(dcc.Graph(figure=tree_fig)),
    
#                                 # html.Div([
#                                 #         html.Div(dcc.Graph( figure=bar_fig)),
#                                 #         html.Div(dcc.Graph(figure=pie_fig))
#                                 # ], style={'display': 'flex'}),
                                 
                                
                            
#                                 ],style={"height": "100vh"})


# @app.callback( [Output(component_id='plot1', component_property='figure'),
#                Output(component_id='plot3',component_property='figure'),],
#                [Input(component_id='customer_type', component_property='value'),],
              
#               )

# # Add computation to callback function and return graph
# def get_graph(Customer_type):
       
#        if Customer_type == "All Customers":
            
#             Sup_cleans = Sup_cl.copy()
#             scatgra_profprdt = scatgrap_profprdt(Sup_cl)
#             scatgra_profloss = scatgrap_profloss(Sup_cl)
#        else:
#              Sup_cleans = Sup_cl[Sup_cl['Category'] == Customer_type]
#              scatgra_profprdt = scatgrap_profprdt(Sup_cleans)
#              scatgra_profloss = scatgrap_profloss(Sup_cleans)
              
#        return scatgra_profprdt, scatgra_profloss





# # Run the app
# if __name__ == '__main__':
#       app.run_server()




