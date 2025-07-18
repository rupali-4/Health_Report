from django.db import models

# Create your models here.

from projects.models import CreateProject, VertexAllocation  # PMO-created projects
from django.conf import settings
from batches.models import AssignCenter

# vp allocated target to rm: Target breakdown is RM-wise for each vertex
class VpRmAllocation(models.Model):
    project = models.ForeignKey(CreateProject, on_delete=models.CASCADE)
    vertex = models.CharField(max_length=50, choices=VertexAllocation.VERTEX_CHOICES)
    rm_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target = models.PositiveIntegerField()

    class Meta:
        unique_together = ('project', 'vertex', 'rm_user')

    
    
# rm allocated target to cm: RM further distributes target across centers under them. Each target is broken down by Quarter (Q1, Q2, Q3, Q4)
class RmCenterQuarterAllocation(models.Model):
    project = models.ForeignKey(CreateProject, on_delete=models.CASCADE)
    vertex = models.CharField(max_length=50, choices=VertexAllocation.VERTEX_CHOICES)
    center = models.ForeignKey(AssignCenter, on_delete=models.CASCADE)  # could be a centre model
    quarter = models.CharField(max_length=2, choices=[('Q1','Q1'),('Q2','Q2'),('Q3','Q3'),('Q4','Q4')])
    target = models.PositiveIntegerField()
    rm_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('project', 'vertex', 'center', 'quarter', 'rm_user')

    
