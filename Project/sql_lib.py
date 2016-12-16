from django.contrib.auth.models import User

class SQLBase:
    def Create_User(self,info):
        user = User.objects.create_user(str(info['login']), str(info['email']), str(info['password']))
        user.first_name = str(info['name'])
        user.last_name = str(info['surname'])
        user.save()
