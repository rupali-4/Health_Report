from django.db import models

# Create your models here.

# Project: name, total_target, start_date, end_date, etc.
# VertexTargetAllocation: project, vertex_name (Diya, SAVE, etc.), target 

from django.conf import settings

class CreateProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    total_target = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name  # this makes the dropdown show project names
    
    
class VertexAllocation(models.Model):
    VERTEX_CHOICES = [
        ('Diya', 'Diya'),
        ('Deep Tech', 'Deep Tech'),
        ('SAVE', 'SAVE'),
        ('BEST', 'BEST'),
    ]
    
    project = models.ForeignKey(CreateProject, related_name='vertex_allocations', on_delete=models.CASCADE)
    vertex = models.CharField(max_length=50, choices=VERTEX_CHOICES)
    target = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('project', 'vertex')
        
    # CASCADE means if the user is deleted, then delete all the related projects automatically