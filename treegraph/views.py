from django.shortcuts import render
from django.db.models import Max

from .models import Nodes, TimeSettings, Edges
from .forms import NodeForm

from plotly.offline import plot
import plotly.graph_objs as go
import networkx as nx


def nodes_list(request):
    nodes = Nodes.objects.order_by('depth')
    settings_array = TimeSettings.objects.all()  # массив настроек времени

    # Детальный обзор + время на изучение уровней
    table = []  # таблица с данными о настройках времени
    count = 0
    for node in nodes:  # для каждого экземпляра вершины в списке вершин
        settings = []  # создаётся пустой массив settings
        actual_time = []  # создаётся пустой массив c текущим временем на изучение
        i = 0
        for setting in settings_array:  # для каждого экземпляра настройки в списке настроек (5 прогонов)
            sett = node.time_math(setting.id)
            settings.append(sett)  # в массив settings добавляется "на изучение уровня №"
            if count == 0:
                if node.lvl == 0:  # если нормативный уровень освоения равен 0
                    act_time = 0
                else:
                    act_time = sett[(node.lvl - 1)]['time']  # Время по нормативам (мин)
            elif node.lvl == 0:  # если нормативный уровень освоения равен 0
                tiham = table[count - 1]['actual_time'][i]
                act_time = tiham['act_t_h'] * 45 + tiham['act_t_m']  # Время по нормативам (мин)
            else:
                tiham = table[count - 1]['actual_time'][i]
                act_time = sett[(node.lvl - 1)]['time'] + tiham['act_t_h'] * 45 + tiham['act_t_m']  # Время по нормативам (мин)
            act = {'act_t_h': act_time // 45,  # добавление разбитого времени
                   'act_t_m': act_time % 45}
            actual_time.append(act)  # Время по нормативам (часы + минуты)
            i += 1
        row = {
            'node': node,  # Содержит название вершины
            'settings': settings,  # Сюда складывается список time_math со временем по каждому из уровней
            'actual_time': actual_time
        }
        table.append(row)
        count += 1

    # время на изучение по уровням  + настроек коэфициентов
    time_table = []  # список из экземпляров коэфф. времени и времени для освоения всего курса на заданный уровень
    for coefficients in settings_array:  # для каждого экземпляра таблицы коэффициентов (5 повторов)
        sum1 = sum2 = sum3 = sum4 = 0
        for node in nodes:  # для каждой вершины суммируем время на освоение всего курса на заданный уровень
            sum1 += int(node.time_math(coefficients.id)[0]['time'])
            sum2 += int(node.time_math(coefficients.id)[1]['time'])
            sum3 += int(node.time_math(coefficients.id)[2]['time'])
            sum4 += int(node.time_math(coefficients.id)[3]['time'])
        row = {  # создаём словарь из:
            'coefficients': coefficients,  # экземпляров коэффициентов времени
            'sum1': sum1 // 45,  # времени на освоение всего курса на заданный уровень (часы)
            'sum2': sum2 // 45,
            'sum3': sum3 // 45,
            'sum4': sum4 // 45,

            'sum1_m': sum1 % 45,  # времени на освоение всего курса на заданный уровень (минуты)
            'sum2_m': sum2 % 45,
            'sum3_m': sum3 % 45,
            'sum4_m': sum4 % 45,
        }
        time_table.append(row)

    #  Суммарное время на изучение по нормативам
    level_time_table = []
    for setting in settings_array:
        level_sum = 0
        for node in nodes:  #
            if node.lvl > 0:
                level_sum += int(node.time_math(setting.id)[(node.lvl-1)]['time'])
        row = {'level_sum_h': level_sum // 45,
               'level_sum_m': level_sum % 45}
        level_time_table.append(row)

    return render(request, 'treegraph/index.html', context={'table': table,
                                                            'time_settings': settings_array,
                                                            'time_table': time_table,
                                                            'level_time_table': level_time_table
                                                            })


def detail(request, Nodes_id):
    form = NodeForm()
    return render(request, 'treegraph/node_edit_old.html', context={'array': form})





# -------------------------------------------- make a tree graph -------------------------------------------------------
max_depth = Nodes.objects.all().aggregate(Max('depth'))['depth__max']
counter = [0]
for i in range(max_depth):  # забиваем список необходимым количеством нулей
    counter.append(0)
for node in Nodes.objects.order_by('depth'):  # считаем количество вершин на каждом из уровней глубины
    i = node.depth
    counter.insert(i, counter.pop(i)+1)
print(counter)

G = nx.Graph()
for edge in Edges.objects.all():
    G.add_edges_from([(edge.parent, edge.child)])  # добавляем грань в граф

y = 0
flag = 0
for node in Nodes.objects.order_by('depth'):
    if flag != counter[node.depth]:
        y = 0
    y += max(counter) / (counter[node.depth] + 1)
    x = node.depth
    G.add_nodes_from([node], pos=[x, y])
    flag = counter[node.depth]

    # neighbours = node.edges_set.count()  # кол-ви детей у вершины
# print(nx.get_node_attributes(G, 'pos'))

# Create Edges
edge_trace = go.Scatter(x=[], y=[], mode='lines', opacity=0.30, hoverinfo='none',
                        line=dict(width=1.8, color='#000000', shape='spline', smoothing=1.3))


for edge in G.edges():
    x0, y0 = G.node[edge[0]]['pos']
    x1, y1 = G.node[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(x=[], y=[], mode='markers+text', opacity=0.90, hoverinfo='text', text=[], textfont=dict(size=14),
                        textposition='middle center', marker=dict(color='#1EB746', size=11, line=dict(width=1)))

for node in G.nodes():
    x, y = G.node[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])

# Color Node Points
for node in G.node:
    node_trace['text'] += tuple([node])

# Create Network Graph
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(title='<br>Дерево знаний',
                                 titlefont=dict(size=24),
                                 showlegend=False,
                                 hovermode='closest',
                                 margin=dict(b=20, l=25, r=5, t=35),
                                 xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                 yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))


def graph(request):
    plot(fig, filename='treegraph/templates/treegraph/networkx.html', auto_open=False)
    return render(request, 'treegraph/networkx.html')
