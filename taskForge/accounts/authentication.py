from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class EmailOrUserBackend(ModelBackend):
    """
    Allows users to login with either a username or email
    Shamelessly appropriated from our esteemed lecturer
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                try:
                    user = UserModel.objects.get(username=username)
                except UserModel.DoesNotExist:
                    return None
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception:
            return None