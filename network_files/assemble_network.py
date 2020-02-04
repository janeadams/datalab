import networkx as nx

from network_files.county_network import read_county_edgelist, assign_rank_to_nodes, get_county_data, measure_neighbors
from network_files.graph_building import build_plotly_graph, read_in_pos_file, get_graph_positions

new_file = True
new_plot = False

analysis = ["abs_dist", 'raw_dist']
coloring_opts = ['rank', 'education', 'income', 'unemployment',
       'disability', 'life', 'obesity']


if new_file:
    county_data = get_county_data().replace("No Data", None)
    county_edgelist = read_county_edgelist("data/CountyNetworkEdgeList.txt")
    edge_graph = nx.from_edgelist(county_edgelist)
    final_graph, ignored = assign_rank_to_nodes(edge_graph, county_data)
    for a in analysis:
        for opts in coloring_opts:
            final_graph = measure_neighbors(final_graph, opts, a)
else:
    final_graph = nx.read_adjlist('data/county_network.adjlist')

if new_plot:
    # p_graph = build_plotly_graph(final_graph, layout = "kamadi")
    pos = get_graph_positions(final_graph, layout='spring')
else:
    pos = read_in_pos_file('county_network_positions')
    # print(final_graph.nodes)
