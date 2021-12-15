from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Enter Username"
                   }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control",
                   "placeholder": "Enter Password"
                   }
        )
    )

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Username or password is incorrect")
        else:
            self.cleaned_data["user"] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Enter Username"
                   }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control",
                   "placeholder": "Enter Password"
                   }
        )
    )

    recording = forms.FileField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username


class LoginFormVoice(forms.Form):
    recording = forms.FileField()


class AddrForm(forms.Form):
    ip = forms.CharField(
        label="Raspberry pi's IP address",
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Enter IP address"}
        )
    )
    port = forms.IntegerField(
        label="Port number",
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Enter port number"}
        )
    )
