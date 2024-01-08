#This file contains the main tracker code 
import requests
import random
from datetime import datetime 
from main import models as db

#Params
RESPONSE_OK_CODE = 200  #Successful response code when querying the API
NUM_NEXT_DEPARTURES = 4  #Number of departures we want to return for a SS. Must be even.
DEF_START_DAY_TIME = 5  #Define the start hour of the day (e.g. if 5, the hours of the day are 5:00-29:00)

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
    if response.status_code == RESPONSE_OK_CODE:
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
            if response.status_code == RESPONSE_OK_CODE:
                predictionsData = response.json()
                if 'direction' in predictionsData['predictions'].keys():
                    if isinstance(predictionsData['predictions']['direction'], list):
                        for x in predictionsData['predictions']['direction']:
                            if isinstance(x["prediction"], list):
                                for y in x["prediction"]:
                                    if y["vehicle"] == bus:
                                        return y['block'], x['title'] #latter is the headsign
                            else:
                                if x["prediction"]["vehicle"] == bus:
                                        return x["prediction"]["block"], predictionsData['predictions']['direction']['title'] #latter is the headsign        
                    else:
                        if isinstance(predictionsData['predictions']['direction']['prediction'], list):
                            for x in predictionsData['predictions']['direction']['prediction']:
                                if x['vehicle'] == bus:
                                    return x['block'], predictionsData['predictions']['direction']['title'] #latter is the headsign
                        else:
                            if predictionsData['predictions']['direction']['prediction']['vehicle'] == bus:
                                return x['block'], predictionsData['predictions']['direction']['title'] #latter is the headsign
            else:
                raise Exception("Unsuccessful response")
    #Scenario 2
    else:
        random.shuffle(stopTags) #Shuffle randomly to increase chances of finding the bus quicker
        for stopTag in stopTags: 
            response = requests.get("https://retro.umoiq.com/service/publicJSONFeed?command=predictions&a=ttc&r=" + route + "&s=" + stopTag)
            #print("https://retro.umoiq.com/service/publicJSONFeed?command=predictions&a=ttc&r=" + route + "&s=" + stopTag)
            if response.status_code == RESPONSE_OK_CODE:
                predictionsData = response.json()
                if 'direction' in predictionsData['predictions'].keys():
                    if isinstance(predictionsData['predictions']['direction'], list):
                        for x in predictionsData['predictions']['direction']:
                            if isinstance(x["prediction"], list):
                                for y in x["prediction"]:
                                    if y["vehicle"] == bus:
                                        return y['block'], x['title'] #latter is the headsign
                            else:
                                if x["prediction"]["vehicle"] == bus:
                                        return x["prediction"]["block"], predictionsData['predictions']['direction']['title'] #latter is the headsign        
                    else:
                        if isinstance(predictionsData['predictions']['direction']['prediction'], list):
                            for x in predictionsData['predictions']['direction']['prediction']:
                                if x['vehicle'] == bus:
                                    return x['block'], predictionsData['predictions']['direction']['title'] #latter is the headsign
                        else:
                            if predictionsData['predictions']['direction']['prediction']['vehicle'] == bus:
                                return x['block'], predictionsData['predictions']['direction']['title'] #latter is the headsign
            else:
                raise Exception("Unsuccessful response")
    return "not found", "not found"

#given the run number, get the next four departures.
#TO DO after the MVP
def getNextDepartures(route, run, time):
    #First determine the day of week. Define hours of a day as according to DEF_START_DAY_TIME parameter
    dayOfWeek = (datetime.strptime(time, "%Y-%m-%d %H:%M") - datetime.timedelta(hours=DEF_START_DAY_TIME)).weekday() 
    if dayOfWeek < 5:
        serviceClass = "wkd"
    elif dayOfWeek == 5:
        serviceClass = "sat"
    else:
        serviceClass = "sun"
    #Holidays.py???
    
    #Convert time to hour epoch time for comparison with the attributes
    dt = datetime.strptime(time, "%Y-%m-%d %H:%M")
    timeHour, timeMin = dt.hour, dt.minute
    if timeHour < DEF_START_DAY_TIME:
        epochHour = datetime(1970, 1, 2, timeHour, timeMin, 0).timestamp() * 1000
    else:
        epochHour = datetime(1970, 1, 1, timeHour, timeMin, 0).timestamp() * 1000

    #Query the schedule API
    nextDepartures = []
    response = requests.get("https://retro.umoiq.com/service/publicJSONFeed?command=schedule&a=ttc&r=" + route)
    if response.status_code == RESPONSE_OK_CODE:
        scheduleData = response.json()
        #Search for the attributes with the run
        foundDepartures = 0
        for x in scheduleData['route']:
            if x['serviceClass'] == serviceClass:
                foundDepartures = 0
                for y in x['tr']:
                    if foundDepartures == NUM_NEXT_DEPARTURES / 2:
                        break 

                    if y['blockID'] == run:
                        startFound = False
                        for z in y['stop']:
                            if z['content'] != "--" and not startFound: #Find the first stop with a time
                                startStopTag = z['tag']
                                startFound = True 
                            if z['content'] != "--" and "ar" in z['tag']:
                                endStopTag = z['tag']
                                break
        
                        #Get the names of the stop given the stop tags
                        for w in x['header']['stop']: #Find the stop name
                            if w['tag'] == startStopTag:
                                startStopName = w['content']
                            if w['tag'] == endStopTag:
                                endStopName = w['content']
                                break

                        foundDepartures += 1            
                        nextDepartures.append()
                    
    else:
        raise Exception("Unsuccessful response")

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
    'nextDepartures': [{ #TO DO after MVP
                        'route': (int),
                        'startStop': (str),
                        'endStop': (str),
                        'startTime': (time) #time leaving the first stop
                      }] (list dict) 
}
"""
def iterateAPI(busLocations, updatedTime):
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
            
            if run == "not found" and headsign == "not found":
                continue

            #From the run, decide if we reject the special sighting (in cases of school specials)
            runRoute = run.split('_')[0]
            if runRoute != busRoute:
                runRouteGarages = list(db.routeAllocations.objects.filter(route=runRoute).values_list('garage',flat=True))
                if busGarage[0] in runRouteGarages:
                    continue #REJECT

            #nextDepartures = getNextDepartures(busRoute, run, updatedTime) #TO DO after MVP

            
            specials.append({'bus':busNum, 'busGarage':busGarage, 'route':busRoute, 'routeGarage':routeGarages, 'dirTag':dirTag, 'run':run, 'headsign':headsign})
    
    if len(specials) != 0:
        #Sort specials based on bus
        specials = sorted(specials, key=lambda x: x['bus'])
        #Clean up the busGarage and routeGarage lists to just a string. At the same time, add to the special sightings database
        for s in specials:
            s["busGarage"] = ', '.join(s["busGarage"])
            s["routeGarage"] = ', '.join(s["routeGarage"])

            bus_instance = db.busAllocations.objects.get(busNumber = s['bus'])
            instance = db.specialSightings(busNumber = bus_instance, busGarage = s['busGarage'], runNumber = s['run'], runGarage = s['routeGarage'], datetime = updatedTime)    
            instance.save()

    return specials


#main tracker code. Returns time that API was last updated at and dict of special sightings. 
def tracker():
    response = requests.get("https://webservices.umoiq.com/service/publicJSONFeed?command=vehicleLocations&a=ttc")
    
    if response.status_code == RESPONSE_OK_CODE:
        data = response.json()
        busLocations = data.get('vehicle')
        
        time = getUpdatedAtTime(int(data.get('lastTime')['time']))        
        specials = iterateAPI(busLocations, time)



    else:
        raise Exception("Unsuccessful response")
        
    return time, specials
    