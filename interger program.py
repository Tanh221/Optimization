from ortools.linear_solver import pywraplp


def IntergerProgrammingExample():
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return

    x = solver.NumVar(0, solver.infinity(), "x")
    y = solver.IntVar(0, solver.infinity(), "y")
    print("Number of variables =", solver.NumVariables())

    # Constraint
    solver.Add(x - 10 * y <= 7)
    solver.Add(2 * x + 3 * y <= 20)
    solver.Add(x <= 14)
    solver.Add(y <= 20)

    print("Number of constraints =", solver.NumConstraints())

    # Objective function:
    solver.Maximize(x + y)

    # Solve the system.
    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print(f"Objective value = {solver.Objective().Value():}")
        print(f"x = {x.solution_value():}")
        print(f"y = {y.solution_value():}")

    else:
        print("The problem does not have an optimal solution.")

    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")


IntergerProgrammingExample()
