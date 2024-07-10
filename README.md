# TTC-Special-Sightings-Tracker

Welcome to the TTC Special Sightings Tracker. This program uses the TTC's [NextBus API](https://webservices.umoiq.com/service/publicXMLFeed?command=vehicleLocations&a=ttc) to output all current special sightings, which are buses on routes which are run by other garages. An example output is: 

Updated at: 2022-05-17 15:27:19.935000

1350: 46   

1550: 24

3552: 104

1350 is a Mount Dennis bus on the 46, a Queensway route. 1550 is a Malvern bus on the 24, a Birchmount route. 3552 is an Arrow Rd bus on the 104, a Wilson route. Up-to-date information on bus and route allocations can be found on the CPTDB Wiki (link for each garage below): 

* [Arrow Rd (ARW)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Arrow_Rd._Division)
* [Birchmount (BIR)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Birchmount_Division)
* [Eglinton (EGL)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Eglinton_Division)
* [Malvern (MAL)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Malvern_Division)
* [McNicoll (MCN)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_McNicoll_Division)
* [Mount Dennis (MTD)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Mount_Dennis_Division)
* [Queensway (QSY)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Queensway_Division)
* [Wilson (WIL)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Wilson_Division)

### Limitations

Sometimes, school specials or certain departures on routes are operated by another garage other than the one that runs said route. For example, in the May 2022 board period, the 32 is a Mount Dennis route and has three school specials in the afternoon: two from Arrow Rd and one from Wilson. The buses on these school specials will show up on the Special Sightings Tracker's output, even though they happen on a daily basis and are thus not considered special. Currently, the tracker has no method of distinguishing these school specials from true special sightings. 

### To use on a mobile Android device for use on the go 

1. Install the [Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3) app from the Google Play Store, which allows you to run Python on your Android device. 
2. Open Pydroid 3 and install the following Python libraries from the Pip menu: datetime, numpy, pandas, requests, openpyxl, and et-xmlfile. 
3. Download the included TTC_RAD_tracker.py file along with the spreadsheets Bus Allocations.xslx and Route Allocations.xslx onto your mobile device, ensuring that they are in the same folder / directory. 
4. Open TTC_RAD_tracker.py in Pydroid 3 and press the yellow play button on the bottom right to run. 
