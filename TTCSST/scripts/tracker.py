#This file contains the main tracker code 
import requests
import random
from datetime import datetime 
from main import models as db

#HELPER FUNCTIONS
#converts epoch to datetime
def getUpdatedAtTime(epoch):
    return (datetime.fromtimestamp(epoch/1000)).strftime('%Y-%m-%d %H:%M')

#given a bus #, route, and its dirTag, find the run number the bus is operating on. Also return the headsign
def getRun(bus, route, dirTag):
    print(bus, route, dirTag)
    #Use routeConfig API to get the stop tags of the dirTag
    #2 scenarios. 1) The dirTag is found so we can narrow down the stop tags
    #             2) The dirTag isn't found so we need to search all of the route's stop tags
    response = requests.get("https://retro.umoiq.com/service/publicJSONFeed?command=routeConfig&a=ttc&r=" + route)
    if response.status_code == 200:
        routeConfigData = response.json()

        dirTagFound = False        
        for x in routeConfigData['route']['direction']:
            if x['tag'] == dirTag: #Scenario 1
                stopTags = [y['tag'] for y in x['stop']]
                dirTagFound = True
                break
        
        if not dirTagFound: #Scenario 2 
            stopTags = [x['tag'] for x in routeConfigData['route']['stop']]

    else:
        raise Exception("Unsuccessful response")        

    #Use the stop tags in the predictions API to look for the bus 
    #Scenario 1
    if dirTagFound:
        for i in range(len(stopTags)-1, -1, -3): #use step -3 to look through the stops faster
            response = requests.get("https://retro.umoiq.com/service/publicJSONFeed?command=predictions&a=ttc&r=" + route + "&s=" + stopTags[i])
            if response.status_code == 200:
                predictionsData = response.json()
                if 'direction' in predictionsData['predictions'].keys():
                    for x in predictionsData['predictions']['direction']['prediction']:
                        if x['vehicle'] == bus:
                            return x['block'], predictionsData['predictions']['direction']['title'] #latter is the headsign
            else:
                raise Exception("Unsuccessful response")
    #Scenario 2
    else:
        random.shuffle(stopTags) #Shuffle randomly to increase chances of finding the bus quicker
        for stopTag in stopTags: 
            response = requests.get("https://retro.umoiq.com/service/publicJSONFeed?command=predictions&a=ttc&r=" + route + "&s=" + stopTag)
            if response.status_code == 200:
                predictionsData = response.json()
                if 'direction' in predictionsData['predictions'].keys():
                    for x in predictionsData['predictions']['direction']['prediction']:
                        if x['vehicle'] == bus:
                            return x['block'], predictionsData['predictions']['direction']['title'] #latter is the headsign
            else:
                raise Exception("Unsuccessful response")
    return ''

#given the run number, get the next three departures
def getNextDepartures(run):
    pass

#iterates through all the bus locations, returning list of potential special sightings.
#the output is a list of dictionaries in this format:
"""
{
    'updatedAt': (datetime),
    'bus': (int),
    'busGarage': (str),
    'route': (int),
    'routeGarage': (str),
    'run': (str) #e.g. 169_1_10,
    'headsign': (str) #e.g. East - 52 Lawrence West towards Eglinton Station via Avenue Rd
    'nextDepartures': [{
                        'route': (int),
                        'startStop': (str),
                        'endStop': (str),
                        'startTime': (time) #time leaving the first stop
                      }] (list dict) 
}
"""
def iterateAPI(busLocations):
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
            run, headsign = getRun(busNum, busRoute, dirTag)
            
            #From the run, decide if we reject the special sighting (in cases of school specials)
            runRoute = run.split('_')[0]
            if runRoute != busRoute:
                runRouteGarages = list(db.routeAllocations.objects.filter(route=runRoute).values_list('garage',flat=True))
                if busGarage[0] in runRouteGarages:
                    continue #REJECT

            nextDepartures = getNextDepartures(run)

            
            specials.append({'bus':busNum, 'busGarage':busGarage, 'route':busRoute, 'routeGarage':routeGarages, 'dirTag':dirTag, 'run':run, 'headsign':headsign})
    
    return specials


#main tracker code. Returns time that API was last updated at and dict of special sightings. 
def tracker(): 
    response = requests.get("https://webservices.umoiq.com/service/publicJSONFeed?command=vehicleLocations&a=ttc")
    
    if response.status_code == 200:
        data = response.json()
        busLocations = data.get('vehicle')
        
        time = getUpdatedAtTime(int(data.get('lastTime')['time']))
        
        
        
        specials = iterateAPI(busLocations)

    else:
        raise Exception("Unsuccessful response")
        






    return time, specials
    