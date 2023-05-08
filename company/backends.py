from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

CustomUser = get_user_model()

class EmailBackend(ModelBackend):
    def authentication(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(Q(username__iexact=username) | Q(email__iexact=username))

        except CustomUser.DoesNotExist:
            CustomUser().set_password(password)
            return
        
        except CustomUser.MultipleObjectsReturned:
            user = CustomUser.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('-id').first()

            if user.check_password(password) and self.user_can_authenticate(user):
                return user