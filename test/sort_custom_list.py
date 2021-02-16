x = ['Wed', 'Thurs', 'Mon']
# y = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
# z = [0, 1, 2, 3, 4, 5, 6]

intToDate = {0: 'Mon', 1: 'Tues', 2: 'Wed', 3: 'Thurs', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
dateToInt = {'Mon': 0, 'Tues': 1, 'Wed': 2, 'Thurs': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}

y = sorted(list(map(lambda y: dateToInt[y], x)))
z = list(map(lambda x: intToDate[x], y))
print(z)
