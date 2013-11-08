#
# URLs for main survey app.
#

from django.conf.urls.defaults import *

urlpatterns = patterns('survey.views',
    # main links.
    (r'^$', 'index'),
    (r'^letsDoThis/?$', 'doQuiz'),
    (r'^beginQuestionnaire/?$', 'personData'),
)

