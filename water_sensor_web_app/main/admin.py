from django.contrib import admin

from .models import *

admin.site.register(Reservoir)
admin.site.register(FlowPoint)
admin.site.register(Measurement)