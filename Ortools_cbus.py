from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
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


def create_data_model(n, k, distances):
    """Stores the data for the problem."""
    data = {}
    data["n"] = n
    data["k"] = k
    data["distance_matrix"] = distances
    data["pickups_deliveries"] = [[i, i + n] for i in range(1, n + 1)]
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


def print_solution(data, manager, routing, solution, runtime):
    """Prints solution in the desired format."""
    path = []
    total_distance = 0
    index = routing.Start(0)
    while not routing.IsEnd(index):
        node_index = manager.IndexToNode(index)
        path.append(node_index)
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        if not routing.IsEnd(index):
            total_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    path.append(manager.IndexToNode(routing.Start(0)))

    print(data["n"])

    print(" ".join(map(str, path[1:-1])))

    print(total_distance)

    print(f"Runtime: {runtime:.2f} seconds")


def main():
    """Entry point of the program."""
    start_time = time.time()

    data = create_data_model(n, k, distances)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Define cost of each arc.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        int(1e9 + 7),  # vehicle maximum travel distance,
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Define Transportation Requests.
    for request in data["pickups_deliveries"]:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index)
        )
        routing.solver().Add(
            distance_dimension.CumulVar(pickup_index)
            <= distance_dimension.CumulVar(delivery_index)
        )

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    runtime = time.time() - start_time  # Calculate the runtime
    if solution:
        print_solution(data, manager, routing, solution, runtime)
    else:
        print("No solution found!")


if __name__ == "__main__":
    main()
