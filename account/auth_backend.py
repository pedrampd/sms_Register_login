from .models import User
class backend:
    def authenticate(self,phone=None,password=None):
        try:
            user = User.objects.get(phone=phone)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self,phone):
        try:
            return User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None
