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

  strRange = models.CharField(max_length=64, unique=True)

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
  otherApp = models.ForeignKey(App, related_name='lostEntries')
  chosenApp = models.ForeignKey(App, related_name='wonEntries')
  explanation = models.TextField('Briefly justify your choice.')

  def __unicode__(self):
    return self.chosenApp.name + ' was chosen.' 

class AppEntryRecord(models.Model):
  entry = models.ForeignKey(AppEntry, unique=True)
  person = models.ForeignKey(PersonEntry)
  timeMade = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return 'record for app entry ' + str(self.entry.id) 


class AppPair(models.Model):
  app1 = models.ForeignKey(App, related_name='appPair1Entries')
  app2 = models.ForeignKey(App, related_name='appPair2Entries')

  def __unicode__(self):
    return self.app1.name + ' compared with ' + self.app2.name

class Constant(models.Model):
  name = models.CharField(max_length=32, unique=True)
  value = models.IntegerField()

  def __unicode__(self):
    return self.name + ': ' + str(self.value)

class ScoreRecord(models.Model):
  person = models.ForeignKey(PersonEntry, related_name='scoreRecord', unique=True)
  correct = models.IntegerField()
  total = models.IntegerField()
  hash = models.CharField(max_length=64)
  timeMade = models.DateTimeField(auto_now_add=True)
  

  def __unicode__(self):
    return 'Score of ' + str(self.correct) + ' / ' + str(self.total) + ' recorded.'

