from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

YES = 'Y'
NO = 'N'
DOUBT = '?'
YES_NO_DOUBT = (
    (YES, _('ja')),
    (NO, _('nee')),
    (DOUBT, _('twijfel')),
)

@python_2_unicode_compatible
class Setting(models.Model):
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    is_local = models.BooleanField(default=False)
    needs_details = models.BooleanField(default=False)
    needs_supervision = models.BooleanField(default=False)
    requires_review = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']
        verbose_name = _('Setting')

    def __str__(self):
        return self.description

class SettingModel(models.Model):
    setting = models.ManyToManyField(
        Setting,
        verbose_name=_('Geef aan waar de dataverzameling plaatsvindt'))
    setting_details = models.CharField(
        _('Namelijk'),
        max_length=200,
        blank=True)
    supervision = models.NullBooleanField(
        _('Vindt het afnemen van de taak plaats onder het toeziend oog \
van de leraar of een ander persoon die bevoegd is?')
    )
    leader_has_coc = models.NullBooleanField(
        _('Is de testleider in het bezit van een VOG?'),
        help_text=_('Iedereen die op een school werkt moet in het bezit \
        zijn van een Verklaring Omtrent Gedrag (VOG, zie \
        <a href="https://www.justis.nl/producten/vog/" \
        target="_blank">https://www.justis.nl/producten/vog/</a>). \
        Het is de verantwoordelijkheid van de school om hierom te vragen. \
        De ETCL neemt hierin een adviserende rol en wil de onderzoekers \
        waarschuwen dat de school om een VOG kan vragen.')
    )

    class Meta:
        abstract = True
