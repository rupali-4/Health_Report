from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class Multiuser(AbstractUser):
    ROLE_CHOICES = [
        ('pmo', 'PMO (Project Management Office)'),
        ('vp', 'VP (Vice President)'),
        ('rm', 'RM (Regional Manager)'),
        ('cm', 'CM (Center Manager)')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    security_question = models.CharField(max_length=255)
    security_answer = models.CharField(max_length=255)
    
    def __str__(self):
        return self.username
    
    # pmo = models.BooleanField('PMO (Project Management Office)', default= False)
    # vp = models.BooleanField('VP (Vice President)', default= False)
    # rm = models.BooleanField('RM (Regional Manager)', default= False)
    # cm = models.BooleanField('CM (Center Manager)', default= False)
    # 'RM' these are label on side of checkbox in forms
    # not using above checkbox as i want only 1 option to be selected 