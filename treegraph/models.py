from django.db import models


class TimeSettings(models.Model):
    t_alpha = models.IntegerField("время на восприятие одного понятия", default=2)
    k_knowledge = models.IntegerField("коэффициент усложнения при создании связей", default=2)
    k_practise = models.IntegerField("коэффициент усложнения при практическом освоении умения", default=4)
    k_skill = models.IntegerField("коэффициент усложнения при приобретении навыка", default=8)

    def __str__(self):
        return "Коэффициенты временных затрат № %d" % self.pk


class Nodes(models.Model):  # Вершина графа

    name = models.CharField("Название понятия", max_length=100)  # Имя вершины
    lvl = models.IntegerField("Этап изучаемого предмета", default=0)  # Уровень освоения

    def __str__(self):
        return self.name

    def time_math(self, pk=1):
        p_child = self.edges_set.count()  # - кол-во потомков данной вершины
        p_stage = self.lvl  # кол-во этапов изучаемого предмета(Кол-во вершин или всё же lvl)

        ts = TimeSettings.objects.get(pk=pk)  # переменные из экземпляра класса TimeSettings

        time1 = ts.t_alpha + p_child * ts.k_knowledge * ts.t_alpha  # время на усвоение понятия
        time2 = p_stage * (ts.t_alpha + ts.k_knowledge * ts.t_alpha)  # время на усвоение знаний о способе действий
        time3 = time2 * ts.k_practise  # время на формирование умения
        time4 = time2 * ts.k_skill  # время на формирование навыка

        lvl1 = time1
        lvl2 = time2 + lvl1
        lvl3 = time3 + lvl2
        lvl4 = time4 + lvl3

        return [{"string": 'Минут для освоения уровня 1', "time": lvl1}, {"string": 'Минут для освоения уровня 2', "time": lvl2},
                {"string": 'Минут для освоения уровня 3', "time": lvl3}, {"string": 'Минут для освоения уровня 4', "time": lvl4}]


class Edges(models.Model):  # Грань графа
    parent = models.ForeignKey(Nodes, verbose_name="Вершина-родитель", on_delete=models.CASCADE)
    child = models.OneToOneField(Nodes, verbose_name="Вершина-потомок", on_delete=models.CASCADE,
                                 related_name='child_of')

    def __str__(self):
        return "Понятие '%s' раскрывается через понятие '%s'" % (self.parent.name, self.child.name)







'''from plotly.offline import plot
import plotly.graph_objs as go

import networkx as nx

G = nx.random_geometric_graph(50, 0.25)
pos = nx.get_node_attributes(G, 'pos')

dmin = 1
ncenter = 0
for n in pos:
    x, y = pos[n]
    d = (x-0.5)**2+(y-0.5)**2
    if d < dmin:
        ncenter = n
        dmin = d

p = nx.single_source_shortest_path_length(G, ncenter)


edge_trace = go.Scatter(x=[], y=[], line=dict(width=0.5,color='#888'), hoverinfo='none', mode='lines')

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
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='Electric',
        reversescale=True,
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


for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['color']+=tuple([len(adjacencies[1])])
    node_info = '# of connections: '+str(len(adjacencies[1]))
    node_trace['text']+=tuple([node_info])


fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[dict(
                    text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002)],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

plot(fig, filename='networkx.html')'''