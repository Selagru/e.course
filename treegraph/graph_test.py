'''import networkx as nx


G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5)])
for n in G.nodes:
    G.add_nodes_from([n], pos=[n+1, n+2])
print(G.node[1])
print(G.nodes)
print(G.edges)
pos = nx.get_node_attributes(G, 'pos')
print(pos)'''












from plotly.offline import plot
import plotly.graph_objs as go

import networkx as nx

G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5)])


G.add_nodes_from([1], pos=[0.3, 0.3])
G.add_nodes_from([2], pos=[0.4, 0.2])
G.add_nodes_from([3], pos=[0.4, 0.4])
G.add_nodes_from([4], pos=[0.5, 0.1])
G.add_nodes_from([5], pos=[0.5, 0.3])

pos = nx.get_node_attributes(G, 'pos')
print(pos)

dmin = 1
ncenter = 0
for n in pos:
    x, y = pos[n]
    d = (x-0.5)**2+(y-0.5)**2
    if d < dmin:
        ncenter = n
        dmin = d

p = nx.single_source_shortest_path_length(G, ncenter)

# Create Edges

edge_trace = go.Scatter(x=[], y=[], line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')

for edge in G.edges():
    x0, y0 = G.node[edge[0]]['pos']
    x1, y1 = G.node[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=False,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='Earth',
        reversescale=False,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

for node in G.nodes():
    x, y = G.node[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])

# Color Node Points

for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['color']+=tuple([len(adjacencies[1])])
    node_info = '# of connections: '+str(len(adjacencies[1]))
    node_trace['text']+=tuple([node_info])

# Create Network Graph

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[dict(
                    text='',
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002)],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

plot(fig, filename='templates/treegraph/networkx.html')
