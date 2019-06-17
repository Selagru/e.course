from django.db import models


class TimeSettings(models.Model):
    t_alpha = models.FloatField("время на восприятие одного понятия", default=2, max_length=4)
    k_knowledge = models.FloatField("коэффициент усложнения при создании связей", default=2, max_length=4)
    k_practise = models.FloatField("коэффициент усложнения при практическом освоении умения", default=4, max_length=4)
    k_skill = models.FloatField("коэффициент усложнения при приобретении навыка", default=8, max_length=4)

    def __str__(self):
        return "Коэффициенты временных затрат № %d" % self.pk


class Nodes(models.Model):  # Вершина графа
    name = models.CharField("Название понятия", max_length=100)  # Имя вершины
    depth = models.IntegerField("Глубина расположения вершины", default=0, editable=False)
    lvl = models.IntegerField("Нормативный уровень освоения", default=3)

    def time_math(self, pk=1):
        if self.edges_set.count() == 0:  # - кол-во потомков данной вершины(UPD)И ЭТАПОВ ИЗУЧАЕМОГО ПРЕДМЕТА.
            p_child_stage = 5
        else:
            p_child_stage = self.edges_set.count()
            # p_stage = self.p_stage()  # кол-во этапов изучаемого предмета(Кол-во вершин или всё же lvl)

        ts = TimeSettings.objects.get(pk=pk)  # переменные из экземпляра класса TimeSettings

        time1 = ts.t_alpha + p_child_stage * ts.k_knowledge * ts.t_alpha  # время на усвоение понятия
        time2 = p_child_stage * (ts.t_alpha + ts.k_knowledge * ts.t_alpha)  # время на усвоение знаний о способе действий
        time3 = time2 * ts.k_practise  # время на формирование умения
        time4 = time2 * ts.k_skill  # время на формирование навыка

        lvl1 = round(time1)
        lvl2 = round(time2 + lvl1)
        lvl3 = round(time3 + lvl2)
        lvl4 = round(time4 + lvl3)

        return [{"string": 'Изучение уровня 1:', "time": lvl1, "time_h": (lvl1 // 45), "time_m": (lvl1 % 45)},
                {"string": 'Изучение уровня 2:', "time": lvl2, "time_h": (lvl2 // 45), "time_m": (lvl2 % 45)},
                {"string": 'Изучение уровня 3:', "time": lvl3, "time_h": (lvl3 // 45), "time_m": (lvl3 % 45)},
                {"string": 'Изучение уровня 4:', "time": lvl4, "time_h": (lvl4 // 45), "time_m": (lvl4 % 45)}]

    def __str__(self):
        return self.name


class Edges(models.Model):  # Грань графа
    parent = models.ForeignKey(Nodes, verbose_name="Вершина-родитель", on_delete=models.CASCADE,)
    child = models.OneToOneField(Nodes, verbose_name="Вершина-потомок", on_delete=models.CASCADE,
                                 related_name='child_of')

    def save(self, *args, **kwargs):  # переопределил save для автоматического высчитывания глубины расположения вершины
        self.child.depth = self.parent.depth + 1
        self.child.save()
        print('save() is called.')
        super().save(*args, **kwargs)

    def __str__(self):
        return "Понятие '%s' раскрывается через понятие '%s'" % (self.parent.name, self.child.name)
