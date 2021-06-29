from django.contrib.auth.mixins import UserPassesTestMixin


class MyTestUserPassesTest(UserPassesTestMixin): #czy nalezy do jakiejs grupy

    def test_func(self):
        if self.request.user.profil is not None: #czy patient istnieje u user
            return True
        return False