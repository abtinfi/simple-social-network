from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created", "slug"]

    def __str__(self):
        return f"{self.slug} - {self.updated}"

    def get_absolute_url(self):
        return reverse("home:post_detail", args=[self.id, self.slug])

    def like_count(self):
        return self.pvotes.count()

    def user_can_like(self, user):
        user_like = user.uvotes.filter(post=self)
        if user_like.exists():
            return True
        return False


class Relation(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    def __str__(self):
        return f"{self.from_user} following {self.to_user}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ucomment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pcomment")
    reply = models.ForeignKey(
        "self", on_delete=models.CASCADE, name="rcomment", blank=True, null=True
    )
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.body[:30]}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uvotes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pvotes")

    def __str__(self):
        return f"{self.user} liked {self.post.slug}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(null=True, blank=True)
    pass


