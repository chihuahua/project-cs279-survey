import sys, os, os.path

currentDirectory = os.getcwd()
sys.path.append(currentDirectory)
sys.path.append(os.path.join(currentDirectory, "apps"))
os.environ['DJANGO_SETTINGS_MODULE'] = "apps.settings"
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
