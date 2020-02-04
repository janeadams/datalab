import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from flask_caching import Cache

from network_files.graph_building import build_plotly_graph
from network_files.assemble_network import final_graph, pos, analysis, coloring_opts

TIMEOUT = 60

x_pos_node, y_pos_node, x_edges, y_edges, node_labels, node_coloring = build_plotly_graph(final_graph, coloring_opts, analysis, pos)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(external_stylesheets = external_stylesheets)

cache = Cache(app.server, config = {
    'CACHE_TYPE': 'filesystem', 
    'CACHE_DIR' : 'cache'
})


app.layout = html.Div([
        html.Div([
            dcc.Graph(
        id='county_network',
        style={
            'width': '99%',
            'position': 'absolute'}
        ),  
        html.Div([
            dcc.Dropdown(
                id='rank_choice',
                options=[{'label': i, 'value': i} for i in coloring_opts],
                value=coloring_opts[0]
            ), 
            dcc.RadioItems(
                options = [
                    {'label': 'Heterogeneity', 'value': 'abs_dist'},
                    {'label': 'Difference', 'value': 'raw_dist'}                    
                ],
                id='calc_choice',
                # options=[{'label': i, 'value': i} for i in coloring_opts],
                value='abs_dist'
            )], 
        style = {
            'display' : 'inline-block',
            'position' : 'relative',
            'top' : 0, 
            'left': 0, 
            'width': '20%'
        })],
        )])


@app.callback(
    dash.dependencies.Output('county_network', 'figure'),
    [dash.dependencies.Input('calc_choice', 'value'), 
    dash.dependencies.Input('rank_choice', 'value')])
@cache.memoize(timeout = TIMEOUT)
def update_plotly_graph(analysis_opt, coloring_opt):
    edge_trace = go.Scatter(x=x_edges,
            y=y_edges,
            mode='lines',
            # color = line_colors[idx],
            line=dict(color= 'gray', width = 0.2),
            hoverinfo='none'
            )

    """
    These are for drawing the nodes
    """
    
    node_trace = go.Scatter(x=x_pos_node,
                y=y_pos_node,
                mode='markers+text',
                name='actors',
                marker=dict(symbol='circle',
                                size=3,
                                color=node_coloring[analysis_opt][coloring_opt],
                                colorscale='Bluered_r',
                                line=dict(color='rgb(50,50,50)', width=0.5)
                                ),
                hoverinfo='text',
                hovertext = node_labels
                )


    axis=dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
            )
    
    layout = go.Layout(
            # title="Title Goes here",
            # width=720,
            # height=480,
            showlegend=False,
            xaxis = dict(
                showgrid = False, 
                zeroline = False,
                showticklabels=False
            ),
            yaxis = dict(
                showgrid = False, 
                zeroline = False,
                showticklabels=False
            ),
            plot_bgcolor='white',
            scene=dict(
                xaxis=dict(axis),
                yaxis=dict(axis)#,
            ),

        bargroupgap=0.3,
        hovermode='closest'#,
    )
    return {'data' : [node_trace, edge_trace], 'layout' : layout}