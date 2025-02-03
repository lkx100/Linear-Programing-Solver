import numpy as np
from scipy.optimize import linprog

class SimplexMethod:
    def __init__(self, cost_matrix, supply, demand):
        self.cost_matrix = cost_matrix
        self.supply = supply
        self.demand = demand

    def solve_transportation_problem(self):
        """
        Solves the transportation problem using linear programming.
        Parameters:
            cost_matrix (2D list or numpy array): Cost matrix (m x n) where m is the number of sources and n is the number of destinations.
            supply (list): List of supply capacities for each source.
            demand (list): List of demand requirements for each destination.

        Returns:
            result: Dictionary with the solution, total cost, and status.
        """
        # Convert inputs to numpy arrays
        matrix = np.array(self.cost_matrix)
        np_supply = np.array(self.supply)
        np_demand = np.array(self.demand)

        # Number of sources and destinations
        m, n = matrix.shape

        # Flatten the cost matrix for linprog
        c = matrix.flatten()

        # Create the inequality constraint matrix and vector
        A_eq = []
        b_eq = []

        # Supply constraints (row-wise)
        for i in range(m):
            row_constraint = [0] * (m * n)
            for j in range(n):
                row_constraint[i * n + j] = 1
            A_eq.append(row_constraint)
            b_eq.append(np_supply[i])

        # Demand constraints (column-wise)
        for j in range(n):
            col_constraint = [0] * (m * n)
            for i in range(m):
                col_constraint[i * n + j] = 1
            A_eq.append(col_constraint)
            b_eq.append(np_demand[j])

        # Solve the problem using linprog
        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='highs')

        # Process the solution
        if result.success:
            solution_matrix = result.x.reshape(m, n)
            return {
                "solution": solution_matrix,
                "total_cost": result.fun,
                "status": result.message,
            }
        else:
            return {
                "solution": None,
                "total_cost": None,
                "status": result.message,
            }



'''
    Example usage

    cost_matrix = [
        [2, 3, 1],
        [5, 4, 8],
        [5, 6, 8]
    ]

    supply = [20, 30, 25]
    demand = [10, 25, 40]

    result = solve_transportation_problem(cost_matrix, supply, demand)

    print("Optimal Transportation Plan:")
    print(result["solution"])
    print("Total Cost:")
    print(result["total_cost"])
    print("Status:")
    print(result["status"])
'''