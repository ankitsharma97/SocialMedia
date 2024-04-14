from django import forms
from .models import Post
from .models import UserProfile as SignUpForm

class SignUpForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    Confirm_Password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = SignUpForm
        fields = ['name', 'email', 'username', 'profile_pic', 'password', 'Confirm_Password', 'about']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Profile Picture'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter about information'}),
        }
        
        
        
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['img', 'video', 'desc']
        labels = {'img': 'Image', 'video': 'Video', 'desc': 'Description'}
        widgets = {
            'img': forms.FileInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
        }

# class SignUpForm(forms.Form):
#     name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}))
#     email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
#     username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
#     profile_pic = forms.ImageField(label='Profile Picture', widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Profile Picture'}))
#     password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
#     confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

