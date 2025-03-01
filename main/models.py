from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Class(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name
    
class Faculty(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=1000)
    classes_per_week = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    Faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} - {self.Faculty.name}"
    
class Weekday(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class TimeSlot(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name