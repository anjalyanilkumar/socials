from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from socials.models import Profile, Posts, Comments

class UserForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'email',
                  'username',
                  'password1',
                  'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location','profile_pic')

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class PostsForm(forms.ModelForm):
    class Meta():
        model=Posts
        fields=[
            "caption",
            "images"
        ]
        
        widgets={
            "caption":forms.Textarea(attrs={"class":"form-control border border-warning mt-2","rows":3,"placeholder":"write a caption .."}),
            "images":forms.FileInput(attrs={"class":"form-select mt-2"})
        }

class ProfileForm(forms.ModelForm):
     class Meta:
        model = Profile
        fields = ['bio',
                  'profile_pic',
                 
                  ]

        widgets ={
            'bio' : forms.TextInput(attrs={'class' :'form-control','placeholder':'write a bio'}),
            'profile_pic' : forms.FileInput(attrs={'class' : 'form-control'}),
            
        }