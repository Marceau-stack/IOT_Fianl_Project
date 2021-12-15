from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
import socket
import os
import json
from .forms import LoginForm, RegForm, LoginFormVoice, AddrForm
from speaker_recognition import Recognizer
from preference.models import Preference

train_path = "train"
test_path = "test"
model_path = "model.out"
recognizer = Recognizer(train_path + "/*", test_path + "/*", model_path)


def home(request):
    if request.method == "POST":
        addr_form = AddrForm(request.POST)
        if addr_form.is_valid():
            preference = Preference.objects(username=request.user.username)[0]
            information = preference.to_json()
            print(information)
            ip = addr_form.cleaned_data["ip"]
            port = addr_form.cleaned_data["port"]
            s = socket.socket()
            s.connect((ip, port))
            s.send(information.encode())
            s.close()
    else:
        addr_form = AddrForm()
    context = {
        "addr_form": addr_form
    }
    return render(request, "home.html", context)


def login_pwd(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data["user"]
            auth.login(request, user)
            return redirect(request.GET.get("from", reverse("home")))
    else:
        login_form = LoginForm()
    context = {
        "login_form": login_form
    }
    return render(request, "login.html", context)


def login_voice(request):
    if request.method == "POST":
        login_form = LoginFormVoice(request.POST, request.FILES)
        if login_form.is_valid():
            file = login_form.cleaned_data["recording"]
            dir_name = test_path + "/"
            handle_upload_file(file, dir_name)

            username = recognizer.task_predict()
            user = User.objects.get(username=username)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            return redirect("home")
    else:
        login_form = LoginFormVoice()
    context = {
        "login_form": login_form
    }
    return render(request, "login_voice.html", context)


def register(request):
    if request.method == "POST":
        reg_form = RegForm(request.POST, request.FILES)
        if reg_form.is_valid():
            username = reg_form.cleaned_data["username"]
            password = reg_form.cleaned_data["password"]
            file = reg_form.cleaned_data["recording"]
            dir_name = train_path + "/" + username + "/"
            handle_upload_file(file, dir_name)

            user = User()
            user.username = username
            user.set_password(password)
            user.save()

            preference = Preference()
            preference.username = username
            preference.save()

            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            recognizer.task_enroll()
            return redirect("home")
    else:
        reg_form = RegForm()
    context = {
        "reg_form": reg_form
    }
    return render(request, "register.html", context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get("from", reverse("home")))


def handle_upload_file(f, dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    with open(dir_name + f.name, "wb") as destination:
        for chunk in f.chunks():
            destination.write(chunk)




