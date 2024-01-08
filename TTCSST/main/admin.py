from django.contrib import admin
from .models import *



#To make every column of the model appear in Django admin
class busAllocationsAdmin(admin.ModelAdmin):    
    list_display = ('busNumber', 'garage', 'artic', 'model') # List display to show all columns in the change list    
    search_fields = ('busNumber', 'garage', 'artic', 'model') # Search fields for easy searching in the admin interface  
    list_filter = ('garage', 'model')  
    ordering = ('busNumber',)

class routesAdmin(admin.ModelAdmin):
    list_display = ('routeNumber', 'routeName', 'artic')
    search_fields = ('routeNumber', 'routeName', 'artic')
    ordering = ('routeNumber',)

class routeAllocationsAdmin(admin.ModelAdmin):
    list_display = ('route', 'garage')
    search_fields = ('route', 'garage')
    list_filter = ('garage',)
    ordering = ('route__routeNumber',)

class specialSightingsAdmin(admin.ModelAdmin):
    list_display = ('busNumber', 'busGarage', 'runNumber', 'runGarage', 'datetime')
    search_fields = ('busNumber', 'busGarage', 'runNumber', 'runGarage', 'datetime')
    list_filter = ('busNumber', 'busGarage', 'runNumber', 'runGarage', 'datetime')
    ordering = ('-datetime', 'busNumber',)

# Register your models here.
admin.site.register(busAllocations, busAllocationsAdmin)
admin.site.register(routes, routesAdmin)
admin.site.register(routeAllocations, routeAllocationsAdmin)
admin.site.register(specialSightings, specialSightingsAdmin)