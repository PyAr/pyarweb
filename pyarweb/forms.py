from allauth.account.forms import SignupForm
from captcha.fields import CaptchaField, CaptchaTextInput


class CustomCaptchaTextInput(CaptchaTextInput):
    # HACK - No entiendo por qué esto apunta a community/templates y no al /templates en el root
    template_name = "account/custom_captcha.html"

    def image_url(self):
        # Agrego el "@2" para enviar un captcha con más resolucioón
        # https://django-simple-captcha.readthedocs.io/en/latest/advanced.html#captcha-2x-image
        return super().image_url().removesuffix("/") + "@2"


class SignupFormWithCaptcha(SignupForm):
    captcha = CaptchaField(widget=CustomCaptchaTextInput)
