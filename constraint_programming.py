from ortools.sat.python import cp_model
import sys
def Input():
    [n, k] = [int(x) for x in sys.stdin.readline().split()]
    d = []
    for i in range(2 * n + 1):
        r = [int(x) for x in sys.stdin.readline().split()]
        d.append(r)
    return n, k, d

def data(n, k, dis):
    data = {}
    data["n"] = n
    data["k"] = k
    data["distance"] = dis
    return data

def constraint_solver():
    model = cp_model.CpModel()
    n, k, dis = Input()
    x = {}
    u = {}
    u[0] = 0
    index = {}

    for i in range(2*n + 1):
        for j in range(2*n + 1):
            if i != j:
                x[i,j] = model.NewIntVar(0, 1, "x(" + str(i) + str(j) + ")") ###
    
    for i in range(1, n + 1):
        u[i] = model.NewIntVar(1, k, "load after leaving point " + str(i))

    for i in range(n + 1, 2*n + 1):
        u[i] = model.NewIntVar(0, k-1, "load after leaving point " + str(i))

    for i in range(1, 2*n + 1):
        index[i] = model.NewIntVar(1, 2*n, "index visitting point " + str(i))

    for i in range(2*n + 1):
        model.Add(sum(x[i,j] for j in range(2*n + 1) if i != j) == 1)
        model.Add(sum(x[j,i] for j in range(2*n + 1) if i != j) == 1)

    for i in range(2*n + 1):
        for j in range(1, n + 1):
            if i != j:
                model.Add(u[j] == u[i] + 1).OnlyEnforceIf(x[i,j]) ###

    for i in range(1, 2*n + 1):
        for j in range(n + 1, 2*n + 1):
            if i != j:
                model.Add(u[i] == u[j] + 1).OnlyEnforceIf(x[i,j])

    for i in range(1, n + 1):
        model.Add(x[i,0] == 0)
        model.Add(x[0,i+n] == 0)

    for i in range(1, n + 1):
        model.Add(index[i+n] > index[i])

    for i in range(1, 2*n + 1):
        for j in range(1, 2*n + 1):
            if i != j:
                model.Add(index[j] == index[i] + 1).OnlyEnforceIf(x[i,j])

    obj = sum(x[i,j] * data(n, k, dis)["distance"][i][j] for i in range(2*n + 1) for j in range(2*n + 1) if i != j)
    model.Minimize(obj)
    solver = cp_model.CpSolver() ###
    status = solver.Solve(model) ###
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(n)
        count = 1
        current_point = 0
        while(count <= 2*n):
            i = current_point
            for j in range(2*n + 1):
                if i != j and solver.Value(x[i,j]) == 1: ###
                    print(j, end = " ")
                    current_point = j
                    count += 1

        #print(status)
        print()
        print(solver.Value(obj)) ###

constraint_solver()
