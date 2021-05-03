""" Exact and approximate algorithms for subset sum problem """

def exact_dyn(items, n, k):
    """ Exact algorithm using dynamic programming """
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
    pass


def greedy(items, k):
    """ Greedy algorithm that is 2-approximate """
    result = []
    sorted_items = sorted(items, reverse = True)
    curr_sum = 0

    for item in sorted_items:
        if item <= k - curr_sum:
            result.append(item)
            curr_sum += item

    return result


def fptas(items, k, epsilon):
    """ Approximate algorithm that is FPTAS. Epsilon controls how good the
        approximation is"""
    l = [0]
    for item in items:
        new_l = merge_and_sort(l[-1], l[-1] + item)



def get_input():
    n = int(input())
    k = int(input())
    ls = []
    for _ in range(n):
        ls.append(int(input()))
    return ls
