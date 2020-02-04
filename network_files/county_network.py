

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re



def get_county_data():
    county_data = pd.read_csv("data/CountyData.tsv", sep= '\t')
    return county_data


def read_county_edgelist(filename):
    fin = open(filename, 'r')
    new_edgelist = []
    for line in fin.readlines():
        split_line = line.rstrip().replace(",", "").split(" ")
        edge = ["{}, {}".format(clean_line(split_line[0]), split_line[1].replace("_", " ")),
         "{}, {}".format(clean_line(split_line[2]), split_line[3].replace("_", " "))]
        new_edgelist.append(edge)
    return new_edgelist

def clean_line(string_line):
    str_repl = re.compile("|".join([
    " Census Area",
    " Borough",
    " Parish", 
    " Municipality"]))
    string_line = string_line.rstrip().replace(",", "").replace("_", " ")
    
    return str_repl.sub(lambda m: "", string_line)


def assign_rank_to_nodes(g, county_data):
    ignored_counties = []
    for node in g.nodes():
        county_rankings = county_data.loc[county_data['County'].str.lower() == node.lower()]
        if county_rankings.shape[0] == 1:
            g.nodes[node]['rank'] = county_rankings['rank'].astype(int).values[0]
            g.nodes[node]['education'] =  county_rankings['education'].astype(float).values[0]
            g.nodes[node]['income'] =  county_rankings['income'].astype(float).values[0]
            g.nodes[node]['unemployment'] = county_rankings['unemployment'].astype(float).values[0]
            g.nodes[node]['diability'] =  county_rankings['disability'].astype(float).values[0]
            g.nodes[node]['life'] =  county_rankings['life'].astype(float).values[0]
            g.nodes[node]['obesity'] =  county_rankings['obesity'].astype(float).values[0]
        else:
            ignored_counties.append(node)
    return g, ignored_counties
    

def read_in_rankings():
    """
    Read in the rankings brought in from the Data Lab Channel 
    """
    fin = open("data/CountyData.tsv", 'r')
    for line in fin.readlines()[1:]:
        split_line = line.rstrip().split('\t')
        split_line[0] = fix_abbreviation(split_line[0], state_abv)
        break
        

def measure_neighbors(g, metric, method):
    for county in nx.generate_adjlist(g, delimiter= "|"):
        split_county = county.split("|")
        if g.nodes[split_county[0]].get(metric, -1) > 0:
            neighbor_metrics = [g.nodes[neighbor].get(metric, None) for neighbor in split_county[1:]]
            if method == 'abs_dist':
                neighbor_metrics = [abs(g.nodes[split_county[0]][metric] - \
                    neighbor_value) for neighbor_value in filter(None, neighbor_metrics)]
            elif method == 'raw_dist':
                # neighbor_metrics = []
                neighbor_metrics = [g.nodes[split_county[0]][metric] - \
                    neighbor_value for neighbor_value in filter(None, neighbor_metrics)]
            g.nodes[split_county[0]]['{}_{}'.format(method, metric)] = sum(neighbor_metrics)/len(neighbor_metrics)
    return g