import numpy as np
from scipy.optimize import linprog

def optimize_distribution(supply, demand, cost_matrix):
    supply = np.array(supply)
    demand = np.array(demand)
    cost_matrix = np.array(cost_matrix)

    # Number of suppliers & demand points
    num_suppliers, num_demands = cost_matrix.shape

    # Convert the cost matrix into a 1D array
    c = cost_matrix.flatten()

    # Constraints: Supply constraints (each row <= supply[i])
    A_eq = []
    b_eq = []

    for i in range(num_suppliers):
        row_constraint = np.zeros(num_suppliers * num_demands)
        row_constraint[i * num_demands: (i + 1) * num_demands] = 1
        A_eq.append(row_constraint)
        b_eq.append(supply[i])

    # Constraints: Demand constraints (each column <= demand[j])
    for j in range(num_demands):
        col_constraint = np.zeros(num_suppliers * num_demands)
        col_constraint[j::num_demands] = 1
        A_eq.append(col_constraint)
        b_eq.append(demand[j])

    # Solve the optimization problem
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, method="highs")

    if result.success:
        allocation = np.array(result.x).reshape(num_suppliers, num_demands)
        return allocation.tolist()
    else:
        return "Optimization failed."

