from allauth.account.forms import SignupForm
from captcha.fields import CaptchaField


class SingupFormWithCaptcha(SignupForm):
    captcha = CaptchaField()
