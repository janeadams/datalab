import math

import networkx as nx
import matplotlib.pyplot as plt

import plotly.graph_objs as go

import matplotlib.pyplot as plt

import numpy as np

def get_graph_positions(G, layout = 'kamadi'):
    if layout == 'spring':
        pos = nx.spring_layout(G, k = 0.5)
    elif layout == 'planar':
        pos = nx.circular_layout(G)
        # nx.planar_layout()
    else:
        pos = nx.kamada_kawai_layout(G)
    return pos


def build_plotly_graph(G, coloring_options, analysis, pos = None, num_dim = 2, layout = 'kamadi'):

    if pos is None:
        pos = get_graph_positions(G, layout)
    
    x_pos_node = []
    y_pos_node = []
    z_pos_node = []
    node_labels = []
    node_coloring = {}
    for a in analysis:
        node_coloring[a] = {}
        for option in coloring_options:
            node_coloring[a][option] = []

    x_edges = []
    y_edges = []
    z_pos_edges = []


    for node in G.nodes():
        # This should give the x and y coordinates for the nodes, by iterating through the position
        # object returned
        x_pos_node.append(pos[node][0]) 
        y_pos_node.append(pos[node][1] )
        node_labels.append(node)
        for a in analysis:
            for option in coloring_options:
                
                node_coloring[a][option].append(G.nodes[node].get('{}_{}'.format(a, option), 0))
        if num_dim > 2:
            z_pos_node.append(pos[node][2])

    for edge in G.edges():
        try:
            x_edges.append(pos[edge[0]][0])
            x_edges.append(pos[edge[1]][0])
            y_edges.append(pos[edge[0]][1])
            y_edges.append(pos[edge[1]][1])
            if num_dim > 2:
                z_pos_edges.append([pos[G.edges[edge]['source']][2], pos[G.edges[edge]['target']][2], None])
            

        except KeyError:
            continue

    
    # plot_data = update_graph(x_pos_node, y_pos_node, x_edges, y_edges, node_labels, node_coloring, coloring_options[0])

    return x_pos_node, y_pos_node, x_edges, y_edges, node_labels, node_coloring


def update_graph(x_loc, y_loc, x_edges, y_edges, labels, coloring, coloring_opt):
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
    
    node_trace = go.Scatter(x=x_loc,
                y=y_loc,
                mode='markers+text',
                name='actors',
                marker=dict(symbol='circle',
                                size=3,
                                color=coloring[coloring_opt],
                                colorscale='Bluered_r',
                                line=dict(color='rgb(50,50,50)', width=0.5)
                                ),
                hoverinfo='text',
                hovertext = labels
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



def write_pos_tofile(pos, filename):
    fout = open("data/{}.txt".format(filename), 'w')
    for county in pos:
        fout.write("{}\t{}\t{}\n".format(county, pos[county][0], pos[county][1]))
    fout.close()


def read_in_pos_file(filename):
    fin = open("data/{}.txt".format(filename), 'r')
    pos = {}
    for line in fin:
        split_line = line.rstrip().split('\t')
        pos[split_line[0]] = split_line[1:]
    return pos

