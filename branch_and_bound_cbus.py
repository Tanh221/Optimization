import sys
import time


def Input():
    [n, k] = [int(x) for x in sys.stdin.readline().split()]
    d = []
    for i in range(2 * n + 1):
        r = [int(x) for x in sys.stdin.readline().split()]
        d.append(r)
    return n, k, d


n, k, distances = Input()
start = time.time()
min_cost = float("inf")
best_path = []

x = [0] * (2 * n + 1)
visited = [False] * (2 * n + 1)
load = 0
current_cost = 0

min_dis = min(distances[i][j] for i in range(2 * n + 1) for j in range(2 * n + 1))


def Try(k):
    global load, current_cost, min_cost, best_path
    if k == 2 * n + 1:  # All passengers picked up and dropped off
        total_cost = current_cost + distances[x[k - 1]][0]  # Add distance to 0
        if total_cost < min_cost:
            min_cost = total_cost
            best_path = x[:] + [0]
        return

    for v in range(1, 2 * n + 1):  # Try each point from 1
        if is_valid_move(v, load, visited):
            x[k] = v
            visited[v] = True
            current_cost += distances[x[k - 1]][x[k]]
            if v <= n:
                load += 1
            else:
                load -= 1
            if current_cost + (2 * n + 1 - k) * min_dis < min_cost:  # lower bound
                Try(k + 1)
            # Backtrack
            if v <= n:
                load -= 1
            else:
                load += 1
            current_cost -= distances[x[k - 1]][x[k]]
            visited[v] = False


def is_valid_move(v, load, visited):
    if v <= n:  # Pick up a passenger
        return load < k and not visited[v]
    else:  # Drop off a passenger
        return (
            visited[v - n] and not visited[v]
        )  # check passenger has been picked up and not already dropped off


Try(1)
end = time.time()
print(f"Minimum cost: {min_cost}")
print(f"Best path: {' '.join(map(str, best_path))}")
print("runtime: ", start - end)
