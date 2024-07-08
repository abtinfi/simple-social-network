from django import forms
from account.models import Post


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("body",)
