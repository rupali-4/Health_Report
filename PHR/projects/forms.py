from django import forms
from .models import CreateProject, VertexAllocation
from django.forms import modelformset_factory

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = CreateProject
        fields = ['name', 'description', 'total_target', 'start_date', 'end_date']
        

class VertexAllocationForm(forms.ModelForm):
    class Meta:
        model = VertexAllocation
        fields = ['vertex', 'target']
        widgets = {
            'vertex': forms.HiddenInput(),  # Hide dropdown
            'target': forms.NumberInput(attrs={'min': 0})
        }
        
VertexAllocationFormSet = modelformset_factory(
    VertexAllocation,             # The model the formset is based on
    form=VertexAllocationForm,
    extra=4,        # Number of empty forms to display by default (for 4 vertex types)
    max_num=4,          # Maximum number of forms allowed in the formset (hard cap of 4)
    validate_max=True,    # If True, the formset will raise a validation error if more than max_num forms are submitted
    can_delete=False        # If True, adds a checkbox to each form to allow deletion — here it's False because all 4 vertices should be allocated, not deleted

)