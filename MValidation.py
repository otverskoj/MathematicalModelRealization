import numpy as np

# Период, на которое составляется расписание в часах
Range = 24

# Количество временных интервалов
N_times = 24

# Шаг дискретизации диспетчерского расписания
delta_t = Range / N_times

# Количество временных интервалов для расчёта временного интервала
N_tau = 60

# Шаг дискретизации временного интервала
delta_tau = delta_t / N_tau

# Структура производства
factory_struct = {
    "pipe": [6, 7, 8, 9, 10, 11, 12, 20, 21, 22, 23, 25, 26],
    "input": [0, 1, 2, 3, 4, 5],
    "pump": [],  # Что это????
    "tank": [13, 14, 15, 16, 17, 18, 19],
    "pipe_c": [],  # Что это????
    "tank_g": [27, 28, 29, 30],
    "stock": [31, 32]
}

N_inputs = len(factory_struct["input"])
N_stocks = len(factory_struct["stock"])
N_tanks_g = len(factory_struct["tank_g"])
N_pipes = len(factory_struct["pipe"])
N_tanks = len(factory_struct["tank"])

N_objects = N_inputs + N_stocks + N_tanks_g + N_pipes + N_tanks
N_all_tanks = N_tanks + N_tanks_g + N_stocks

# Двумерный массив связей между объектами
L = [(0, 6), (0, 7), (1, 8), (2, 9), (3, 10), (4, 11), (5, 12),
     (6, 13), (7, 14), (8, 15), (9, 19), (10, 16), (11, 17), (12, 18),
     (13, 20), (13, 21), (13, 22), (13, 23), (14, 20), (14, 21), (14, 22), (14, 23), (15, 20), (15, 21), (15, 22), (15, 23), (16, 20), (16, 21), (16, 22), (16, 23), (17, 20), (17, 21), (17, 22), (17, 23), (18, 20), (18, 21), (18, 22), (18, 23), (19, 20), (19, 21), (19, 22), (19, 23),
     (20, 24), (21, 24), (22, 24), (23, 24),
     (24, 25), (24, 26),
     (25, 27), (25, 28), (26, 29), (26, 30),
     (27, 31), (28, 31), (29, 32), (30, 32)]

# Количество связей между объектами
# FIX ME!!!
N_lines = len(L)

# Все объекты, являющиеся резервуарами
All_tanks = factory_struct["tank_g"] + factory_struct["tank"] + factory_struct["stock"]
print(All_tanks)
# Максимальная скорость потока между объектами
f_max = np.zeros((N_lines, N_times))

# Доля скорости потока от максимально возможной
x = np.zeros((N_lines, N_times))

# Скорость потока между объектами
f = np.zeros((N_lines, N_times))

# Поэлементное умножение
f = f_max * x
# Инициализирование массива f
for j in range(N_times):
  f[0][j] = 14.2
  f[1][j] = 14.2
  f[7][j] = 14.2
  f[8][j] = 14.2
  f[2][j] = 62
  f[9][j] = 62
  f[3][j] = 16.6
  f[10][j] = 16.6
  f[4][j] = 81.9
  f[11][j] = 81.9
  f[5][j] = 91.2
  f[12][j] = 91.2
  f[6][j] = 148.9
  f[13][j] = 148.9

for j in range(6, 16):
  f[14][j] = 0.7 #из 42 связи разделяем
  f[42][j] = 1.4
  f[18][j] = 0.7

  f[23][j] = 28.2
  f[43][j] = 28.2

  f[28][j] = 148.95
  f[32][j] = 148.95
  f[44][j] = 297.9

  f[37][j] = 152.5
  f[45][j] = 152.5

  f[46][j] = 480
  f[48][j] = 480

for j in range(16, 24):
  f[14][j] = 18
  f[42][j] = 18

  f[23][j] = 10.1
  f[39][j] = 10.1
  f[43][j] = 20.2

  f[28][j] = 146.7
  f[44][j] = 146.7

  f[33][j] = 32.55
  f[37][j] = 32.55
  f[45][j] = 65.1

  f[47][j] = 250
  f[50][j] = 250

for j in range(19, 24):
  f[52][j] = 960

# Множество пар связей, промежуточный объект которых является резервуаром
D = []

for i in range(len(L)):
    if L[i][1] in All_tanks:
        for j in range(i, len(L)):
            if L[i][1] == L[j][0]:
                D.append((i, j))

# Матрица остатков на конец t-го интервала времени в i-ом резервуаре
M = np.zeros((N_all_tanks, N_times))

M[0][0] = 580
M[1][0] = 789
M[2][0] = 632
M[3][0] = 689
M[4][0] = 124
M[5][0] = 206
M[6][0] = 750
M[7][0] = 820
M[8][0] = 200
M[9][0] = 1212
M[10][0] = 1212

## Количество имеющейся массы в 𝑖-м объекте (являющемся резервуаром) на конец 𝑡-го временного интервала:
## Для случая, когда один вход и несколько выходов
#for i in All_tanks:
#    for t in range(1, N_times):
#        total_out = 0
#        for item in D:
#            # Номер объекта на технологической схеме
#            obj = L[item[0]][1]
#            if obj == i:
#              need_connect = item
#              total_out += (f[item[1]][t] * delta_t)
#        M[All_tanks.index(i)][t] = (total_out + f[need_connect[0]][t])\
#        + M[All_tanks.index(i)][t - 1]

##print(M)
#print(D)

# Матрица максимальной массы остатков в i-ом резервуаре
M_max = [15000 for i in range(N_tanks + N_tanks_g)]

# Матрица минимальной массы остатков в i-ом резервуаре
M_min = [150 for i in range(N_tanks + N_tanks_g)]

# Ограничения по остаткам в резервуаре
stop = False
for t in range(N_times):
  for i in range(N_tanks + N_tanks_g):
    if M[i][t] > M_max[i] or M[i][t] < M_min[i]:
      stop = True
      i_stop = i
      t_stop = t

#if stop:
  #print("Выход за допустимые границы массы остатков")
  #print(i_stop)
  #print(t_stop)


# Массив максимальной пропускной способности в i-ой трубе
V_max = np.zeros(N_objects)
for i in range(N_objects):
    if i == 25:
        V_max[i] = 480
    elif i == 26:
        V_max[i] = 250
    V_max[i] = 500

# Массив минимальной пропускной способности в i-ой трубе
V_min = np.zeros(N_objects)

# Ограничения входящего и выходящего потока в объект
Summa_f_1 = 0; Summa_f_2 = 0
for t in range(N_times):
  for i in range(N_objects):
    for line in range(N_lines):
      if i == L[line][0]: #в номере связи первым объектом является рассматриваемый объект
        Summa_f_1 += f[line][t]
      if i == L[line][1]: #в номере связи вторым объектом является рассматриваемый объект
        Summa_f_2 += f[line][t]
    if (Summa_f_1 > V_max[i] or Summa_f_1 < V_min[i]) or (Summa_f_2 > V_max[i] or Summa_f_2 < V_min[i]):
      stop = True
      i_stop = i
      t_stop = t

#if stop:
  #print("Выход за допустимые границы пропускной способности")
  #print(i_stop)
  #print(t_stop)
q_f = 0; q_t = 0
# Количество имеющейся массы в 𝑖-м объекте (являющемся резервуаром) на конец 𝑡-го временного интервала:
# Для случая, когда один вход и несколько выходов
for i in All_tanks:
  for t in range(1, N_times):
      total_out = 0
      for item in D:
          # Номер объекта на технологической схеме
          obj = L[item[0]][1]
          if obj == i:
            need_connect = item
            total_out += (f[item[1]][t - 1] * delta_t)
      M[All_tanks.index(i)][t] = (f[need_connect[0]][t-1] - total_out)\
      + M[All_tanks.index(i)][t - 1]
      if t in range(6, 16) and i in range(16, 17):
        q_f += f[need_connect[0]][t-1]
        q_t += total_out
        print("f[need_connect[0]][t] = {}".format(f[need_connect[0]][t]))
        print("total_out = {}".format(total_out))
        print("M[All_tanks.index(i)][t] = {}".format(M[All_tanks.index(i)][t]))
        print("i = {}".format(i))
        print("t = {}".format(t))
print(q_f)
print(q_t)

print(M)
#15, 16
# Массив связей из L, в которых первый элемент является tank_g, а второй - stock
lines_gs = [line for line in L if (line[0] in factory_struct["tank_g"]) and (line[1] in factory_struct["stock"])]

M_task = [4800, 2000]
count_M_task = [0 for m in range(N_stocks)]
# В каждый пункт отгрузки должно быть поставлено заданное количество нефтепродукта
for s in range(N_stocks):
    for w in lines_gs:
        if w[1] == factory_struct["stock"][s]:
            for t in range(N_times):
                count_M_task[s] += f[L.index(w)][t]

# Проверка ограничения 5г
check = [M_task[s] == count_M_task[s] for s in range(N_stocks)]

for s in range(N_stocks):
  if check[s] == True:
    print("В {} пункт отгрузки было поставлено заданное количество нефтепродукта".format(factory_struct["stock"][s]))
  if check[s] == False:
    print("В {} пункт отгрузки не было поставлено заданное количество нефтепродукта!".format(factory_struct["stock"][s]))


# В товарном резервуаре номер 1 (27) на начало 23 часа остаток равен 1540, а не 580, как в таблице, потому что мы считаем остаток на начало часа, а не его конец, а в таблице представлен остаток на начала нулевого часа следующего дня, короче, все правильно работает
