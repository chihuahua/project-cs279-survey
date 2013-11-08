#
# Contains forms for the app.
#

from django.forms import ModelForm
import models

class AppEntryForm(ModelForm):
  class Meta:
    model = models.AppEntry

class PersonForm(ModelForm):
  class Meta:
    model = models.PersonEntry

