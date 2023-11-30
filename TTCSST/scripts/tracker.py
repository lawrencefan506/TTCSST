#This file contains the main tracker code 
import requests
from datetime import datetime 
from main import models as db

#HELPER FUNCTIONS
#converts epoch to datetime
def getUpdatedAtTime(epoch):
    return (datetime.fromtimestamp(epoch/1000)).strftime('%Y-%m-%d %H:%M')

#iterates through all the bus locations, returning list of potential special sightings.
def findSpecials(busLocations):
    specials = []
    for bus in busLocations:
        if 'dirTag' in bus.keys(): #sometimes this is missing, so check it to prevent errors 
            busRoute = bus['routeTag']            
            if bus['id'][0] == '4': 
                continue #ignore streetcars
            else:
                busNum = bus['id']
            dirTag = bus['dirTag']
        else:
            continue

        #Query the db to determine if route garage != bus garage
        routeGarages = list(db.routeAllocations.objects.filter(route=busRoute).values_list('garage',flat=True))
        busGarage = list(db.busAllocations.objects.filter(busNumber=busNum).values_list('garage',flat=True))
        if busGarage[0] not in routeGarages:
            specials.append({'bus':busNum, 'route':busRoute, 'dirTag':dirTag})
    
    return specials


#main tracker code. Returns time that API was last updated at and dict of special sightings. 
def tracker(): 
    response = requests.get("https://webservices.umoiq.com/service/publicJSONFeed?command=vehicleLocations&a=ttc")
    
    if response.status_code == 200:
        data = response.json()
        busLocations = data.get('vehicle')
        
        time = getUpdatedAtTime(int(data.get('lastTime')['time']))
        specials = findSpecials(busLocations)


        






    return time, specials
    