from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import Registration, RegistrationKind, SettingModel
from studies.models import Study


class Intervention(SettingModel):
    period = models.TextField(
        _('Wat is de periode waarbinnen de interventie plaatsvindt?'))
    amount_per_week = models.PositiveIntegerField(
        _('Hoe vaak per week vindt de interventiesessie plaats?'))
    duration = models.PositiveIntegerField(
        _('Wat is de duur van de interventie per sessie in minuten?'))

    has_prepost = models.BooleanField(
        _('Is er sprake van een voor- en een nameting?'),
        default=False)
    prepost_experimenter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Wie voert de voor- en nameting uit?'),
        blank=True,
        null=True)
    prepost_description = models.TextField(
        _('Geef een precieze beschrijving van de voor- en nameting'),
        blank=True)

    pre_duration = models.PositiveIntegerField(
        _('Wat is de duur van de voormeting (in minuten)?'),
        blank=True,
        null=True)
    pre_registrations = models.ManyToManyField(
        Registration,
        verbose_name=_('Hoe worden de gegevens bij de voormeting vastgelegd?'),
        related_name='pre_registrations',
        blank=True)
    pre_registrations_details = models.CharField(
        _('Namelijk'),
        max_length=200,
        blank=True)
    pre_registration_kinds = models.ManyToManyField(
        RegistrationKind,
        verbose_name=_('Kies het soort meting'),
        related_name='pre_registration_kinds',
        blank=True)
    pre_registration_kinds_details = models.CharField(
        _('Namelijk'),
        max_length=200,
        blank=True)

    post_duration = models.PositiveIntegerField(
        _('Wat is de duur van de nameting (in minuten)?'),
        blank=True,
        null=True)
    post_registrations = models.ManyToManyField(
        Registration,
        verbose_name=_('Hoe worden de gegevens bij de nameting vastgelegd?'),
        related_name='post_registrations',
        blank=True)
    post_registrations_details = models.CharField(
        _('Namelijk'),
        max_length=200,
        blank=True)
    post_registration_kinds = models.ManyToManyField(
        RegistrationKind,
        verbose_name=_('Kies het soort meting'),
        related_name='post_registration_kinds',
        blank=True)
    post_registration_kinds_details = models.CharField(
        _('Namelijk'),
        max_length=200,
        blank=True)

    experimenter = models.TextField(
        _('Wie voert de interventie uit?'))
    description = models.TextField(
        _('Geef een beschrijving van de experimentele interventie'))
    has_controls = models.BooleanField(
        _('Is er sprake van een controlegroep?'),
        default=False)
    controls_description = models.TextField(
        _('Geef een beschrijving van de controleinterventie'),
        blank=True)

    # References
    study = models.OneToOneField(Study)
