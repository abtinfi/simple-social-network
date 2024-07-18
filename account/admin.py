from django.contrib import admin
from .models import Post, Relation, Comment, Vote, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.
class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False


class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInLine,)


admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "slug", "updated"]
    search_fields = ["slug", "body"]
    list_filter = ["updated"]
    prepopulated_fields = {"slug": ["body"]}
    raw_id_fields = ["user"]


admin.site.register(Relation)
admin.site.register(Vote)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created", "is_reply"]
    raw_id_fields = ["user", "post", "rcomment"]

