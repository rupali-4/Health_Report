from django.db import models

# Create your models here.

from django.conf import settings
from projects.models import CreateProject, VertexAllocation

# Handles batch tagging and actual enrollments by Center Managers. models:-
# Batch: name, center, project, quarter, vertex
# Enrollment: batch, number_of_students (actual achieved number)

CENTER_CHOICES = [
    ('a_mh', 'Airoli (Maharashtra)'),  
    ('n_mh', 'Nashik (Maharashtra)'),  
    ('p_mh', 'Pune (Maharashtra)'), 
    ('h_tl', 'Hyderabad (Telangana)'), 
    ('a_tl', 'Ameerpet (Telangana)'), 
    ('s_wb', 'Sonarpur (West Bengal)'), 
    ('h_wb', 'Habra (West Bengal)'), 
    ('b_wb', 'Barasat (West Bengal)'), 
    # Add other centers as needed
]

# done by cm : total target, enrollemnt add (option) , vertex: each vertex 1 batch 1 quarter,  
class CreateBatch(models.Model):
    name = models.CharField(max_length=255, unique=True)
    project = models.ForeignKey(CreateProject, on_delete=models.CASCADE)
    vertex = models.CharField(max_length=50, choices=VertexAllocation.VERTEX_CHOICES)
    center = models.CharField(max_length=50, choices=CENTER_CHOICES)
    quarter = models.CharField(max_length=2, choices=[('Q1','Q1'),('Q2','Q2'),('Q3','Q3'),('Q4','Q4')])
    cm_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target = models.PositiveIntegerField()


class Enrollment(models.Model):
    student_name = models.CharField(max_length=255)
    batch = models.ForeignKey(CreateBatch, related_name='enrollments', on_delete=models.CASCADE)


# vp assign region to rm 
class AssignRegion(models.Model):
    REGION_CHOICES = [
    ('mh', 'Maharashtra'),
    ('tl', 'Telangana'),
    ('wb', 'West Bengal'),
    # Add other regions as needed
]
    region = models.CharField(max_length=50, choices=REGION_CHOICES, unique=True)
    rm_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.region} → {self.rm_user}"
    
    
# rm assign center to cm
class AssignCenter(models.Model):
    center = models.CharField(max_length=50, choices=CENTER_CHOICES, unique=True)
    cm_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_center_display()}"
    
    