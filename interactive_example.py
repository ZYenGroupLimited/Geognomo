import geocoding
import re
# please Enter latitude, longitude, altitude and level you desire to generate QTM code
# or you can use the commented value in the side to test
# need to have validation for latitude, longitude, level and atitude
# latitude range from -90 to +90
# longitude range from -180 to 180
# level range from 1 to 40
# altitude -12262 to 8848 meters
# for testing purpose you can use following values:
# latitude: 51.499207299999995, longitude: -0.08800609999999999, altitude: 0, level: 5
print("Please enter")
latitude = raw_input("Latitude: ")
longitude = raw_input("Longitude: ")
altitude = raw_input("Altitude: ")
level = raw_input("Level: ")

latlon2qtm = geocoding.LatLonToIcosahedronID(latitude, longitude, altitude, level)
print "QTM Code: ", latlon2qtm['QTM_GeoGnomo_Code'], "\n", "QTM Details : \n",  latlon2qtm, "\n"

latlon2qrs = geocoding.LatLonToQrsID(latitude, longitude, altitude, level)
print "QRS Code: ", latlon2qrs['QRS_GeoGnomo_Code'], "\n", "QRS Details : \n",  latlon2qrs, "\n"

latlon2qutms = geocoding.LatLonToQUTMSID(latitude, longitude, altitude, level)
print "QUTMS Code: ", latlon2qutms['QUTMS_GeoGnomo_Code'], "\n", "QUTMS Details : \n",  latlon2qutms, "\n"

latlon2vrs = geocoding.LatLonToVRS(latitude, longitude, 51.505876019041246, -0.09002700448036194)
print "VRS Code base on (51.505876019041246, -0.09002700448036194) : ", latlon2vrs['VRS_GeoGnomo_Code'], "\n",\
    "VRS Details : \n",  latlon2vrs, "\n"

print "decoding geocode generated before"

icos2latlon = geocoding.IcosIDToLatLon(latlon2qtm['QTM_GeoGnomo_Code'], level)
print "Icosahedron boundaries: ", "Top Vertices: ", \
    (icos2latlon['Top_LatLonA'],icos2latlon['Top_LatLonB'],icos2latlon['Top_LatLonC']),\
    "\n", "Left Vertices: ", \
    (icos2latlon['Left_LatLonA'], icos2latlon['Left_LatLonB'], icos2latlon['Left_LatLonC']),\
    "\n", "Right Vertices: ", \
    (icos2latlon['Right_LatLonA'], icos2latlon['Right_LatLonB'], icos2latlon['Right_LatLonC']),\
    "\n", "Bottom Vertices: ", \
    (icos2latlon['Bottom_LatLonA'], icos2latlon['Bottom_LatLonB'], icos2latlon['Bottom_LatLonC']),\
    "\n"

qrs2latlon = geocoding.QRSIDToLatLon(latlon2qrs['QRS_GeoGnomo_Code'], level)
print "QRS boundaries: ", "Top Vertices: ", \
    (qrs2latlon['Top_LatLonA'],qrs2latlon['Top_LatLonB'],qrs2latlon['Top_LatLonC']),\
    "\n", "Left Vertices: ", \
    (qrs2latlon['Left_LatLonA'], qrs2latlon['Left_LatLonB'], qrs2latlon['Left_LatLonC']),\
    "\n", "Right Vertices: ", \
    (qrs2latlon['Right_LatLonA'], qrs2latlon['Right_LatLonB'], qrs2latlon['Right_LatLonC']),\
    "\n", "Bottom Vertices: ", \
    (qrs2latlon['Bottom_LatLonA'], qrs2latlon['Bottom_LatLonB'], qrs2latlon['Bottom_LatLonC']),\
    "\n"

qutms2latlon = geocoding.QUTMSIDToLatLon(latlon2qutms['QUTMS_GeoGnomo_Code'], level)
print "QUTMS boundaries: ", "Top Vertices: ", \
    (qutms2latlon['Top_LatLonA'],qutms2latlon['Top_LatLonB'],qutms2latlon['Top_LatLonC']),\
    "\n", "Left Vertices: ", \
    (qutms2latlon['Left_LatLonA'], qutms2latlon['Left_LatLonB'], qutms2latlon['Left_LatLonC']),\
    "\n", "Right Vertices: ", \
    (qutms2latlon['Right_LatLonA'], qutms2latlon['Right_LatLonB'], qutms2latlon['Right_LatLonC']),\
    "\n", "Bottom Vertices: ", \
    (qutms2latlon['Bottom_LatLonA'], qutms2latlon['Bottom_LatLonB'], qutms2latlon['Bottom_LatLonC']),\
    "\n"
vrs2latlon = geocoding.VRSToLatLon(latlon2vrs['VRS_GeoGnomo_Code'])
print "VRS Details: \n", vrs2latlon