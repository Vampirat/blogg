from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class EmailAuthBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        model = get_user_model()
        try:
            user = model.objects.get(email=username)
            if user.check_password(password):
                return user
        except (model.DoesNotExist, model.MultipleObjectsReturned):
            return None
        
    def get_user(self, user_id):
        model = get_user_model()
        try:
            return model.objects.get(pk=user_id)
        except model.DoesNotExist:
            return None