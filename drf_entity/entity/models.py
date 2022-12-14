from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Entity(models.Model):
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    value = models.IntegerField(default=0, verbose_name=_("value"))
    properties = models.ManyToManyField("Property")

    def __str__(self) -> str:
        return str(self.value)

    class Meta:
        verbose_name = _("Entity")
        verbose_name_plural = _("Entities")


class Property(models.Model):
    key = models.CharField(max_length=128, default="")
    value = models.CharField(max_length=128, default="")

    def __str__(self) -> str:
        return self.key

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")
