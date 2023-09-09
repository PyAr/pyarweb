from allauth.account.forms import SignupForm
from captcha.fields import CaptchaField, CaptchaTextInput


class CustomCaptchaTextInput(CaptchaTextInput):
    # HACK - No entiendo por qué esto apunta a community/templates y no al /templates en el root
    template_name = "account/custom_captcha.html"


class SignupFormWithCaptcha(SignupForm):
    captcha = CaptchaField(widget=CustomCaptchaTextInput)
