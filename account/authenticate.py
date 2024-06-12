from django.contrib.auth.models import User


class EmailBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(
                email=username
            )  # the real mean of username in here is email!
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
