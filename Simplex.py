# PYTHON
import sys

# inputting
[n, m] = [int(x) for x in sys.stdin.readline().split()]
c = [-float(x) for x in sys.stdin.readline().split()]
a = [[float(x) for x in sys.stdin.readline().split()] for y in range(m)]
b = [float(x) for x in sys.stdin.readline().split()]


# adding slack variables and setting up tabular form
for x in range(m):
    for i in range(x):
        a[x].append(0)
    for i in range(1):
        a[x].append(1.0)
    for j in range(m - x):
        a[x].append(0)
    c.append(0)

b.append(0)
c.append(1.0)
a.append(c)

for x in range(m + 1):
    a[x].append(b[x])  # now array a becomes the tabular form of simplex method

# finding optimal values
e = ["inf" for x in range(m)]  # ratio list

opt = [0 for i in range(n)]

while True:
    # checking for the smallest negative value on the last row to find the pivot column
    minimum = 9999999
    neg = False
    for i in range(m + n):
        if a[m][i] < 0 and minimum > a[m][i]:
            minimum = a[m][i]
            pivot_col = i  # finding pivot column
            neg = True
    if neg:
        count_inf = 0  # check for number of infinity values in e
        # calculating e
        for i in range(m):
            if a[i][pivot_col] <= 0:
                e[i] = "inf"
                count_inf += 1
            else:
                e[i] = a[i][6] / a[i][pivot_col]
        # if all of the values in e are infinity then there is no optimal solution
        if count_inf == m:
            print("UNBOUNDED")
            break
        # finding the smallest value of e to find the pivot row
        min_e = 9999999
        for i in range(m):
            if e[i] != "inf" and min_e > e[i]:
                pivot_row = i  # finding pivot row
                min_e = e[i]
        # Using Gaussian elimination
        tmp = a[pivot_row][pivot_col]
        for i in range(m + n + 2):
            a[pivot_row][i] /= tmp
        for i in range(m + 1):
            tmp = a[i][pivot_col] / a[pivot_row][pivot_col]
            if i != pivot_row:
                for j in range(m + n + 2):
                    a[i][j] = -tmp * a[pivot_row][j] + a[i][j]
    else:
        # printing optimal solution
        for i in range(m):
            for j in range(n):
                if a[i][j] == 1.0:
                    opt[j] = a[i][m + n + 1]
        print(n)
        print(*opt)
        break
