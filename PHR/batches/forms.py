from django import forms
from .models import AssignRegion, AssignCenter, CreateBatch, Enrollment
from user_roles.models import Multiuser  

class AssignRegionForm(forms.ModelForm):
    class Meta:
        model = AssignRegion
        fields = ['region', 'rm_user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rm_user'].queryset = Multiuser.objects.filter(role='rm')


class AssignCenterForm(forms.ModelForm):
    class Meta:
        model = AssignCenter
        fields = ['center', 'cm_user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter users by role 'CM'
        self.fields['cm_user'].queryset = Multiuser.objects.filter(role='cm')
        
        
class BatchForm(forms.ModelForm):
    class Meta:
        model = CreateBatch
        fields = ['name', 'project', 'vertex', 'quarter', 'target']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student_name']