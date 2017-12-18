# About Geognomo

**GeoGnomo** is an open-source project exploring various forms of geocoding for use in Smart Ledgers (aka blockchains with embedded computer code). The GeoGnomo project focuses on memorable systems that provide easy ways to aggregate areas together, as well as giving users some clues to location and distance and scale. GeoGnomo consists of three systems for geostamping: Quaternary Triangular System, a Quaternary Rectangular System, and a Variable Rectangular System. Each can be used to record geographic areas into a blockchain. We have provided the source code and an online translation from latitude & longitude areas to geocodes and back. Thus, blockchain applications have almost an instant ‘global post code’ or ‘global zip code’ system. By using consistent geocoding data retrieval is easier. Users can share information easily – “tell the drone to come to F49PUR9B7-20”, a resolution of 7.6 metres.

We believe the principal qualities of a good geocode are:

**Memorability** - It should be compact and memorable

**Aggregation** - A coding system should be able to describe comparably a variety of area sizes and structures, both natural and human, such as forests, beaches, buildings, sports grounds, country borders, etc.

**Proximity** - Similar codes should represent similar locations, so that people exchanging codes can roughly understand the distance and relationship between them.

**Scale** -  Users should have control over the precision.


GeoGnomo encompasses four different approaches designed to provide effective methods for geocoding:

 **Variable Rectangular System (VRS):**
 
 In the Variable Rectangular System codes are generated from a rectangular area, that may be specified through a ‘click and drag’ selection and represent the selected area
 
 To explore VRS in action [click here!](https://geognomo.com/geognomo/VRS/)
 
 **Quaternary Rectangular System (QRS):**
 
Quaternary Rectangular System defines the level 0 grid by dividing latitude into 3 bands and longitude into 6 bands, resulting in eighteen 60 by 60 degree squares that can be subdivided with no exceptions.

To explore QRS in action [click here!](https://geognomo.com/geognomo/QRS/)

 **Quaternary Triangular System (QTS)**
 
The Quaternary Triangle System divides the globe into a fixed grid of triangles and assigns a unique geocode to each triangle. Codes are generated from a latitude/longitude coordinate pair and a specified level n, which determines the scale of the grid. The code generated describes an area that contains the specified point.

To explore QTS in action [click here!](https://geognomo.com/geognomo/QTS/)

 **Quaternary UTM System (QUTMS) (Experimental)**
 
Quaternary UTM System uses the same quaternary trail method as QTS but defines its level 0 grid according to the Universal Transverse Mercator (UTM) projection, combined with the Military Grid Reference System (MGRS). It also generates codes from a single point and a specified scale level, with the code representing the area that the point lies in.

To explore QUTMS in action [click here!](https://geognomo.com/geognomo/QUTMS/)
 
## About Geognomo Geocoding project

**Z/Yen** presents four geocoding system as open source to further advancement of algorithm and it's proper 
and optimized implementation. **Geognomo** itself is a **Django** web application and is integrated with **google map api** to
display and work with maps in front-end. The open source code acts as basic back-end code which generated all the 
details required to display it in any front-end of your choice.

Open sourced **Geocoding** system  is a python project which lies under geocoding source folder. It structure is as follows:
- base32.json: It is the json file which acts as the base32 converter to alphabets. Alphabets are use for simplicity and memoriability in Geognomo coding systems.
- base32_data.py: It loads base32.json file from source directory and return json data for future manipulation.
- example.py: If you want to quick start about geo-coding system then this is the starting open. It call geo-coding functions and prints result to 
give you feel of how it works and can be implemented.
- geocode_decoder: This is the decoder file of QTM, QUTMS geo-coding system.
- geocode_encoder.py: This file acts as encoder for three different geo-coding system. QTM, QRS and QUTMS.
- geocoding.py: This is the bridge for all geo-coding systems and front-end. It communicates with encoder and decoder of different geo coding systems and return the 
result in json format.
- integer2base.py: This function convert integer into the binary system.
- interactive_example.py: This file contains interactive example: asking user input and print different geo-coding based on input.
- qrs_decoder: This is the decoder file of QRS geo-coding system.
- triangle.py: This file is module used inside QTM code to manipulate triangle.
- vrs_decoder: Decoder for VRS
- vrs_encoder: Encoder for VRS

## Running Geocoding in local machine

This project is python project so python need to be installed into the local machine. We also need git and numpy package.
If you have pip installed you can install numpy as follows: 

```commandline
# install numpy using pip:
 pip install numpy
```
If you don't have pip installed look documentation [here](https://pip.pypa.io/en/stable/installing/).

After you install numpy just clone the project into local machine.
```commandline
git clone https://github.com/ZYenGroupLimited/Geognomo.git
 
cd Geognomo/
```

Running example files:
```python
# you can run example.py to see how it works.

python example.py

# if you want to run interactive example:
python interactive_example.py
```


## Function Definition and Returned value structure

Find the meaning of the words used as key in returned json data:
- '__GeoGnomo_Code' : the shareable code which is generated using QTM/QRS/QUTMS/VRS geo-coding system.
- 'LatLon_' is the latitude, longitude of vertex(A/B/C/D) of triangle/ rectangle which enclosed the given latitude, longitude.
- 'Top_LatLon_' is the latitude, longitude of vertex(A/B/C/D) of triangle/ rectangle which lies at top of main triangle/rectangle.
- 'Left_LatLon_' is the latitude, longitude of vertex(A/B/C/D) of triangle/ rectangle which lies on left of main triangle/rectangle.
- 'Right_LatLon_' is the latitude, longitude of vertex(A/B/C/D) of triangle/ rectangle which lies on right of main triangle/rectangle.
- 'Bottom_LatLon_' is the latitude, longitude of vertex(A/B/C/D) of triangle/ rectangle which lies on bottom of main triangle/rectangle.
- 'area' is the total area of the enclosed by main triangle/rectangle.
- '_Base32_Code' is the base 32 alphabetic code for given latitude, longitude in that level produced by QTM/QRS/QUTMS/VRS encoding.
- '_Neighbor' gives the QTM_Base32_Code for neighbors of main triangle/rectangle.

### For QTM Code system: 
You can run QTM code system as shown:
```python
import geocoding
#geocoding.LatLonToIcosahedronID(latitude, longitude, altitude, level)
latlon2icos = geocoding.LatLonToIcosahedronID(51.499207299999995, -0.08800609999999999, 0, 5)
print latlon2icos
#Returned Json value. Example 1:
{
	"QTM_Quarternary_Code": "5,31133",
	"Bottom_LatLonA": "(50.353157,-3.6)",
	"Bottom_LatLonB": "(50.353157,0.0)",
	"Bottom_LatLonC": "(48.370815,-3.428571)",
	"Top_LatLonA": "N/A",
	"Top_LatLonC": "N/A",
	"Top_LatLonB": "N/A",
	"QTM_GeoGnomo_Code": "F49",
	"Left_LatLonB": "(52.335499,0.0)",
	"Left_LatLonC": "(50.353157,-3.6)",
	"Right_Neighbor": "Bravo,Sierra,4",
	"area": 28200.71915628558,
	"LatLonA": "(50.353157,-3.6)",
	"LatLonC": "(50.353157,0.0)",
	"LatLonB": "(52.335499,0.0)",
	"QTM_Base32_Code": "Foxtrot,4,9",
	"Left_Neighbor": "Foxtrot,4,6",
	"Left_LatLonA": "(52.335499,-3.789474)",
	"IJ": "(13,39)",
	"LatLonCentral": "(51.013938,-1.220339)",
	"Right_LatLonA": "(50.353157,-0.0)",
	"Right_LatLonB": "(52.335499,0.0)",
	"Right_LatLonC": "(50.353157,3.6)",
	"Top_Neighbor": "N/A",
	"Bottom_Neighbor": "Foxtrot,4,Papa"
}
```

You can run QTM decoding as shown:
```python
import geocoding
#geocoding.IcosIDToLatLon(QTM_GeoGnomo_Code, level)
icos2latlon = geocoding.IcosIDToLatLon('F49', 5)
print icos2latlon
#Returned Json value. Example 2:
{
	"QTM_Quarternary_Code": "5,31133",
	"Bottom_LatLonA": "(50.353157,-3.6)",
	"Bottom_LatLonB": "(50.353157,0.0)",
	"Bottom_LatLonC": "(48.370815,-3.428571)",
	"Top_LatLonA": "N/A",
	"Top_LatLonC": "N/A",
	"Top_LatLonB": "N/A",
	"Left_LatLonA": "(52.335499,-3.789474)",
	"Left_LatLonB": "(52.335499,0.0)",
	"Left_LatLonC": "(50.353157,-3.6)",
	"Right_Neighbor": "Bravo,Sierra,4",
	"area": 28200.71915628558,
	"altitude": "N/A",
	"LatLonA": "(50.353157,-3.6)",
	"LatLonC": "(50.353157,0.0)",
	"LatLonB": "(52.335499,0.0)",
	"Left_Neighbor": "Foxtrot,4,6",
	"IJ": "(13,39)",
	"LatLonCentral": "(51.013938,-1.220339)",
	"Right_LatLonA": "(50.353157,-0.0)",
	"Right_LatLonB": "(52.335499,0.0)",
	"Right_LatLonC": "(50.353157,3.6)",
	"Top_Neighbor": "N/A",
	"Bottom_Neighbor": "Foxtrot,4,Papa"
}
```
### For QRS Code system: 
You can run QRS code system as shown:

```python
import geocoding
#geocoding.LatLonToQrsID(latitude, longitude, altitude, level)
latlon2qrs = geocoding.LatLonToQrsID(51.499207299999995, -0.08800609999999999, 0, 5)
print latlon2qrs
# Returned Json value.Example 3
{
	"Bottom_LatLonA": "(48.75,-1.875)",
	"Bottom_LatLonB": "(50.625,-1.875)",
	"Bottom_LatLonC": "(50.625,0.0)",
	"Bottom_LatLonD": "(48.75,0.0)",
	"Top_LatLonD": "(52.5,0.0)",
	"Top_LatLonA": "(52.5,-1.875)",
	"Top_LatLonC": "(54.375,0.0)",
	"Top_LatLonB": "(54.375,-1.875)",
	"Left_LatLonA": "(50.625,-3.75)",
	"Left_LatLonB": "(52.5,-3.75)",
	"Left_LatLonC": "(52.5,-1.875)",
	"Left_LatLonD": "(50.625,-1.875)",
	"Right_Neighbor": "Bravo,Romeo,Alpha",
	"area": 27081.57217945275,
	"QTM32Code": "Golf,5,Victor",
	"LatLonD": "(50.625,0.0)",
	"LatLonA": "(50.625,-1.875)",
	"LatLonC": "(52.5,0.0)",
	"LatLonB": "(52.5,-1.875)",
	"QRS_GeoGnomo_Code": "G5V",
	"Left_Neighbor": "Golf,5,Uniform",
	"LatLonCenter": "(51.5625,-0.9375)",
	"Right_LatLonD": "(50.625,1.875)",
	"Right_LatLonA": "(50.625,0)",
	"Right_LatLonB": "(52.5,0)",
	"Right_LatLonC": "(52.5,1.875)",
	"QTMCode": "6,31311",
	"Top_Neighbor": "Golf,4,9",
	"Bottom_Neighbor": "Golf,5,X-ray"
}
```
You can run QRS decoding as shown:
```python
import geocoding
#geocoding.QRSIDToLatLon(QRS_GeoGnomo_Code, level)
qrs2latlon = geocoding.QRSIDToLatLon('G5V', 5)
print qrs2latlon
#Returned Json value.Example 4
{
	"Bottom_LatLonA": "(48.75,-1.875)",
	"Bottom_LatLonB": "(50.625,-1.875)",
	"Bottom_LatLonC": "(50.625,0.0)",
	"Bottom_LatLonD": "(48.75,0.0)",
	"Top_LatLonD": "(52.5,0.0)",
	"Top_LatLonA": "(52.5,-1.875)",
	"Top_LatLonC": "(54.375,0.0)",
	"Top_LatLonB": "(54.375,-1.875)",
	"Left_LatLonA": "(50.625,-3.75)",
	"Left_LatLonB": "(52.5,-3.75)",
	"Left_LatLonC": "(52.5,-1.875)",
	"Left_LatLonD": "(50.625,-1.875)",
	"Right_Neighbor": "Bravo,Romeo,Alpha",
	"area": 27081.57217945275,
	"altitude": "N/A",
	"LatLonD": "(50.625,0.0)",
	"LatLonA": "(50.625,-1.875)",
	"LatLonC": "(52.5,0.0)",
	"LatLonB": "(52.5,-1.875)",
	"Left_Neighbor": "Golf,5,Uniform",
	"Right_LatLonD": "(50.625,1.875)",
	"LatLonCentral": "(51.5625,-0.9375)",
	"Right_LatLonA": "(50.625,0)",
	"Right_LatLonB": "(52.5,0)",
	"Right_LatLonC": "(52.5,1.875)",
	"Top_Neighbor": "Golf,4,9",
	"Bottom_Neighbor": "Golf,5,X-ray"
}
```
### For QUTMS Code system: 
You can run QUTMS code system as shown:

```python
import geocoding
#geocoding.LatLonToQUTMSID(latitude, longitude, altitude, level)
latlon2qutms = geocoding.LatLonToQUTMSID(51.499207299999995, -0.08800609999999999, 0, 5)
print latlon2qutms
#Returned Json value.Example 5
{
	"Bottom_LatLonA": "(51.0,-0.1875)",
	"Bottom_LatLonB": "(51.25,-0.1875)",
	"Bottom_LatLonC": "(51.25,0.0)",
	"Bottom_LatLonD": "(51.0,0.0)",
	"Top_LatLonD": "(51.5,0.0)",
	"Top_LatLonA": "(51.5,-0.1875)",
	"Top_LatLonC": "(51.75,0.0)",
	"Top_LatLonB": "(51.75,-0.1875)",
	"Left_LatLonA": "(51.25,0)",
	"Left_LatLonB": "(51.5,0)",
	"Left_LatLonC": "(51.5,0.1875)",
	"Left_LatLonD": "(51.25,0.1875)",
	"Right_Neighbor": "30U-4,6",
	"area": 362.59046108503685,
	"QTM32Code": "30U-4,7",
	"LatLonD": "(51.25,0.0)",
	"LatLonA": "(51.25,-0.1875)",
	"LatLonC": "(51.5,0.0)",
	"LatLonB": "(51.5,-0.1875)",
	"Left_Neighbor": "31U-Quebec,India",
	"Bottom_Neighbor": "30U-4,9",
	"LatLonCenter": "(51.375,-0.09375)",
	"Right_LatLonD": "(51.25,-0.1875)",
	"Right_LatLonA": "(51.25,-0.375)",
	"Right_LatLonB": "(51.5,-0.375)",
	"Right_LatLonC": "(51.5,-0.1875)",
	"QTMCode": "30U,31131",
	"Top_Neighbor": "30U-4,X-ray",
	"QUTMS_GeoGnomo_Code": "30U-47"
}
```
You can run QUTMS decoding as shown:
```python
import geocoding
#geocoding.QUTMSIDToLatLon(QUTMS_GeoGnomo_Code, level)
qutms2latlon = geocoding.QUTMSIDToLatLon('30U-47', 5)
print qutms2latlon
#Returned Json value.Example 6
{
	"Bottom_LatLonA": "(51.0,-0.1875)",
	"Bottom_LatLonB": "(51.25,-0.1875)",
	"Bottom_LatLonC": "(51.25,0.0)",
	"Bottom_LatLonD": "(51.0,0.0)",
	"Top_LatLonD": "(51.5,0.0)",
	"Top_LatLonA": "(51.5,-0.1875)",
	"Top_LatLonC": "(51.75,0.0)",
	"Top_LatLonB": "(51.75,-0.1875)",
	"Left_LatLonA": "(51.25,0)",
	"Left_LatLonB": "(51.5,0)",
	"Left_LatLonC": "(51.5,0.1875)",
	"Left_LatLonD": "(51.25,0.1875)",
	"Right_Neighbor": "30U-4,6",
	"area": 362.59046108503685,
	"altitude": "N/A",
	"LatLonD": "(51.25,0.0)",
	"LatLonA": "(51.25,-0.1875)",
	"LatLonC": "(51.5,0.0)",
	"LatLonB": "(51.5,-0.1875)",
	"Left_Neighbor": "31U-Quebec,India",
	"LatLonCenter": "(51.375,-0.09375)",
	"Right_LatLonD": "(51.25,-0.1875)",
	"Right_LatLonA": "(51.25,-0.375)",
	"Right_LatLonB": "(51.5,-0.375)",
	"Right_LatLonC": "(51.5,-0.1875)",
	"Top_Neighbor": "30U-4,X-ray",
	"Bottom_Neighbor": "30U-4,9"
}
```

### For VRS Code system: 
VRS coding system takes two point as an input so we need two (latitude, longitude) combination.
You can run VRS code system as shown:

```python
import geocoding
#geocoding.LatLonToVRS(latitude1, longitude1, latitude2, longitude2)
latlon2vrs = geocoding.LatLonToVRS(51.49518997210978, -0.11363044381141663, 51.505876019041246, -0.09002700448036194)
print latlon2vrs
#Returned Json value.Example 7
{
	"LAT1": 51.49518997210978,
	"area": 1.7742498857804638,
	"LAT2": 51.505876019041246,
	"VRS_GeoGnomo_Code": "RUYQ8VN57H",
	"LatLonA": "(51.495,-0.114)",
	"LatLonB": "(51.505,-0.091)",
	"LON1": -0.11363044381141663,
	"LON2": -0.09002700448036194
}
```

You can run VRS decoding as shown:
```python
import geocoding
#geocoding.VRSToLatLon(VRS_GeoGnomo_Code)
vrs2latlon = geocoding.VRSToLatLon('RUYQ8VN57H')
print vrs2latlon
#Returned Json value.Example 8
{
 "LatLonB": "(51.505, -0.091)",
 "LatLonA": "(51.495, -0.114)", 
 "area": 1.7742498857804638
 }

```

## Using Geognomo Api for geocoding:

As being open source project we provide api service for public, which can be integrated into any application and services. 
Z/Yen will keep web api updated as new improvements are introduced in github. 
Api is URL base api. So you will query the web url and get result in json format which you can further manipulate as your need.

Url for Api uses are as follows: "http://geognomo.com/"
- geognomo/api/latlon2qtm/latitude/longitude/altitude/level:
  - http://geognomo.com/geognomo/api/latlon2qtm/51.49518997210978/-0.11363044381141663/0/5/
- geognomo/api/qtm2latlon/QTM_GeoGnomo_Code/level:
  - http://geognomo.com/geognomo/api/qtm2latlon/f49/5
- geognomo/api/latlon2qrs/latitude/longitude/altitude/level
  - http://geognomo.com/geognomo/api/latlon2qrs/51.49518997210978/-0.11363044381141663/0/5/
- geognomo/api/qrs2latlon/QRS_GeoGnomo_Code/level
  - http://geognomo.com/geognomo/api/qrs2latlon/G5V/5/
- geognomo/api/latlon2qutms/latitude/longitude/altitude/level
  - http://geognomo.com/geognomo/api/latlon2qutms/51.49518997210978/-0.11363044381141663/0/5/
- geognomo/api/qutms2latlon/QUTMS_GeoGnomo_Code/level
  - http://geognomo.com/geognomo/api/qutms2latlon/30U-47/5/
- geognomo/api/latlon2vrs/latitude1/longitude1/latitude2/longitude2
  - http://geognomo.com/geognomo/api/latlon2vrs/51.49518997210978/-0.11363044381141663/51.505876019041246/-0.09002700448036194/
- geognomo/api/vrs2latlon/VRS_GeoGnomo_Code/level
  - http://geognomo.com/geognomo/api/vrs2latlon/RUYQ8VN57H/

Simple python application to use API is as follows:

```python
import urllib2

# for QTM Encoding:
##http://geognomo.com/geognomo/api/latlon2qtm/latitude/longitude/altitude/level
pageUrl_qtm2latlon = "http://geognomo.com/geognomo/api/latlon2qtm/51.49518997210978/-0.11363044381141663/0/5/"
response_qtm2latlon = urllib2.urlopen(pageUrl_qtm2latlon).read()
print response_qtm2latlon
## It will result exact output as shown in Example 1
## for decoding from qtm code to latitude longitude
##http://geognomo.com/geognomo/api/qtm2latlon/QTM_GeoGnomo_Code/level
pageUrl_latlon2qtm = "http://geognomo.com/geognomo/api/qtm2latlon/f49/5"
response_latlon2qtm  = urllib2.urlopen(pageUrl_latlon2qtm).read()
print response_latlon2qtm
## It will result exact output as shown in Example 2

# for QRS Encoding:
##http://geognomo.com/geognomo/api/latlon2qrs/latitude/longitude/altitude/level
pageUrl_latlon2qrs = "http://geognomo.com/geognomo/api/latlon2qrs/51.49518997210978/-0.11363044381141663/0/5/"
response_latlon2qrs  = urllib2.urlopen(pageUrl_latlon2qrs).read()
print response_latlon2qrs
## It will result exact output as shown in Example 3
## for decoding from QRS code to latitude longitude
##http://geognomo.com/geognomo/api/qrs2latlon/QRS_GeoGnomo_Code/level
pageUrl_qrs2latlon = "http://geognomo.com/geognomo/api/qrs2latlon/G5V/5/"
response_qrs2latlon  = urllib2.urlopen(pageUrl_qrs2latlon).read()
print response_qrs2latlon
## It will result exact output as shown in Example 4

# for QUTMS Encoding:
##http://geognomo.com/geognomo/api/latlon2qutms/latitude/longitude/altitude/level
pageUrl_latlon2qutms = "http://geognomo.com/geognomo/api/latlon2qutms/51.49518997210978/-0.11363044381141663/0/5/"
response_latlon2qutms  = urllib2.urlopen(pageUrl_latlon2qutms).read()
print response_latlon2qutms
## It will result exact output as shown in Example 5
## for decoding from QUTMS code to latitude longitude
##http://geognomo.com/geognomo/api/qutms2latlon/QUTMS_GeoGnomo_Code/level
pageUrl_qutms2latlon = "http://geognomo.com/geognomo/api/qutms2latlon/30U-47/5/"
response_qutms2latlon  = urllib2.urlopen(pageUrl_qutms2latlon).read()
print response_qutms2latlon
## It will result exact output as shown in Example 6

# for VRS Encoding:
##http://geognomo.com/geognomo/api/latlon2vrs/latitude1/longitude1/latitude2/longitude2
pageUrl_latlon2vrs = "http://geognomo.com/geognomo/api/latlon2vrs/51.49518997210978/-0.11363044381141663/\
51.505876019041246/-0.09002700448036194/"
response_latlon2vrs  = urllib2.urlopen(pageUrl_latlon2vrs).read()
print pageUrl_latlon2vrs
## It will result exact output as shown in Example 7
## for decoding from QRS code to latitude longitude
##http://geognomo.com/geognomo/api/vrs2latlon/VRS_GeoGnomo_Code/level
pageUrl_vrs2latlon = "http://geognomo.com/geognomo/api/vrs2latlon/RUYQ8VN57H/"
response_vrs2latlon  = urllib2.urlopen(pageUrl_vrs2latlon).read()
print response_vrs2latlon
## It will result exact output as shown in Example 8
```

