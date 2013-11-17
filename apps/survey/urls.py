#
# URLs for main survey app.
#

from django.conf.urls.defaults import *

urlpatterns = patterns('survey.views',
    # main links.
    (r'^$', 'index'),
    (r'^choseApp', 'choseApp'),
    (r'^letsDoThis/?$', 'doQuiz'),
    (r'^beginQuestionnaire/?$', 'personData'),
    (r'^informedConsent/?$', 'informedConsent'),
    (r'^score/(?P<scoreHash>\w+)/?$', 'viewScore'),
)

