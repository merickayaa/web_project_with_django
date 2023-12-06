from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class UserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        if username is None:
            username = kwargs.get('student_no')

        users = User._default_manager.filter(Q(student_no= str(username)) | Q(username= str(username)))
        # Test whether any matched user has the provided password:
        for user in users:
            if user.check_password(password):
            
                return user

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None