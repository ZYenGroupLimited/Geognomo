import geocoding

latlon2icos = geocoding.LatLonToIcosahedronID(51.499207299999995, -0.08800609999999999, 0, 5)
print 'latlon2QTM\n', latlon2icos

icos2latlon = geocoding.IcosIDToLatLon('F49', 5)
print 'icos2latlon:\n' , icos2latlon

latlon2qrs = geocoding.LatLonToQrsID(51.499207299999995, -0.08800609999999999, 0, 5)
print 'latlon2qrs:\n', latlon2qrs

qrs2latlon = geocoding.QRSIDToLatLon('G5V', 5)
print 'qrs2latlon:\n', qrs2latlon

latlon2qtms = geocoding.LatLonToQUTMSID(51.499207299999995, -0.08800609999999999, 0, 5)
print 'latlon2qtms:\n', latlon2qtms

qtms2latlon = geocoding.QUTMSIDToLatLon('30U-47', 5)
print 'qtms2latlon:\n', qtms2latlon

latlon2vrs = geocoding.LatLonToVRS(51.49518997210978, -0.11363044381141663, 51.505876019041246, -0.09002700448036194)
print 'latlon2vrs:\n', latlon2vrs

vrs2latlon = geocoding.VRSToLatLon('RUYQ8VN57H')
print 'vrs2latlon:\n', vrs2latlon

