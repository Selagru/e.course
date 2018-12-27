from django.shortcuts import render

from .models import Nodes, Levels, TimeSettings
from .forms import NodeForm


# Create your views here.


def nodes_list(request):
    nodes = Nodes.objects.order_by('lvl')
    settings_array = TimeSettings.objects.all()  # массив настроек времени
    levels = Levels.objects.all()

    table = []  # таблица с данными о настройках времени
    for node in nodes:  # для каждого экземпляра вершины в списке вершин
        settings = []  # создаётся пустой массив settings

        for setting in settings_array:  # для каждого экземпляра настройки в списке настроек
            settings.append(node.time_math(setting.id))  # в массив settings добавляется
        row = {
            'node': node,
            'settings': settings
        }
        table.append(row)  #

    time_table = []
    for setting in settings_array:
        sum1 = sum2 = sum3 = sum4 = 0
        for node in nodes:
            sum1 += int(node.time_math(setting.id)[0]['time'])
            sum2 += int(node.time_math(setting.id)[1]['time'])
            sum3 += int(node.time_math(setting.id)[2]['time'])
            sum4 += int(node.time_math(setting.id)[3]['time'])
        row = {
            'setting': setting,
            'sum1': sum1,
            'sum2': sum2,
            'sum3': sum3,
            'sum4': sum4,
        }
        time_table.append(row)

    level_time_table = []
    for setting in settings_array:
        level_sum = 0
        for lvl in levels:
            if lvl.level > 0:
                level_sum += int(lvl.node_id.time_math(setting.id)[(lvl.level-1)]['time'])
                #print(lvl.level)
        row = {'level_sum': level_sum}
        level_time_table.append(row)

    return render(request, 'treegraph/index.html', context={'table': table,
                                                            'time_settings': settings_array,
                                                            'time_table': time_table,
                                                            'level_time_table': level_time_table},)


def detail(request, Nodes_id):
    form = NodeForm()

    return render(request, 'treegraph/node_edit_old.html', context={'array': form})


def graph(request):
    return render(request, 'treegraph/networkx.html')
