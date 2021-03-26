# I'm blue, if I were green I would die

import math
import numpy as np
import random


def dist_calc(origin, target):
    '''
    origin is a tuple with the logitude and latitude of the origin location in degrees (lat, long)
    target is a tuple with the logitude and latitude of the target location in degrees (lat, long)
    '''
    R = 6371e3  # Earth radius [m]

    phi1 = origin[0] * math.pi / 180
    phi2 = target[0] * math.pi / 180
    dphi = (target[0] - origin[0]) * math.pi / 180
    dlambda = (target[1] - origin[1]) * math.pi / 180

    a = math.sin(dphi / 2) * math.sin(dphi / 2) + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) * math.sin(
        dlambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    d = R * c  # [m]

    return d


def constr_dist_matrix(IATA_lst, coord_lst):
    n = len(IATA_lst)
    a = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                a[i][j] = a[j][i] = dist_calc(coord_lst[i], coord_lst[j])
    return a


def init_population(population_size):
    population = np.zeros((population_size, len(IATA_lst)))
    for j in range(population_size):
        cities_left = IATA_lst.copy()
        for k in range(len(IATA_lst)):
            if k == 0:
                population[j][k] = 0
                cities_left.remove('ROO')
            else:
                next_city = random.choice(cities_left)
                cities_left.remove(next_city)
                population[j][k] = IATA_lst.index(next_city)
    return population


def dist_route(population):
    dist_matrix = constr_dist_matrix(IATA_lst, coord_lst)
    dist_lst = []
    total_dist = []
    for i in range(len(population)):
        dist = []
        for j in range(len(population[i])):
            if j == 0:
                dist_city = 0
            else:
                dist_city = dist_matrix[int(population[i][j-1])][int(population[i][j])]
                dist.append(dist_city)
                dist.append(dist_matrix[int(population[i][j])][int(population[i][0])])
        dist_lst.append(sum(dist))

    total_dist = sum(dist_lst)
    return dist_lst, total_dist

def population_ranking(population, distances):
    for i in range(len(distances) - 1):
        for j in range(i + 1, len(distances)):
            if distances[i] > distances[j]:
                a = distances[i]
                distances[i] = distances[j]
                distances[j] = a
                b = population[i]
                population[i] = population[j]
                population[j] = b
    return population, distances

def swap_cities(population):
    for i in range(population):
        for j in range(population[i]):
            a, b = random.randint(1,len(population[i])), random.randint(1,len(population[i]))
            if a != b:
                population[i][b], population[i][a] = population[i][a], population[i][b]
            else:
                None
    return population


def breeding(parent1, parent2):
    child = []
    startCut = random.randint(0, len(parent2) - 1)
    endCut = random.randint(startCut + 1, len(parent2))
    cut2 = parent2[startCut:endCut]
    '''
    j = 0
    for i in range(len(parent1)):
        if parent1[i] not in cut2:
            child.append(parent1[i])
            j += 1
        if j == startCut:
            break
    child.extend(cut2)
    for k in range(i + 1, len(parent1)):
        if parent1[i] not in cut2:
            child.append(parent1[i])
    '''
    i = j = k = 0
    while k < len(parent1):
        if k < startCut or k >= endCut:
            if parent1[i] not in cut2:
                child.append(parent1[i])
                k += 1
            i += 1
        else:
            child.extend(cut2)
            k += len(cut2)
    print(f"cut2 is {cut2}")
    print(f"startCut is {startCut}")
    print(f"endCut is {endCut}")
    return np.array(child)


IATA_lst = ["ROO", "AMS", "ANR", "BRU", "CRL", "DHR", "EIN", "ENS", "GLZ", "GRQ", "KJK", "LEY", "LGG", "LID", "LUX",
            "LWR", "MST", "OBL", "OST", "RTM", "UDE", "UTC", "WOE"]
coord_lst = [(51.535849, 4.4653213), (52.308056, 4.764167), (51.1893997192, 4.46027994156), (50.9008, 4.4840),
             (50.455998176, 4.45166486), (52.9234008789063, 4.78062009811401),
             (51.4499982, 5.371331848), (52.27166666, 6.87833333), (51.5672222222, 4.9316666667), (53.1273, 6.58249),
             (50.817, 3.20578), (52.4544444444, 5.5244444444), (50.6375, 5.44333), (52.1697, 4.4261),
             (49.628899, 6.214745), (53.2286, 5.76056), (50.9175, 5.7755), (51.264722000000, 4.75333300),
             (51.1988983154, 2.8622200489), (51.95694, 4.43722), (51.6544444444, 5.6861111111),
             (52.1294, 5.27258), (51.4491, 4.34203)]

'''
test1 = (51.535849, 4.4653213)
test2 = (52.308056, 4.764167)
print(dist_calc)
'''
print(constr_dist_matrix(IATA_lst, coord_lst))


# iterations = 10
population_size = 4
# distance_his = []
# current_best = []

population = init_population(population_size)
distances, total_dist = dist_route(population)
print(distances,total_dist)
population, distances = population_ranking(population, distances)


parent1 = np.array([0, 1, 2, 3, 4, 5, 6, 7])
parent2 = np.array([7, 6, 2, 1, 3, 0, 5, 4])
child = breeding(parent1, parent2)
print(child)
