from django.db import models
from django.utils.translation import gettext_lazy as _


class State(models.Model):
    title = models.CharField(_("title"), max_length=150)

    def __unicode__(self):
        return f"{self.title}"

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("state")
        verbose_name_plural = _("states")


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name=_("state"), blank=True, null=True)
    title = models.CharField(_("title"), max_length=150)

    def __unicode__(self):
        return f"{self.title}"

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")
