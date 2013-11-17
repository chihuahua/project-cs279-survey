#
# Views for the main survey app.
#

import models, forms, os, random
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
import django.core.exceptions

def clearSession(request):
  '''
  Clears a session. Redirects to home page.
  '''
  del request.session['personId']
  del request.session['total']
  del request.session['correct']
  return index(request)

def doQuiz(request, randomApp=False, showResultFor=None):
  '''
  Renders the questionnaire.
  @param randomApp Whether to chose random apps.
  @param showResultFor Pair of apps to show results for. Chosen
      app appears first. The third item is the person entry.
  '''
  appIndex = -1
  if 'personId' not in request.session and 'personIdOverride' not in request.GET:
    # person has not entered personal information yet.
    return personData(request)

  if 'correct' not in request.session or 'total' not in request.session:
    return clearSession(request)

  # generate a new app?
  if 'gen' in request.GET and request.GET['gen'] == '1':
    randomApp = True

  # retrive a pair of apps.
  if randomApp:
    # chose a random app.
    allPairs = models.AppPair.objects.all()
    numAppPairs = allPairs.count()
    appPairId = random.randint(1, numAppPairs)
  else:
    # chose the next pair of apps.
    appPairId = models.Constant.objects.get(name="currentComparisonPk").value

  apps = models.AppPair.objects.get(pk=appPairId)

  results = None
  scoreCurrent = None
  if showResultFor:
    # show the results for the last comparison.
    chosenApp = showResultFor[0]
    otherApp = showResultFor[1]
    downloadCat1 = models.DownloadCategory.objects.get(strRange=chosenApp.downloads)
    downloadCat2 = models.DownloadCategory.objects.get(strRange=otherApp.downloads)
    if downloadCat1 > downloadCat2:
      correct = 1
      request.session['correct'] += 1
      request.session['total'] += 1
    elif downloadCat1 < downloadCat2:
      correct = -1
      request.session['total'] += 1
    else:
      correct = 0
    
    # update the score recorded.
    scoreRecord = showResultFor[2].scoreRecord.all()[0]
    scoreRecord.correct = request.session['correct']
    scoreRecord.total = request.session['total']
    scoreRecord.save()
    
    results = (chosenApp, otherApp, correct)
    scoreCurrent = {}
    scoreCurrent['correct'] = request.session['correct']
    scoreCurrent['total'] = request.session['total']
    scoreCurrent['percent'] = 100 * float(request.session['correct']) / request.session['total']
    scoreCurrent['record'] = scoreRecord

  return render_to_response('quiz.html', {
        'apps': apps,
        'results': results,
        'score': scoreCurrent
      }, context_instance=RequestContext(request))

def choseApp(request):
  '''
  Choses a specific app over another one.
  '''
  if request.method != "POST":
    return doQuiz(request, randomApp=True)

  # find the 2 apps.
  chosenAppId = int(request.POST['chosenApp'])
  try:
    chosenApp = models.App.objects.get(pk=chosenAppId)
  except django.core.exceptions.ObjectDoesNotExist:
    return doQuiz(request, randomApp=True)

  otherAppId = int(request.POST['otherApp'])
  try:
    otherApp = models.App.objects.get(pk=otherAppId)
  except django.core.exceptions.ObjectDoesNotExist:
    return doQuiz(request, randomApp=True)

  # find the person.
  if 'personId' not in request.session or 'correct' not in request.session or 'total' not in request.session:
    return clearSession(request)

  try:
    person = models.PersonEntry.objects.get(pk=request.session['personId'])
  except django.core.exceptions.ObjectDoesNotExist:
    return clearSession(request)

  # make an app entry
  appEntry = models.AppEntry(
      otherApp = otherApp,
      chosenApp = chosenApp,
      explanation = request.POST['explanation']
    )
  appEntry.save()

  # make an app entry record.
  appEntryRecord = models.AppEntryRecord(
      entry = appEntry,
      person = person
    )
  appEntryRecord.save()

  # increase the current app pair ID.
  appPairId = models.Constant.objects.get(name="currentComparisonPk")
  appPairId.value = appPairId.value + 1
  if appPairId.value > models.AppPair.objects.count():
    appPairId.value = 1
  appPairId.save()

  # redirect to the main page.
  return doQuiz(request, showResultFor=(chosenApp, otherApp, person))

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

      # score is A / Total.
      request.session['correct'] = 0
      request.session['total'] = 0

      # create an entry to record the score.
      scoreRecord = models.ScoreRecord(
          person = personData,
          correct = request.session['correct'],
          total = request.session['total'],
          hash = os.urandom(16).encode('hex')
        )
      scoreRecord.save()

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

def informedConsent(request):
  return render_to_response(
      'informedConsent.html',
  )

def viewScore(request, scoreHash=None):
  '''
  Displays a score.
  '''
  if not scoreHash:
    return index(request)

  try:
    score = models.ScoreRecord.objects.get(hash=scoreHash)
  except django.core.exceptions.ObjectDoesNotExist:
    return index(request)

  percent = 100. * score.correct / score.total
  return render_to_response(
      'viewScore.html', {
        'percent': percent,
        'score': score,
      }
  )

