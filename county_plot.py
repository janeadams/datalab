import plotly.graph_objs as go
from ipywidgets import widgets

from network_files.graph_building import build_plotly_graph
from network_files.assemble_network import final_graph, pos, analysis, coloring_opts


TIMEOUT = 60

# print([{'label': i, 'value': i} for i in coloring_opts])

x_pos_node, y_pos_node, x_edges, y_edges, node_labels, node_coloring = build_plotly_graph(final_graph, \
    coloring_opts, analysis, pos)

metric_opts = widgets.Dropdown(
        description='rank_choice',
        options=[i for i in coloring_opts],
        value=coloring_opts[0]
    ) 
analysis_opts = widgets.RadioButtons(
        options = ['abs_dist', 'raw_dist'],
        #     {'label': 'Heterogeneity', 'value': 'abs_dist'},
        #     {'label': 'Difference', 'value': 'raw_dist'}                    
        # '],
        description ='Calculation',
        # options=[{'label': i, 'value': i} for i in coloring_opts],
        value='abs_dist'
    ) 
def colab_widget(analysis_opt, coloring_opt, x_pos_node, y_pos_node, x_edges, y_edges, node_labels, node_coloring):
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
                                color=node_coloring[analysis_opt[0]][coloring_opt[0]],
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

plotly_graph = colab_widget(analysis, coloring_opts, x_pos_node, y_pos_node, \
    x_edges, y_edges, node_labels, node_coloring)

option_box = widgets.HBox(children = [analysis_opts, metric_opts])

network = go.FigureWidget(data = plotly_graph['data'], layout = plotly_graph['layout'])


def response(change):

    network['data'][0]['marker']['color'] = \
        node_coloring[analysis_opts.value][metric_opts.value]

analysis_opts.observe(response, names = 'value')
metric_opts.observe(response, names = 'value')


final = widgets.VBox(children = [option_box,network])