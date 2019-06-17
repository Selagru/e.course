from django.test import TestCase

# Create your tests here.


#from django.db import models

#help(models)

c = []

row = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
}
for i in range(4):
    c.append(row)
print(c[2]['three'])
print()
print(len(c))


def sum(n):
    if n == 1:
        return c[n-1]['four']
    else:
        return c[n-1]['four'] + sum(n - 1)


print(sum(len(c)))




if count > 0:
    for i in range(4):
        pass
        tiham = table[count]['actual_time'][i]
        tiham2 = table[count - 1]['actual_time'][i]
        h = (tiham['act_t_h'] + tiham2['act_t_h']) * 45
        m = tiham['act_t_m'] + tiham2['act_t_m']
        z = h + m
        count_list.append(z)
        print(count_list[i])
    print(count_list)

