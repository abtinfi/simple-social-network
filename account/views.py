from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views import View
from .forms import UserRegisterForm, UserLogInForm, EditUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Relation
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

# Create your views here.


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_form = "account/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_form, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                username=cd["username"], email=cd["email"], password=cd["password"]
            )
            messages.success(request, "you registered successfuly", "success")
            return redirect("home:home")
        return render(request, self.template_form, {"form": form})


class UserLogInView(View):
    form_class = UserLogInForm
    template_name = "account/login.html"

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next", None)
        return super().setup(request, *args, **kwargs)

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
                if self.next:
                    return redirect(self.next)
                return redirect("home:home")
            messages.error(request, "username or password is wrong", "warning")
        return render(request, self.template_name, {"form": form})


class UserLogOutView(LoginRequiredMixin, View):
    # login_url = "/account/login/"
    def get(self, request):
        logout(request)
        messages.success(request, "user logout successfuly", "success")
        return redirect("home:home")


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        post = user.user_post.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(
            request,
            "account/profile.html",
            {"user": user, "posts": post, "is_following": is_following},
        )


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = "account/password_reset_form.html"
    success_url = reverse_lazy("account:password_reset_done")
    email_template_name = "account/password_reset_email.html"


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "account/password_reset_done.html"


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("account:password_reset_complete")


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, "you already follow this user", "danger")

        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, "you successfuly follow this user", "success")

        return redirect("account:user_profile", user_id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, "you successfuly unfollow this user", "success")

        else:
            messages.error(request, "you are not following this user", "danger")

        return redirect("account:user_profile", user_id)


class EditUserView(LoginRequiredMixin, View):
    form_class = EditUserForm

    def get(self, request):
        form = self.form_class(
            instance=request.user.profile, initial={"email": request.user.email}
        )
        return render(request, "account/edit_profile.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data["email"]
            request.user.save()
            messages.success(request, "edited success", "success")
        return redirect("account:user_profile", request.user.id)
        pass
