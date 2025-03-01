from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import pandas as pd

class TimetableSolver:
    def __init__(self, sections, courses, professors, course_time_requirements, days, time_slots):
        self.sections = sections
        self.courses = courses
        self.professors = professors
        self.course_time_requirements = course_time_requirements
        self.days = days
        self.time_slots = time_slots
        self.model = LpProblem("Timetable_Scheduling", LpMaximize)
        self.x = LpVariable.dicts("x", [(c, d, t, s) for s in sections for c in courses[s] for d in days for t in time_slots], cat='Binary')

    def define_objective(self):
        self.model += lpSum(self.x[c, d, t, s] for s in self.sections for c in self.courses[s] for d in self.days for t in self.time_slots)

    def add_constraints(self):
        # Constraint 1: Each course must be scheduled exactly as required in a week
        for s in self.sections:
            for c in self.courses[s]:
                self.model += lpSum(self.x[c, d, t, s] for d in self.days for t in self.time_slots) == self.course_time_requirements[c]

        # Constraint 2: A professor cannot teach two courses at the same time
        for d in self.days:
            for t in self.time_slots:
                for prof in set(self.professors.values()):
                    self.model += lpSum(self.x[c, d, t, s] for s in self.sections for c in self.courses[s] if self.professors[c] == prof) <= 1

        # Constraint 3: No two courses should be at the same time slot for a section
        for s in self.sections:
            for d in self.days:
                for t in self.time_slots:
                    self.model += lpSum(self.x[c, d, t, s] for c in self.courses[s]) <= 1

    def solve(self):
        self.model.solve()

    def print_solution(self):
        print("\nOptimal Weekly Timetable:")
        for s in self.sections:
            print(f"\nSection {s} Timetable:")
            for d in self.days:
                for c in self.courses[s]:
                    for t in self.time_slots:
                        if self.x[c, d, t, s].value() == 1:
                            print(f"{d}: Course {c} (Prof {self.professors[c]}) → Time Slot {t}")

    def get_weekly_timetable(self):
        weekly_timetable_data = {}
        for s in self.sections:
            weekly_timetable_data[s] = {}
            for d in self.days:
                weekly_timetable_data[s][d] = {}
                for t in self.time_slots:
                    weekly_timetable_data[s][d][t] = ''  # Initialize with empty strings

        for s in self.sections:
            for d in self.days:
                for c in self.courses[s]:
                    for t in self.time_slots:
                        if self.x[c, d, t, s].value() == 1:
                            weekly_timetable_data[s][d][t] = f"{c}"

        return weekly_timetable_data

    def print_weekly_timetable(self):
        weekly_timetable_data = self.get_weekly_timetable()
        for s in self.sections:
            print(f"\nWeekly Timetable for Section {s}:")
            section_df = pd.DataFrame.from_dict(weekly_timetable_data[s]).transpose()
            print(section_df)

# Example usage
if __name__ == "__main__":
    sections = ['A', 'B', 'C', 'D']
    courses = {
        'A': ['Maths', 'Physics', 'Chemistry', 'FSD'],
        'B': ['Maths', 'DMW', 'Chemistry', 'Sanskrit'],
        'C': ['Sports', 'Physics', 'Biology', 'Hindi'],
        'D': ['Maths', 'DL', 'Chemistry', 'Sanskrit'],
    }
    professors = {
        'Maths': 'Prof A',
        'Physics': 'Prof B',
        'Chemistry': 'Prof C',
        'FSD': 'Prof D',
        'DMW': 'Prof E',
        'Sports': 'Prof A',
        'DL': 'Prof B',
        'Biology': 'Prof C',
        'Sanskrit': 'Prof D',
        'Hindi': 'Prof E',
    }
    course_time_requirements = {
        'Maths': 5,
        'Physics': 5,
        'Chemistry': 5,
        'FSD': 5,
        'DMW': 5,
        'Sports': 3,
        'DL': 5,
        'Biology': 5,
        'Sanskrit': 5,
        'Hindi': 7,
    }
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = ['T1', 'T2', 'T3', 'T4']

    solver = TimetableSolver(sections, courses, professors, course_time_requirements, days, time_slots)
    solver.define_objective()
    solver.add_constraints()
    solver.solve()
    solver.print_solution()
    solver.print_weekly_timetable()