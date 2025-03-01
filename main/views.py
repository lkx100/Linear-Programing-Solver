from django.shortcuts import render
from .models import Class, Subject, Faculty, Weekday, TimeSlot
from .solver import TimetableSolver
import json

# Create your views here.
def home(request):
    return render(request, 'home.html')


def generate(request):
    if request.method == 'POST':
        sections = request.POST.getlist('section_name')
        
        courses = {}
        course_names = request.POST.getlist('course_name')
        course_sections = request.POST.getlist('course_section')
        for name, section in zip(course_names, course_sections):
            if section not in courses:
                courses[section] = []
            courses[section].append(name)
        
        professors = {}
        professor_courses = request.POST.getlist('professor_course')
        professor_names = request.POST.getlist('professor_name')
        for course, name in zip(professor_courses, professor_names):
            professors[course] = name
        
        course_time_requirements = {}
        for course in course_names:
            subject = Subject.objects.get(name=course)
            course_time_requirements[course] = subject.classes_per_week
        
        days = request.POST.getlist('day_name')
        time_slots = request.POST.getlist('time_slot')

        solver = TimetableSolver(sections, courses, professors, course_time_requirements, days, time_slots)
        solver.define_objective()
        solver.add_constraints()
        solver.solve()
        timetable = solver.get_weekly_timetable()

        return render(request, 'generate.html', {'timetable': timetable, 'time_slots': time_slots, 'professors': professors})

    sections = Class.objects.all()
    courses = Subject.objects.all()
    professors = Faculty.objects.all()
    days = Weekday.objects.all()
    time_slots = TimeSlot.objects.all()

    return render(request, 'generate.html', {
        'sections': sections,
        'courses': courses,
        'professors': professors,
        'days': days,
        'time_slots': time_slots,
    })