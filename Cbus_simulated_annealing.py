import random
import math


def calculate_distance(route, distances):
    return sum(distances[route[i]][route[i + 1]] for i in range(len(route) - 1))


def generate_initial_route(n, k):
    route = [0]  # Start at the depot
    pickups = list(range(1, n + 1))
    deliveries = list(range(n + 1, 2 * n + 1))
    random.shuffle(pickups)

    capacity = 0
    picked = set()
    dropped = set()

    for p in pickups:
        if capacity < k:
            route.append(p)
            capacity += 1
            picked.add(p)
        route.append(p + n)
        capacity -= 1
        dropped.add(p)

    route.append(0)  # End at depot
    return route


# Generate a neighboring solution by swapping two nodes
def generate_neighbor(route, n):
    neighbor = route[:]
    i = random.randint(1, len(route) - 3)  # Avoid depot nodes
    j = random.randint(1, len(route) - 3)

    # Ensure valid swaps (avoid invalid capacity states)
    if neighbor[i] != neighbor[j]:
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor


def is_valid_route(route, n, k):
    capacity = 0
    picked = set()

    for point in route:
        if point <= n:  # Pickup
            capacity += 1
            picked.add(point)
        else:  # Drop-off
            if (point - n) not in picked:
                return False
            capacity -= 1
        if capacity > k:
            return False

    return True


def simulated_annealing(n, k, distances, initial_temp, cooling_rate, max_iter):
    current_route = generate_initial_route(n, k)
    while not is_valid_route(current_route, n, k):
        current_route = generate_initial_route(n, k)

    best_route = current_route[:]
    best_distance = calculate_distance(best_route, distances)
    current_temp = initial_temp

    for _ in range(max_iter):
        neighbor = generate_neighbor(current_route, n)
        while not is_valid_route(neighbor, n, k):
            neighbor = generate_neighbor(current_route, n)

        current_distance = calculate_distance(current_route, distances)
        neighbor_distance = calculate_distance(neighbor, distances)

        # Acceptance probability
        if neighbor_distance < current_distance or random.random() < math.exp(
            (current_distance - neighbor_distance) / current_temp
        ):
            current_route = neighbor[:]

        # Update the best solution
        if calculate_distance(current_route, distances) < best_distance:
            best_route = current_route[:]
            best_distance = calculate_distance(current_route, distances)

        # Cool down
        current_temp *= cooling_rate
        if current_temp < 1e-6:
            break

    return best_route, best_distance


n, k = map(int, input().split())
distances = [list(map(int, input().split())) for _ in range(2 * n + 1)]

# Parameters
initial_temp = 10000.0
cooling_rate = 0.9995
max_iter = 1000000

optimized_route, optimized_distance = simulated_annealing(
    n, k, distances, initial_temp, cooling_rate, max_iter
)

print(n)
print(" ".join(map(str, optimized_route[1:-1])))
print(optimized_distance)
