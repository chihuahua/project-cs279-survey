from django.db import models
import appData, personData

class App(models.Model):
  '''
  A single app.
  '''

  name = models.CharField(max_length=64)
  genre = models.CharField(max_length=64)
  iconUrl = models.CharField(max_length=256)
  downloads = models.CharField(max_length=64)
  updateDate = models.DateField()
  description = models.TextField()

  def __unicode__(self):
    return self.name + ' (' + self.genre + ')'

class DownloadCategory(models.Model):
  '''
  Category of number of downloads.
  '''

  strRange = models.CharField(max_length=64)

  def __unicode__(self):
    return self.strRange

class PersonEntry(models.Model):
  '''
  Data on a single subject.
  '''

  phoneUsage = models.CharField('How often do you use your phone?', max_length=64, choices=personData.USAGE_CHOICES)
  downloadApps = models.CharField('How often do you download apps onto your smartphone?', max_length=64, choices=personData.USAGE_CHOICES)
  useApps = models.CharField('How often do you use apps on your smartphone?', max_length=64, choices=personData.USAGE_CHOICES)
  age = models.CharField('How old are you?', max_length=64, choices=personData.AGE_CHOICES)
  gender = models.CharField('What\'s your gender?', max_length=64, choices=personData.SEX_CHOICES)
  country = models.CharField('Which country are you from?', max_length=64, choices=personData.COUNTRIES)

  def __unicode__(self):
    return 'person with id ' + str(self.id)

class AppEntry(models.Model):
  '''
  Data on a subject's analysis of an app. 
  '''
  nameClear = models.IntegerField('Does the app\'s name clearly indicate what the app does?', choices=appData.LIKERT_SCALE)
  nameExciting = models.IntegerField('Is the app\'s name exciting?', choices=appData.LIKERT_SCALE)
  iconFun = models.IntegerField('Does the icon look fun?', choices=appData.LIKERT_SCALE)
  iconTrust = models.IntegerField('Based on the icon, do you trust this app?', choices=appData.LIKERT_SCALE)
  iconEnticing = models.IntegerField('Is the icon enticing?',  choices=appData.LIKERT_SCALE)
  description = models.IntegerField('Based on the description, would you trust this app?', choices=appData.LIKERT_SCALE)
  trustApp = models.IntegerField('Do you trust this app?', choices=appData.LIKERT_SCALE)
  
  def __unicode__(self):
    return 'analysis of an app'

class AppEntryRecord(models.Model):
  app = models.ForeignKey(App)
  entry = models.ForeignKey(AppEntry)
  person = models.ForeignKey(PersonEntry)
  timeMade = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return 'record for app entry ' + str(entry.id) 


