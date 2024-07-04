from allauth.account.forms import LoginForm, SignupForm


class EtnaLoginForm(LoginForm):
    def login(self, *args, **kwargs):
        return super(EtnaLoginForm, self).login(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["login"].error_messages = {
            "required": "The email field is required"
        }

        self.fields["password"].error_messages = {
            "required": "The password field is required"
        }

class EtnaSignupForm(SignupForm):
    def save(self, request):
        user = super(EtnaSignupForm, self).save(request)

        return user