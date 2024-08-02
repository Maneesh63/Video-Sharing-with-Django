# video/backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class UsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        print(f"Authenticating username: {username}")  # Debugging output
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            print("User does not exist")  # Debugging output
            return None
        else:
            if user.check_password(password):
                print("Password is correct")  # Debugging output
                return user
            else:
                print("Password is incorrect")  # Debugging output
        return None
