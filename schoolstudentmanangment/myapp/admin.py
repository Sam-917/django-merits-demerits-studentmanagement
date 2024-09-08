from django.contrib import admin
from myapp.models import *

# register models to admin interface to view, edit, add and delete instances of models in admin interfaces
admin.site.register([MeritStudent, DemeritStudent, Class, Grade])