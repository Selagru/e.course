from django.shortcuts import render

from .models import Nodes, Edges, TimeSettings
from .forms import NodeForm


# Create your views here.


def nodes_list(request):
    nodes = Nodes.objects.order_by('lvl')
    settings_array = TimeSettings.objects.all()  # массив настроек времени
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

    return render(request, 'treegraph/index.html', context={'nodes': nodes,
                                                            'table': table,
                                                            'time_settings': settings_array})


def detail(request, Nodes_id):
    form = NodeForm()

    return render(request, 'treegraph/node_edit_old.html', context={'array': form})
