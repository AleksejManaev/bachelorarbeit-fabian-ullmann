from account.views import LoginView


class LoginView(LoginView):
    template_name = 'ldap_login.html'
