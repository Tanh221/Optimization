# Input
# n = 3
# k = 2

# distances = [
#     [0, 82, 15, 4, 95, 36, 32],
#     [82, 0, 29, 18, 95, 14, 87],
#     [15, 29, 0, 95, 70, 12, 76],
#     [4, 18, 95, 0, 55, 5, 4],
#     [95, 95, 70, 55, 0, 12, 28],
#     [36, 14, 12, 5, 12, 0, 30],
#     [32, 87, 76, 4, 28, 30, 0],
# ]

import sys

sys.setrecursionlimit(3000)


def Input():
    [n, k] = [int(x) for x in sys.stdin.readline().split()]
    d = []
    for i in range(2 * n + 1):
        r = [int(x) for x in sys.stdin.readline().split()]
        d.append(r)
    return n, k, d


n, k, distances = Input()

min_cost = float("inf")
best_path = []
x = [0] * (2 * n + 1)
visited = [False] * (2 * n + 1)
load = 0
current_cost = 0


def is_valid_move(v, load, visited):
    if v <= n:
        return load < k and not visited[v]
    else:
        return visited[v - n] and not visited[v]


def greedy(k):
    global load, current_cost, min_cost, best_path
    if k == 2 * n + 1:
        total_cost = current_cost + distances[x[k - 1]][0]
        if total_cost < min_cost:
            min_cost = total_cost
            best_path = x[:] + [0]
        return

    # Find the valid move with the minimum distance
    min_distance = float("inf")
    best_move = -1
    for v in range(1, 2 * n + 1):
        if is_valid_move(v, load, visited):
            if distances[x[k - 1]][v] < min_distance:
                min_distance = distances[x[k - 1]][v]
                best_move = v

    if best_move != -1:
        x[k] = best_move
        visited[best_move] = True
        current_cost += distances[x[k - 1]][x[k]]
        if best_move <= n:
            load += 1
        else:
            load -= 1

        greedy(k + 1)

        # Backtrack
        if best_move <= n:
            load -= 1
        else:
            load += 1
        current_cost -= distances[x[k - 1]][x[k]]
        visited[best_move] = False


greedy(1)
# print(f"Minimum cost: {min_cost}")
# print(f"Best path: {' '.join(map(str, best_path))}")
print(n)
print(*best_path[1:-1])
