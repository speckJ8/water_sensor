from django.contrib import admin

from .models import *

admin.site.register(Reservoir)
admin.site.register(FlowPoint)
admin.site.register(Measurement)
admin.site.register(Pump)
admin.site.register(Connection)
admin.site.register(PumpConnection)