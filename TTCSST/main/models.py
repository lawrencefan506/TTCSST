from django.db import models

# Create your models here.

class busAllocations(models.Model):
    busNumber = models.IntegerField(primary_key=True)
    garage = models.CharField(max_length=50)
    artic = models.BooleanField(default=False) #Artic special sightings for a later phase in the project 
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.busNumber}"
    
    class Meta:
        verbose_name_plural = "Bus Allocations" #Removes trailing s in admin page

class routes(models.Model):
    routeNumber = models.IntegerField(primary_key=True)
    routeName = models.CharField(max_length=100)
    artic = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.routeNumber}"    
    
    class Meta:
        verbose_name_plural = "Routes" 

class routeAllocations(models.Model):
    route = models.ForeignKey(routes, on_delete=models.CASCADE)
    garage = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.route}"

    class Meta:
        unique_together = ['route', 'garage']
        verbose_name_plural = "Route Allocations" #Removes trailing s in admin page

#Display historical Special Sightings in this DB
class specialSightings(models.Model):
    busNumber = models.ForeignKey(busAllocations, on_delete=models.PROTECT) #PROTECT: buses should never be deleted
                                                                            #Need to take into account reusing of numbers for the future...
    busGarage = models.CharField(max_length=50)
    runNumber = models.ForeignKey(routes, on_delete=models.PROTECT)
    runGarage = models.CharField(max_length=50)
    datetime = models.DateTimeField(auto_now_add=True) # Set to True if you want to set the date and time to the current date and time only when the object is created.

    class Meta:
        verbose_name_plural = "Special Sightings"    