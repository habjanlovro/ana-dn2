""" Exact and approximate algorithms for subset sum problem """

import timeit
import matplotlib.pyplot as plt


def wrapper(f, *args, **kwargs):
    """ Wrapper for timeit function """
    def wrapped():
        return f(*args, **kwargs)
    return wrapped


def exact_dyn(items, k):
    """ Exact algorithm using dynamic programming """
    n = len(items)
    array = [[0 for _ in range(k + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(k + 1):
            if i == 0 or j == 0:
                array[i][j] = 0
            else:
                index_before = j - items[i - 1]
                if index_before >= 0:
                    item_before = array[i - 1][index_before] + items[i - 1]
                else:
                    item_before = 0
                array[i][j] = max(array[i - 1][j], item_before)
    return array[n][k]


def exact_exh(items, k):
    """ Exact algorithm using branch and prune """
    potential_solutions = [0]
    for item in items:
        potential_solutions = add_solutions(potential_solutions, item)
        potential_solutions = [s for s in potential_solutions if s <= k]
    return max(potential_solutions)


def greedy(items, k):
    """ Greedy algorithm that is 2-approximate """
    sorted_items = sorted(items, reverse = True)
    curr_sum = 0

    for item in sorted_items:
        if item <= k - curr_sum:
            curr_sum += item

    return curr_sum


def fptas(items, k, epsilon):
    """ Approximate algorithm that is FPTAS. Epsilon controls how good the
        approximation is"""
    potential_solutions = [0]
    trim_factor = epsilon / (2 * len(items))
    for item in items:
        potential_solutions = add_solutions(potential_solutions, item)
        potential_solutions = trim(potential_solutions, trim_factor)
        potential_solutions = [s for s in potential_solutions if s <= k]
    return max(potential_solutions)

def add_solutions(l, item):
    new_l = []
    for num in l:
        new_l.append(num + item)
    l += new_l
    return list(set(l))

def trim(l, delta):
    l = sorted(l)
    trimmed_l = [l[0]]
    last = l[0]
    for num in l:
        if num > last * (1 + delta):
            trimmed_l.append(num)
            last = num
    return trimmed_l


def get_input():
    n = int(input())
    k = int(input())
    ls = []
    for _ in range(n):
        ls.append(int(input()))
    return (ls, k)


def meausre_fptas(items, k):
    epsilons = []
    times = []

    epsilon = 0.0
    while epsilon <= 1:
        t = timeit.timeit(wrapper(fptas, items, k, epsilon), number = 1)
        epsilons.append(epsilon)
        times.append(t)
        print(f"fptas %1.2f:\t %f" % (epsilon, t))
        epsilon += 0.05

    plt.plot(epsilons, times)
    plt.xlabel("Epsilon value")
    plt.ylabel("Execution time")
    plt.show()


def dyno_hard():
    times = []
    n = []
    for i in range(5, 20):
        items, k = generate_bad_dyno(i)
        t = timeit.timeit(wrapper(exact_dyn, items, k), number = 1)

        n.append(i)
        times.append(t)

    plt.plot(n, times)
    plt.xlabel("Size of A")
    plt.ylabel("Execution time")
    plt.show()


def generate_bad_exh(n):
    items = [2 ** i for i in range(1, n)]
    k = 2 ** n
    return items, k

def exh_hard():
    times = []
    n = []
    for i in range(5, 20):
        items, k = generate_bad_exh(i)
        t = timeit.timeit(wrapper(exact_dyn, items, k), number = 1)

        n.append(i)
        times.append(t)

    plt.plot(n, times)
    plt.xlabel("Size of A")
    plt.ylabel("Execution time")
    plt.show()




def generate_bad_dyno(n):
    A = [i for i in range(1, n+1)]
    k = 2 ** n
    return A, k


if __name__ == "__main__":
    items, k = get_input()


    print("Exact DYN time:")
    print(timeit.timeit(wrapper(exact_dyn, items, k), number = 1))
    print()

    print("Exact EXH:")
    print(timeit.timeit(wrapper(exact_exh, items, k), number = 1))
    print()

    print("2-approx:")
    print(timeit.timeit(wrapper(greedy, items, k), number = 1))
    print()
