import math

def dist_calc(origin, target):
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

a = [44.929071, 26.024663]
b = [44.969132, 26.068413]

print(dist_calc(a, b))
