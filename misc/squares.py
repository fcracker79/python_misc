import math
import typing


def var(x: typing.Sequence[float]) -> float:
    avg = sum(x) / len(x)
    return sum(map(lambda d: d * d, map(lambda d: d - avg, x))) / len(x)


def dev(*a) -> float:
    return math.sqrt(var(*a))


print(dev((4, 6, 8, 6)))
print(var((4, 6, 8, 6)))
