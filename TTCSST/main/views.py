from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("<h1>Welcome to TTC Special Sightings Tracker</h1>")

def allocations(request):
    return HttpResponse("<h1>Current Allocations</h1>")

def history(request):
    return HttpResponse("<h1>History of Special Sightings</h1>")