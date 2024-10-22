# Input
n = 5
k = 3
distances = [
    [0, 5, 8, 11, 12, 8, 3, 3, 7, 5, 5],
    [5, 0, 3, 5, 7, 5, 3, 4, 2, 2, 2],
    [8, 3, 0, 7, 8, 8, 5, 7, 1, 6, 5],
    [11, 5, 7, 0, 1, 5, 9, 8, 6, 5, 6],
    [12, 7, 8, 1, 0, 6, 10, 10, 7, 7, 7],
    [8, 5, 8, 5, 6, 0, 8, 5, 7, 3, 4],
    [3, 3, 5, 9, 10, 8, 0, 3, 4, 5, 4],
    [3, 4, 7, 8, 10, 5, 3, 0, 6, 2, 2],
    [7, 2, 1, 6, 7, 7, 4, 6, 0, 5, 4],
    [5, 2, 6, 5, 7, 3, 5, 2, 5, 0, 1],
    [5, 2, 5, 6, 7, 4, 4, 2, 4, 1, 0],
]

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
print(f"Minimum cost: {min_cost}")
print(f"Best path: {' '.join(map(str, best_path))}")
