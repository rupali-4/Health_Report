from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Multiuser

class Loginform(forms.Form):
    # create text input for username
    username = forms.CharField(    # creates a form field for accepting text input, It’s required by default
        widget= forms.TextInput(    # widget controls how the input will be rendered in HTML, By default, CharField uses TextInput, but customizing it
            attrs= {              # adds HTML attributes to the input field
                'class': 'form-control',   # applies a CSS class
                'required': True
            }
        )
    )   # in html render: <input type="text" name="username" class="form-control"> 
        # name="username"= Connects HTML input to Django form field hence need to be same in both

    password = forms.CharField(
        widget= forms.PasswordInput(
            attrs= {
                'class': 'form-control'
            }
        )
    )  
  
class Registerform(UserCreationForm):
    role = forms.ChoiceField(
        choices= Multiuser.ROLE_CHOICES,
        label="Select Your Role",
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'height: 30px; width: 230px;'})
    )
    security_question = forms.CharField(max_length=255)
    security_answer = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:   # specify model & fields
        model = Multiuser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'security_question', 'security_answer']

    def __init__(self, *args, **kwargs):   # Called when the form is created
        super(Registerform, self).__init__(*args, **kwargs)  #  initializes the default form behavior
        for field_name in self.fields:  
            self.fields[field_name].widget.attrs['class'] = 'form-control'      
        #  loop goes through all form fields and adds the Bootstrap class form-control to each field's widget


class CustomForgotPasswordForm(forms.Form):
    username = forms.CharField(label="Username")

    # This will be filled later only if username is valid
    security_answer = forms.CharField(label="Answer", required=False, widget=forms.PasswordInput)
    
    # New password fields will appear only after valid answer
    new_password = forms.CharField(label="New Password", required=False, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", required=False, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_pass = cleaned_data.get("new_password")
        confirm_pass = cleaned_data.get("confirm_password")

        # If both are present and don't match, raise error
        if new_pass and confirm_pass and new_pass != confirm_pass:
            self.add_error('confirm_password', "Passwords do not match.")

      