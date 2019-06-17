from plotly.offline import plot
import plotly.graph_objs as go
import networkx as nx


G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5)])


G.add_nodes_from([1], pos=[0.0, 0.0])
G.add_nodes_from([2], pos=[0.1, 0.2])
G.add_nodes_from([3], pos=[0.1, -0.2])
G.add_nodes_from([4], pos=[0.2, 0.4])
G.add_nodes_from([5], pos=[0.2, -0.2])

pos = nx.get_node_attributes(G, 'pos')
print(pos)
print(G.node)
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

edge_trace = go.Scatter(x=[], y=[], line=dict(width=5.5, color='#888', shape='spline', smoothing=1.3), hoverinfo='none', mode='lines')

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
                xaxis=dict(showgrid=True, zeroline=True, showticklabels=True),
                yaxis=dict(showgrid=True, zeroline=True, showticklabels=True)))

plot(fig, filename='networkx.html', auto_open=False)





'''
Эта штука нужна что бы располагать вершины в графе относительно своих братьев

neighbour = [2]
for edge in Edges.objects.all():
    G.add_edges_from([(edge.parent, edge.child)])  # добавляем грань в граф
    neighbour.append(edge.parent.edges_set.count() + 1)  # добавляем для каждой вершины кол-во её братьев
    # print(edge.child, ' - ', edge.parent.edges_set.count() + 1)
# print(neighbour)

count = 0
y = 0
for node in Nodes.objects.order_by('depth'):
    x = node.depth
    divider = 10000/neighbour[count]
    if neighbour[count] != neighbour[count-1] or count == 0:
        y = divider
        G.add_nodes_from([node], pos=[x, y])
    else:
        y += divider
        G.add_nodes_from([node], pos=[x, y])
    # neighbours = node.edges_set.count()  # кол-ви детей у вершины
    count += 1
'''
