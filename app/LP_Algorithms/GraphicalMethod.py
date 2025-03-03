import numpy as np
from scipy.optimize import linprog
import matplotlib
matplotlib.use("Agg")  # Added to use a non-GUI backend
import matplotlib.pyplot as plt
import io, base64

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

    def get_graph_details(self):
        import math
        eps = 1e-7
        # Build list of lines: original constraints and non-negativity (x=0, y=0)
        lines = []
        for constr in self.constraints:
            lines.append((constr['a'], constr['b'], constr['limit']))
        lines.append((1, 0, 0))  # x = 0
        lines.append((0, 1, 0))  # y = 0

        def intersect(line1, line2):
            a1, b1, c1 = line1
            a2, b2, c2 = line2
            det = a1 * b2 - a2 * b1
            if abs(det) < eps:
                return None
            x = (c1 * b2 - c2 * b1) / det
            y = (a1 * c2 - a2 * c1) / det
            return (x, y)

        points = []
        # Find all intersection points
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                pt = intersect(lines[i], lines[j])
                if pt is not None:
                    x, y = pt
                    if x >= -eps and y >= -eps:
                        valid = True
                        for constr in self.constraints:
                            if constr['a'] * x + constr['b'] * y > constr['limit'] + eps:
                                valid = False
                                break
                        if valid:
                            points.append((x, y))
        # Remove duplicates
        unique_points = []
        for pt in points:
            if not any(math.hypot(pt[0] - up[0], pt[1] - up[1]) < eps for up in unique_points):
                unique_points.append(pt)
        if unique_points:
            cx = sum(pt[0] for pt in unique_points) / len(unique_points)
            cy = sum(pt[1] for pt in unique_points) / len(unique_points)
            unique_points.sort(key=lambda pt: math.atan2(pt[1] - cy, pt[0] - cx))
            polygon = {"x": [pt[0] for pt in unique_points], "y": [pt[1] for pt in unique_points]}
        else:
            polygon = {"x": [], "y": []}

        # Prepare endpoints for each constraint for plotting
        constraints_plot = []
        for constr in self.constraints:
            a, b, limit = constr['a'], constr['b'], constr['limit']
            pts = []
            if abs(b) > eps:
                pts.append((0, limit / b))
            if abs(a) > eps:
                pts.append((limit / a, 0))
            if len(pts) == 1:
                pts.append((pts[0][0] + 1, pts[0][1]))
            constraints_plot.append({
                "x": [p[0] for p in pts],
                "y": [p[1] for p in pts]
            })

        return {"constraints": constraints_plot, "polygon": polygon}

    def get_plot(self, optimal_solution=None):  # Modified to accept optimal_solution
        # Get graph details from existing method
        graph_data = self.get_graph_details()
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('lightgrey')  # Set the background color of the figure
        ax.set_facecolor('lightgrey')  # Set the background color of the axes
        # Plot each constraint line
        for idx, constraint in enumerate(graph_data["constraints"]):
            ax.plot(constraint["x"], constraint["y"], label=f"Constraint {idx+1}")
        # Plot feasible region if available
        if graph_data["polygon"]["x"]:
            poly_x = graph_data["polygon"]["x"]
            poly_y = graph_data["polygon"]["y"]
            if poly_x[0] != poly_x[-1] or poly_y[0] != poly_y[-1]:
                poly_x = poly_x + [poly_x[0]]
                poly_y = poly_y + [poly_y[0]]
            ax.fill(poly_x, poly_y, 'green', alpha=0.2, label="Feasible Region")
        # Annotate the optimal solution if provided
        if optimal_solution is not None:
            # Cast to float for safety
            x_opt = float(optimal_solution[0])
            y_opt = float(optimal_solution[1])
            ax.plot(x_opt, y_opt, 'ro', markersize=8)
            # Use ax.text with an offset to ensure visibility
            ax.text(x_opt + 0.1, y_opt, f"({x_opt:.2f}, {y_opt:.2f})", color='red', fontsize=12, fontweight='bold')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode('utf8')

