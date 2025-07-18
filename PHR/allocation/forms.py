from django import forms
from .models import VpRmAllocation, RmCenterQuarterAllocation

from django.contrib.auth import get_user_model
User = get_user_model() # This now points to Multiuser because of AUTH_USER_MODEL

class VpRmAllocationForm(forms.ModelForm):
    class Meta:
        model = VpRmAllocation
        fields = ['project', 'vertex', 'rm_user', 'target']
        
    def __init__(self, *args, **kwargs):
        super(VpRmAllocationForm, self).__init__(*args, **kwargs)
        # ✅ Only include users where role is 'rm'
        self.fields['rm_user'].queryset = User.objects.filter(role='rm')


class RmCenterQuarterForm(forms.ModelForm):
    class Meta:
        model = RmCenterQuarterAllocation
        fields = ['project', 'vertex', 'center', 'quarter', 'target']
        
    def __init__(self, *args, **kwargs):
        super(RmCenterQuarterForm, self).__init__(*args, **kwargs)
        #self.fields['cm_user'].queryset = User.objects.filter(role='cm')  # filter by CM role
            
            
            