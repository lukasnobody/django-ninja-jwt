from django.conf import settings
from django.db import models
from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from ..settings import api_settings

USER_MODELS = (
    apps.get_model(*model_path.split('.'))
    for model_path in api_settings.USER_MODELS
)
USER_MODELS_NAMES = [
    user_model.__name__ for user_model in USER_MODELS
]


class OutstandingToken(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)

    user_content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    user_object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('user_content_type', 'user_object_id')

    jti = models.CharField(unique=True, max_length=255)
    token = models.TextField()

    created_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = "ninja_jwt.token_blacklist" not in settings.INSTALLED_APPS
        ordering = ("user",)

    def __str__(self):
        return "Token for {} ({})".format(
            self.user,
            self.jti,
        )

    @property
    def user(self):
        model_class = self.content_type.model_class()
        if model_class.__name__ in USER_MODELS_NAMES:
            return self.content_object
        return None

    @user.setter
    def user(self, value):
        if isinstance(value, USER_MODELS):
            self.content_object = value
        elif value is None:
            self.content_object = None
        else:
            raise ValueError(f"The 'user' property can be only {USER_MODELS_NAMES} object")


class BlacklistedToken(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    token = models.OneToOneField(OutstandingToken, on_delete=models.CASCADE)

    blacklisted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = "ninja_jwt.token_blacklist" not in settings.INSTALLED_APPS

    def __str__(self):
        return "Blacklisted token for {}".format(self.token.user)
