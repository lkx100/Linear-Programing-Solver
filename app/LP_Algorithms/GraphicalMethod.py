import numpy as np
from scipy.optimize import linprog

class GraphicalMethod:
    def __init__(self, objective, constraints, problem_type="max"):
        # objective: list of two coefficients e.g. [c1, c2]
        # constraints: list of dicts { 'a': float, 'b': float, 'limit': float }
        # problem_type: "max" or "min"
        self.objective = objective
        self.constraints = constraints
        self.problem_type = problem_type.lower()

    def solve(self):
        # Ensure problem supports only 2 variables
        if len(self.objective) != 2:
            raise ValueError("Only 2-variable problems are supported.")
        c = self.objective[:]
        if self.problem_type == "max":
            # Convert maximization to minimization by multiplying by -1
            c = [-x for x in c]
        A_ub = []
        b_ub = []
        for constr in self.constraints:
            A_ub.append([constr['a'], constr['b']])
            b_ub.append(constr['limit'])
        bounds = [(0, None), (0, None)]
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
        if result.success:
            optimal_value = result.fun
            if self.problem_type == "max":
                optimal_value = -optimal_value
            return {
                "optimal_value": optimal_value,
                "solution": result.x,
                "status": result.message,
            }
        else:
            raise ValueError(result.message)
