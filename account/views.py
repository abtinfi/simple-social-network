from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.


class RegisterView(View):
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
