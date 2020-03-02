from math import log, exp
from time import time

t = time()

length = 90

max_ups = int(length / (1 + log(3) / log(2)))
small_ratio = exp(log(2) - max((i * log(3)) % log(2) for i in range(max_ups + 1)))
max_min = int(1 / (3 * (pow(small_ratio, 1 / max_ups) - 1)))


def collatz(x):
    if x % 2 == 0:
        return x // 2
    return 3 * x + 1


def collatz2(i, f):
    if i % 2 == 0:
        return i // 2, f / 2
    return 3 * i + 1, 3 * f


def collatz_sequence(x):
    l = []
    while (x > 1):
        l.append(x)
        x = collatz(x)
    while len(l) >= 2 and l[-2] > l[-1]:
        l = l[:-1]
    return l[:-1]


def check_bad_1(start, end):
    assert (start < end)
    i, f = start, start
    while i != end:
        i, f = collatz2(i, f)
        assert (i > 1)
    return start > f


def check_bad_2(start, end, minimum):
    x = start
    while x > minimum:
        x = collatz(x)
        if x == minimum:
            return check_bad_1(start, end)
    return False


bad = []


def get_all_bad():
    for minimum in range(2, max_min + 1):
        for end in collatz_sequence(minimum)[1:]:
            if end < minimum:
                break
            for start in range(int(end * pow(1 + minimum / 3, -max_ups)), end):
                if check_bad_2(start, end, minimum):
                    s = collatz_sequence(start)
                    if len(s) <= length:
                        bad.append(tuple(s))


print("Computing ...")

get_all_bad()

bad.sort(key=len)

bad_set = set(bad)

minimal_bad = [b for b in bad if not any(b[i:] in bad_set for i in range(1, len(b)))]

cache = dict()


def count_prefixes(end, length):
    if length == 0:
        return 1
    max_ups = length - length // 2
    end = end % (2 * 3 ** max_ups)
    if (end, length) in cache:
        return cache[(end, length)]
    result = count_prefixes(end * 2, length - 1)
    if (end - 4) % 6 == 0:
        result += count_prefixes((end - 1) // 3, length - 1)
    cache[(end, length)] = result
    return result


fib = [0, 1]

for i in range(length + 1):
    fib.append(fib[-1] + fib[-2])

total_bad = sum(count_prefixes(b[0], length - len(b)) for b in minimal_bad)

total_good = fib[length]

print("Answer: ", total_bad + total_good, "Time in seconds: ", time() - t)
