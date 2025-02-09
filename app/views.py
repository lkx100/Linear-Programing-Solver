from django.shortcuts import render
from django.http import JsonResponse
from .LP_Algorithms.Transportation import SimplexMethod
from .LP_Algorithms.GraphicalMethod import GraphicalMethod
from .LP_Algorithms.SimplexMethod import SimplexSolver
import numpy as np

def home(request):
    return render(request, 'home.html', {})

def transportation_method(request):
    if request.method == 'POST':
        try:
            # Get and validate matrix dimensions
            rows = request.POST.get('matrix_rows')
            cols = request.POST.get('matrix_cols')
            
            if not rows or not cols:
                raise ValueError("Matrix dimensions are required")
            
            rows = int(rows)
            cols = int(cols)
            
            if rows <= 0 or cols <= 0:
                raise ValueError("Number of rows and columns must be positive")

            # Build and validate cost matrix
            cost_matrix = []
            for i in range(rows):
                row = []
                for j in range(cols):
                    value = request.POST.get(f'cost_{i}_{j}')
                    if not value:
                        raise ValueError(f"Cost value at position ({i},{j}) is missing")
                    row.append(float(value))
                cost_matrix.append(row)

            # Build and validate supply and demand vectors
            supply = []
            demand = []
            total_supply = 0
            total_demand = 0

            for i in range(rows):
                value = request.POST.get(f'supply_{i}')
                if not value:
                    raise ValueError(f"Supply value at position {i} is missing")
                supply_val = float(value)
                if supply_val <= 0:
                    raise ValueError(f"Supply value at position {i} must be positive")
                supply.append(supply_val)
                total_supply += supply_val

            for i in range(cols):
                value = request.POST.get(f'demand_{i}')
                if not value:
                    raise ValueError(f"Demand value at position {i} is missing")
                demand_val = float(value)
                if demand_val <= 0:
                    raise ValueError(f"Demand value at position {i} must be positive")
                demand.append(demand_val)
                total_demand += demand_val

            # Check if total supply equals total demand
            if total_supply != total_demand:
                raise ValueError("Total supply must equal total demand")

            problem = SimplexMethod(cost_matrix, supply, demand)
            result = problem.solve_transportation_problem()
            
            if result["total_cost"] is None:
                raise ValueError("No feasible solution found")

            response_data = {
                'total_cost': round(result["total_cost"], 2),  # Round to 2 decimal places
                'status': result["status"],
                'error': None
            }

        except ValueError as e:
            response_data = {
                'error': str(e)
            }
        except Exception as e:
            response_data = {
                'error': "An unexpected error occurred. Please check your input values."
            }

        # Always return JSON for POST requests
        return JsonResponse(response_data)

    # For GET requests, render the template
    return render(request, 'transportation_method.html', {})

def graphical_method(request):
    if request.method == "POST":
        try:
            # Get objective function coefficients and problem type
            c1 = float(request.POST.get("c1"))
            c2 = float(request.POST.get("c2"))
            problem_type = request.POST.get("problem_type", "max")
            # Get and validate constraints count
            constraint_count = int(request.POST.get("constraint_count"))
            if constraint_count <= 0:
                raise ValueError("At least one constraint is required.")
            constraints = []
            for i in range(constraint_count):
                a_val = float(request.POST.get(f"constraint_{i}_a"))
                b_val = float(request.POST.get(f"constraint_{i}_b"))
                limit = float(request.POST.get(f"constraint_{i}_limit"))
                constraints.append({"a": a_val, "b": b_val, "limit": limit})
            solver = GraphicalMethod([c1, c2], constraints, problem_type)
            result = solver.solve()
            response_data = {
                "optimal_value": round(result["optimal_value"], 2),
                "solution": [round(sol, 2) for sol in result["solution"]],
                "status": result["status"],
                "error": None
            }
            response_data["graph_data"] = solver.get_graph_details()
            # Pass the optimal solution coordinates to get_plot
            response_data["plot"] = solver.get_plot(optimal_solution=result["solution"])
        except Exception as e:
            response_data = {"error": str(e)}
        return JsonResponse(response_data)

    return render(request, "graphical_method.html", {})


def simplex_method(request):
    if request.method == "POST":
        try:
            num_vars = int(request.POST.get("num_vars"))
            num_constraints = int(request.POST.get("num_constraints"))
            # Read objective coefficients
            c = [float(request.POST.get(f"obj_{i}")) for i in range(num_vars)]
            A = []
            b = []
            for i in range(num_constraints):
                # For each constraint, read coefficients for each variable
                row = [float(request.POST.get(f"constr_{i}_coef_{j}")) for j in range(num_vars)]
                A.append(row)
                b.append(float(request.POST.get(f"constr_{i}_rhs")))
            problem_type = request.POST.get("problem_type", "max").lower()
            if problem_type == "min":
                c = [-x for x in c]
            solver = SimplexSolver(np.array(c), np.array(A), np.array(b))
            solution, optimal_value = solver.solve()
            response_data = {
                "solution": [round(x, 2) for x in solution],
                "optimal_value": round(optimal_value, 2),
                "error": None
            }
        except Exception as e:
            response_data = {"error": str(e)}
        return JsonResponse(response_data)
    return render(request, "simplex_method.html", {})
