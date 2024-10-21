from itertools import permutations


def brute_force(n, k, distances):
    points = list(range(1, 2 * n + 1))
    min_cost = float("inf")
    best_path = []

    def is_valid_path(path):  # kiểm tra đường đi hợp lệ
        load = 0
        picked = set()
        for point in path:
            if point <= n:
                load += 1
                picked.add(point)
            else:
                if (point - n) not in picked:
                    return False
                load -= 1
            if load > k:
                return False
        return True

    for perm in permutations(points):  # duyet toàn bộ hoán vị từ 1->10
        path = [0] + list(perm) + [0]  # add thêm 2 điểm 0 ở xuất phát và kết thúc
        if not is_valid_path(path[1:-1]):
            continue
        cost = sum(
            distances[path[i]][path[i + 1]] for i in range(len(path) - 1)
        )  # tính distance
        if cost < min_cost:
            min_cost = cost  # update min_cost and best path
            best_path = path

    return min_cost, best_path


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

min_cost, best_path = brute_force(n, k, distances)
print(f"Minimum cost: {min_cost}")
print(f"Best path: {' '.join(map(str, best_path))}")
