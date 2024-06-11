from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, UserLogInForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_form = "account/register.html"

    def get(self, request):
        form = self.form_class()

        return render(request, self.template_form, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(
                username=cd["username"], email=cd["email"], password=cd["password"]
            )
            messages.success(request, "you registered successfuly", "success")
            return redirect("home:home")
        return render(request, self.template_form, {"form": form})


class UserLogInView(View):
    form_class = UserLogInForm
    template_name = "account/login.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                login(request, user)
                messages.success(request, "user login successfuly", "success")
                return redirect("home:home")
            messages.error(request, "username or password is wrong", "warning")
        return render(request, self.template_name, {"form": form})


class UserLogOutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "user logout successfuly", "success")
        return redirect("home:home")
