from django.contrib import admin

# Register your models here.

from .models import ServerAllocation, ServerPing, ServerStatistic

admin.site.register(ServerAllocation)
admin.site.register(ServerPing)
admin.site.register(ServerStatistic)