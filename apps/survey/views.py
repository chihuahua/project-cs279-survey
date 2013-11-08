#
# Views for the main survey app.
#

import models, forms, random
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def doQuiz(request):
  '''
  Renders the questionnaire.
  '''
  appIndex = -1
  if 'personId' not in request.session and 'personIdOverride' not in request.GET:
    # person has not entered personal information yet.
    return personData(request)

  if request.method == 'POST' and request.POST['purpose'] == 'appEval':
    # form just submitted.
    appIndex = int(request.POST['appIndex'])
    form = forms.AppEntryForm(request.POST)
    if form.is_valid() and 'personIdOverride' not in request.GET:
      # record this entry.
      entry = form.save()
      app = models.App.objects.get(pk = appIndex)
      personId = request.session['personId']
      person = models.PersonEntry.objects.get(pk = personId)
      record = models.AppEntryRecord(
          app = app,
          entry = entry,
          person = person
        )
      record.save()
      form = forms.AppEntryForm()
  else:
    form = forms.AppEntryForm()

  # retrive a random app.
  allApps = models.App.objects.all()
  if appIndex < 0:
    lastAppIndex = allApps.count() - 1
    appIndex = random.randint(0, lastAppIndex)
    if 'avoid' in request.GET:
      indexToAvoid = int(request.GET['avoid'])
      while appIndex == indexToAvoid:
        appIndex = random.randint(0, lastAppIndex)
  app = allApps[appIndex]

  return render_to_response('quiz.html', {
        'app': app,
        'form': form
      }, context_instance=RequestContext(request)
    )

def index(request):
  '''
  Renders response for home page.
  '''
  return render_to_response('home.html')

def personData(request):
  '''
  Collects data about a person.
  '''
  if 'personId' in request.session:
    # user already did the personal survey.
    return doQuiz(request)

  errors = None
  if request.method == 'POST':
    form = forms.PersonForm(request.POST)
    if form.is_valid():
      # valid personal information filled out.
      personData = models.PersonEntry(
          phoneUsage = form.cleaned_data['phoneUsage'],
          downloadApps = form.cleaned_data['downloadApps'],
          useApps = form.cleaned_data['useApps'],
          age = form.cleaned_data['age'],
          gender = form.cleaned_data['gender'],
          country = form.cleaned_data['country']
        )
      personData.save()
      request.session['personId'] = personData.id
      return doQuiz(request)

    # form is not valid. 
    errors = "Please fill out all information."
  else:
    form = forms.PersonForm()
  return render_to_response(
      'person.html',
      {'form': form, 'errors': errors},
      context_instance=RequestContext(request)
    )

