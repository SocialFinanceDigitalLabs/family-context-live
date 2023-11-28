from decouple import config

from family_context.settings.base import INSTALLED_APPS, MIDDLEWARE

# Check if setting is set to allow this to run behind a load balancer
LOAD_BALANCER_SSL = config("LOAD_BALANCER_SSL", default=False, cast=bool)
if LOAD_BALANCER_SSL:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_ON_GET = True
COGNITO_DOMAIN = config("AWS_COGNITO_DOMAIN", default=False)
AWS_REGION = config("AWS_REGION", default=False)
COGNITO_CLIENT_ID = config("AWS_COGNITO_APP_CLIENT_ID", default=False)
COGNITO_CLIENT_SECRET = config("AWS_COGNITO_APP_CLIENT_SECRET", default=False)

SSO_USED = COGNITO_DOMAIN and AWS_REGION and COGNITO_CLIENT_ID and COGNITO_CLIENT_SECRET

if SSO_USED:
    SOCIALACCOUNT_PROVIDERS = {
        "amazon_cognito": {
            "APP": {
                "client_id": COGNITO_CLIENT_ID,
                "secret": COGNITO_CLIENT_SECRET,
            },
            "SCOPE": {"aws.cognito.signin.user.admin", "openid", "email"},
            "DOMAIN": COGNITO_DOMAIN,
        }
    }
    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
        "allauth.account.auth_backends.AuthenticationBackend",
    )
    MIDDLEWARE.append("allauth.account.middleware.AccountMiddleware")
    INSTALLED_APPS.append("allauth")
    INSTALLED_APPS.append("allauth.account")
    INSTALLED_APPS.append("allauth.socialaccount")
    INSTALLED_APPS.append("allauth.socialaccount.providers.amazon_cognito")
else:
    AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)
