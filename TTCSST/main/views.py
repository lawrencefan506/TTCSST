from django.shortcuts import render, HttpResponse
from scripts import tracker

# Create your views here.
def home(response):

    time, specials = tracker.tracker()

    return render(response, "main/home.html", {"updateTime": time,
                                               "specials": specials
                                               })

def allocations(request):
    return HttpResponse("<h1>Current Allocations</h1>")

def history(request):
    return HttpResponse("<h1>History of Special Sightings</h1>")