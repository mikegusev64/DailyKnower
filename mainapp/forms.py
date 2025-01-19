from django.forms import ModelForm

from django.contrib.auth.forms import User



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']