import math
import geocode_encoder as encoder
import geocode_decoder as decoder
import qrs_decoder
import vrs_encoder
import vrs_decoder
import triangle


def LatLonToIcosahedronID(latitude, longitude, altitude, level):
    context = {}
    level = int(level)
    icosahedronObject = encoder.IcoEncoder(latitude, longitude, level)
    icosahedronIndex = int(icosahedronObject.icosahedron())
    altitudeBase32ID = encoder.getAlt32ID(level, altitude)
    rowIndex = encoder.getAdjustedRowCol(latitude, longitude, level)[0]
    columnIndex = encoder.getAdjustedRowCol(latitude, longitude, level)[1]

    QTMCode = encoder.getQTMIDs(level, rowIndex, columnIndex, icosahedronIndex)
    QTM32Code = encoder.getQTM32ID(str(QTMCode))
    QTM32Code_word = QTM32Code[0]
    QTM32Code_alpha = QTM32Code[1]

    leftIcosahedron = encoder.LEFT_NEIGHBOR(level, rowIndex, columnIndex, icosahedronIndex)
    rightIcosahedron = encoder.RIGHT_NEIGHBOR(level, rowIndex, columnIndex, icosahedronIndex)

    context['IJ'] = str((rowIndex, columnIndex))
    context['QTM_Quarternary_Code'] = QTMCode
    context['QTM_Base32_Code'] = QTM32Code_word
    context['QTM_GeoGnomo_Code'] = QTM32Code_alpha
    if altitudeBase32ID <> '':
        context['QTM_Base32_Quantization_Code'] = QTM32Code_alpha + '@' + altitudeBase32ID

    Left_Neighbor_Code = encoder.getQTMIDs(level, leftIcosahedron[1], leftIcosahedron[2], leftIcosahedron[0])
    Right_Neighbor_Code = encoder.getQTMIDs(level, rightIcosahedron[1], rightIcosahedron[2], rightIcosahedron[0])

    left_abc = encoder.getABC(leftIcosahedron[1], leftIcosahedron[2])
    right_abc = encoder.getABC(rightIcosahedron[1], rightIcosahedron[2])

    context['Left_LatLonA'] = decoder.covertToLatLon(Left_Neighbor_Code, left_abc[0][0], left_abc[0][1])
    context['Left_LatLonB'] = decoder.covertToLatLon(Left_Neighbor_Code, left_abc[1][0], left_abc[1][1])
    context['Left_LatLonC'] = decoder.covertToLatLon(Left_Neighbor_Code, left_abc[2][0], left_abc[2][1])
    context['Right_LatLonA'] = decoder.covertToLatLon(Right_Neighbor_Code, right_abc[0][0], right_abc[0][1])
    context['Right_LatLonB'] = decoder.covertToLatLon(Right_Neighbor_Code, right_abc[1][0], right_abc[1][1])
    context['Right_LatLonC'] = decoder.covertToLatLon(Right_Neighbor_Code, right_abc[2][0], right_abc[2][1])

    t = encoder.TOP_NEIGHBOR(level, rowIndex, columnIndex, icosahedronIndex)
    Top_Neighbor_Code = encoder.getQTMIDs(level, t[1], t[2], t[0])
    context['Top_Neighbor'] = encoder.getQTM32ID(str(Top_Neighbor_Code))[0]
    top_abc = encoder.getABC(t[1], t[2])

    context['Top_LatLonA'] = 'N/A'
    context['Top_LatLonB'] = 'N/A'
    context['Top_LatLonC'] = 'N/A'
    context['Bottom_LatLonA'] = 'N/A'
    context['Bottom_LatLonB'] = 'N/A'
    context['Bottom_LatLonC'] = 'N/A'
    if (math.ceil(float(icosahedronIndex) / 5) % 2 != 0 and columnIndex % 2 == 0) or \
            (math.ceil(float(icosahedronIndex) / 5) % 2 == 0 and columnIndex % 2 != 0):
        context['Bottom_Neighbor'] = 'N/A'
        context['Top_LatLonA'] = decoder.covertToLatLon(Top_Neighbor_Code, top_abc[0][0], top_abc[0][1])
        context['Top_LatLonB'] = decoder.covertToLatLon(Top_Neighbor_Code, top_abc[1][0], top_abc[1][1])
        context['Top_LatLonC'] = decoder.covertToLatLon(Top_Neighbor_Code, top_abc[2][0], top_abc[2][1])
    else:
        context['Bottom_Neighbor'] = context['Top_Neighbor']
        context['Bottom_LatLonA'] = decoder.covertToLatLon(Top_Neighbor_Code, top_abc[0][0], top_abc[0][1])
        context['Bottom_LatLonB'] = decoder.covertToLatLon(Top_Neighbor_Code, top_abc[1][0], top_abc[1][1])
        context['Bottom_LatLonC'] = decoder.covertToLatLon(Top_Neighbor_Code, top_abc[2][0], top_abc[2][1])
        context['Top_Neighbor'] = 'N/A'


    context['Left_Neighbor'] = encoder.getQTM32ID(str(Left_Neighbor_Code))[0]
    context['Right_Neighbor'] = encoder.getQTM32ID(str(Right_Neighbor_Code))[0]
    abc = encoder.getABC(rowIndex, columnIndex)
    context['LatLonA'] = decoder.covertToLatLon(QTMCode, abc[0][0], abc[0][1])
    context['LatLonB'] = decoder.covertToLatLon(QTMCode, abc[1][0], abc[1][1])
    context['LatLonC'] = decoder.covertToLatLon(QTMCode, abc[2][0], abc[2][1])
    context['LatLonCentral'] = decoder.getCentreLatLon(QTM32Code_word, level)
    context['area'] = triangle.getArea(str(QTMCode), rowIndex, columnIndex)
    return context


def IcosIDToLatLon(qtm32code, level):
    context = {}
    QTM32Code = str(qtm32code).split("@")[0]
    if "@" in str(qtm32code):
        altitude = str(qtm32code).split("@")[1]
    else:
        altitude = "N/A"
    context['altitude'] = altitude
    level = int(level)

    latlonCentral = decoder.getCentreLatLon(QTM32Code, level)
    context['LatLonCentral'] = latlonCentral
    icosahedronDecoderObject = decoder.IcoDecoder(QTM32Code, level)
    QTMCode = icosahedronDecoderObject.covertToQTMIDs()
    context['QTM_Quarternary_Code'] = QTMCode
    icosahedronIndex = int(icosahedronDecoderObject.icos())

    i = int(decoder.getRowCol(QTMCode, level)[0])
    j = int(decoder.getRowCol(QTMCode, level)[1])
    context['IJ'] = str((i, j))

    left_neighbor = encoder.LEFT_NEIGHBOR(level, i, j, icosahedronIndex)
    right_neighbor = encoder.RIGHT_NEIGHBOR(level, i, j, icosahedronIndex)

    Left_Neighbor_Code = encoder.getQTMIDs(level, left_neighbor[1], left_neighbor[2], left_neighbor[0])
    Right_Neighbor_Code = encoder.getQTMIDs(level, right_neighbor[1], right_neighbor[2], right_neighbor[0])
    left_abc = encoder.getABC(left_neighbor[1], left_neighbor[2])
    right_abc = encoder.getABC(right_neighbor[1], right_neighbor[2])

    context['Left_LatLonA'] = decoder.covertToLatLon(Left_Neighbor_Code, left_abc[0][0], left_abc[0][1])
    context['Left_LatLonB'] = decoder.covertToLatLon(Left_Neighbor_Code, left_abc[1][0], left_abc[1][1])
    context['Left_LatLonC'] = decoder.covertToLatLon(Left_Neighbor_Code, left_abc[2][0], left_abc[2][1])
    context['Right_LatLonA'] = decoder.covertToLatLon(Right_Neighbor_Code, right_abc[0][0], right_abc[0][1])
    context['Right_LatLonB'] = decoder.covertToLatLon(Right_Neighbor_Code, right_abc[1][0], right_abc[1][1])
    context['Right_LatLonC'] = decoder.covertToLatLon(Right_Neighbor_Code, right_abc[2][0], right_abc[2][1])

    t = encoder.TOP_NEIGHBOR(level, i, j, icosahedronIndex)
    Top_Neighbor_Code = encoder.getQTMIDs(level, t[1], t[2], t[0])
    context['Top_Neighbor'] = encoder.getQTM32ID(str(Top_Neighbor_Code))[0]
    top_abc = encoder.getABC(t[1], t[2])

    context['Top_LatLonA'] = 'N/A'
    context['Top_LatLonB'] = 'N/A'
    context['Top_LatLonC'] = 'N/A'
    context['Bottom_LatLonA'] = 'N/A'
    context['Bottom_LatLonB'] = 'N/A'
    context['Bottom_LatLonC'] = 'N/A'
    context['Bottom_Neighbor'] = 'N/A'

    if (math.ceil(float(icosahedronIndex) / 5) % 2 != 0 and j % 2 == 0) or \
            (math.ceil(float(icosahedronIndex) / 5) % 2 == 0 and j % 2 != 0):
        context['Top_LatLonA'] = decoder.covertToLatLon(Top_Neighbor_Code, top_abc[0][0], top_abc[0][1])
        context['Top_LatLonB'] = decoder.covertToLatLon(Top_Neighbor_Code, top_abc[1][0], top_abc[1][1])
        context['Top_LatLonC'] = decoder.covertToLatLon(Top_Neighbor_Code, top_abc[2][0], top_abc[2][1])
    else:
        context['Bottom_Neighbor'] = context['Top_Neighbor']
        context['Bottom_LatLonA'] = decoder.covertToLatLon(Top_Neighbor_Code, top_abc[0][0], top_abc[0][1])
        context['Bottom_LatLonB'] = decoder.covertToLatLon(Top_Neighbor_Code, top_abc[1][0], top_abc[1][1])
        context['Bottom_LatLonC'] = decoder.covertToLatLon(Top_Neighbor_Code, top_abc[2][0], top_abc[2][1])
        context['Top_Neighbor'] = 'N/A'

    abc = encoder.getABC(i, j)
    context['Left_Neighbor'] = encoder.getQTM32ID(str(Left_Neighbor_Code))[0]
    context['Right_Neighbor'] = encoder.getQTM32ID(str(Right_Neighbor_Code))[0]
    context['LatLonA'] = decoder.covertToLatLon(QTMCode, abc[0][0], abc[0][1])
    context['LatLonB'] = decoder.covertToLatLon(QTMCode, abc[1][0], abc[1][1])
    context['LatLonC'] = decoder.covertToLatLon(QTMCode, abc[2][0], abc[2][1])
    context['area'] = triangle.getArea(str(QTMCode), i, j)
    return context


def LatLonToQrsID(latitude, longitude, altitude, level):
    context = {}
    level = int(level)
    qrsGrid = encoder.QrsGrid(latitude, longitude, level)
    rec = int(qrsGrid.rectangle())
    alt32ID = encoder.getQrsAlt32ID(level, altitude)

    QTMCode = qrsGrid.QTMID()
    QTM32Code = encoder.getQTM32ID(str(QTMCode))
    QTM32Code_word = QTM32Code[0]
    QTM32Code_alpha = QTM32Code[1]

    context['QTMCode'] = QTMCode
    context['QTM32Code'] = QTM32Code_word
    context['QRS_GeoGnomo_Code'] = QTM32Code_alpha
    if alt32ID <> '':
        context['QRS_Quarternary_Code'] = QTM32Code_alpha + '@' + alt32ID

    left_neighbor = qrsGrid.LEFT_NEIGHBOR().QTMID()
    right_neighbor = qrsGrid.RIGHT_NEIGHBOR().QTMID()
    top_neighbor = qrsGrid.TOP_NEIGHBOR().QTMID()
    bottom_neighbor = qrsGrid.BOTTOM_NEIGHBOR().QTMID()

    Left_Neighbor_Code = encoder.getQTM32ID(str(left_neighbor))[1]
    Right_Neighbor_Code = encoder.getQTM32ID(str(right_neighbor))[1]
    Top_Neighbor_Code = encoder.getQTM32ID(str(top_neighbor))[1]
    Bottom_Neighbor_Code = encoder.getQTM32ID(str(bottom_neighbor))[1]

    left_abcd = qrs_decoder.QrsDecode(Left_Neighbor_Code, level).getABCD()
    right_abcd = qrs_decoder.QrsDecode(Right_Neighbor_Code, level).getABCD()
    top_abcd = qrs_decoder.QrsDecode(Top_Neighbor_Code, level).getABCD()
    bottom_abcd = qrs_decoder.QrsDecode(Bottom_Neighbor_Code, level).getABCD()

    context['Left_LatLonA'] = str((left_abcd[0]))
    context['Left_LatLonB'] = str((left_abcd[1]))
    context['Left_LatLonC'] = str((left_abcd[2]))
    context['Left_LatLonD'] = str((left_abcd[3]))
    context['Right_LatLonA'] = str((right_abcd[0]))
    context['Right_LatLonB'] = str((right_abcd[1]))
    context['Right_LatLonC'] = str((right_abcd[2]))
    context['Right_LatLonD'] = str((right_abcd[3]))
    context['Top_LatLonA'] = str((top_abcd[0]))
    context['Top_LatLonB'] = str((top_abcd[1]))
    context['Top_LatLonC'] = str((top_abcd[2]))
    context['Top_LatLonD'] = str((top_abcd[3]))
    context['Bottom_LatLonA'] = str((bottom_abcd[0]))
    context['Bottom_LatLonB'] = str((bottom_abcd[1]))
    context['Bottom_LatLonC'] = str((bottom_abcd[2]))
    context['Bottom_LatLonD'] = str((bottom_abcd[3]))

    context['Left_Neighbor'] = encoder.getQTM32ID(str(left_neighbor))[0]  # returns GeoGnomo code
    context['Right_Neighbor'] = encoder.getQTM32ID(str(right_neighbor))[0]
    context['Top_Neighbor'] = encoder.getQTM32ID(str(top_neighbor))[0]
    context['Bottom_Neighbor'] = encoder.getQTM32ID(str(bottom_neighbor))[0]

    abcd = qrs_decoder.QrsDecode(QTM32Code_alpha, level).getABCD()
    context['LatLonA'] = str((abcd[0]))
    context['LatLonB'] = str((abcd[1]))
    context['LatLonC'] = str((abcd[2]))
    context['LatLonD'] = str((abcd[3]))
    context['LatLonCenter'] = str((qrs_decoder.QrsDecode(QTM32Code_alpha, level).getCenter()))
    context['area'] = qrs_decoder.QrsDecode(QTM32Code_alpha, level).getArea()
    return context


def QRSIDToLatLon(qrs32code, level):
    context = {}
    QTM32Code = str(qrs32code).split("@")[0]
    if "@" in str(qrs32code):
        altitude = str(qrs32code).split("@")[1]
    else:
        altitude = "N/A"
    context['altitude'] = altitude
    level = int(level)
    rq = qrs_decoder.QrsDecode(QTM32Code, level)
    # get centroid lat lon from the given geognomo code
    CentralLatLon = rq.getCenter()
    context['LatLonCentral'] = str((CentralLatLon))
    # use centroid of the above rec to calc neighbouring codes
    latitude = rq.getCenter()[0]
    longitude = rq.getCenter()[1]
    # call the encoder function
    q = encoder.QrsGrid(latitude, longitude, level)  # The input order is Lon, Lat!!!!!!
    QTMCode = q.QTMID()
    QTM32Code = encoder.getQTM32ID(str(QTMCode))
    QTM32Code_alpha = QTM32Code[1]
    # get QTMID for neighbor polygons:
    l = q.LEFT_NEIGHBOR().QTMID()
    r = q.RIGHT_NEIGHBOR().QTMID()
    t = q.TOP_NEIGHBOR().QTMID()
    b = q.BOTTOM_NEIGHBOR().QTMID()
    # get base32 codes for neighbor polygons:
    Left_Neighbor_Code = encoder.getQTM32ID(str(l))[1]
    Right_Neighbor_Code = encoder.getQTM32ID(str(r))[1]
    Top_Neighbor_Code = encoder.getQTM32ID(str(t))[1]
    Bottom_Neighbor_Code = encoder.getQTM32ID(str(b))[1]
    # get latlon for the neighbor polygons:
    left_abcd = qrs_decoder.QrsDecode(Left_Neighbor_Code, level).getABCD()
    right_abcd = qrs_decoder.QrsDecode(Right_Neighbor_Code, level).getABCD()
    top_abcd = qrs_decoder.QrsDecode(Top_Neighbor_Code, level).getABCD()
    bottom_abcd = qrs_decoder.QrsDecode(Bottom_Neighbor_Code, level).getABCD()
    # store all relevant codes in dictionary:
    context['Left_LatLonA'] = str((left_abcd[0]))
    context['Left_LatLonB'] = str((left_abcd[1]))
    context['Left_LatLonC'] = str((left_abcd[2]))
    context['Left_LatLonD'] = str((left_abcd[3]))
    context['Right_LatLonA'] = str((right_abcd[0]))
    context['Right_LatLonB'] = str((right_abcd[1]))
    context['Right_LatLonC'] = str((right_abcd[2]))
    context['Right_LatLonD'] = str((right_abcd[3]))
    context['Top_LatLonA'] = str((top_abcd[0]))
    context['Top_LatLonB'] = str((top_abcd[1]))
    context['Top_LatLonC'] = str((top_abcd[2]))
    context['Top_LatLonD'] = str((top_abcd[3]))
    context['Bottom_LatLonA'] = str((bottom_abcd[0]))
    context['Bottom_LatLonB'] = str((bottom_abcd[1]))
    context['Bottom_LatLonC'] = str((bottom_abcd[2]))
    context['Bottom_LatLonD'] = str((bottom_abcd[3]))
    context['Left_Neighbor'] = encoder.getQTM32ID(str(l))[0]  # returns GeoGnomo code
    context['Right_Neighbor'] = encoder.getQTM32ID(str(r))[0]
    context['Top_Neighbor'] = encoder.getQTM32ID(str(t))[0]
    context['Bottom_Neighbor'] = encoder.getQTM32ID(str(b))[0]

    abcd = qrs_decoder.QrsDecode(QTM32Code_alpha, level).getABCD()
    context['LatLonA'] = str((abcd[0]))
    context['LatLonB'] = str((abcd[1]))
    context['LatLonC'] = str((abcd[2]))
    context['LatLonD'] = str((abcd[3]))
    context['area'] = qrs_decoder.QrsDecode(QTM32Code_alpha, level).getArea()
    return context


def LatLonToVRS(latitude1, longitude1, latitude2, longitude2):
    context = {}
    code32 = vrs_encoder.VrsCode(str(latitude1), str(longitude1), str(latitude2), str(longitude2))
    context['VRS_GeoGnomo_Code'] = str((code32))
    # following return lat-lon pair used for calculating the code
    QTM32Code = str(code32)
    pointA = vrs_decoder.VrsDecode(QTM32Code)[0]
    pointB = vrs_decoder.VrsDecode(QTM32Code)[1]
    context['area'] = vrs_decoder.VrsArea(pointA, pointB)
    context['LatLonA'] = str((pointA))
    context['LatLonB'] = str((pointB))
    context['LAT1'] = latitude1
    context['LON1'] = longitude1
    context['LAT2'] = latitude2
    context['LON2'] = longitude2
    return context


def VRSToLatLon(vrs32code):
    context = {}
    QTM32Code = str(vrs32code)
    pointA = vrs_decoder.VrsDecode(QTM32Code)[0]
    pointB = vrs_decoder.VrsDecode(QTM32Code)[1]
    context['area'] = vrs_decoder.VrsArea(pointA, pointB)
    context['LatLonA'] = str((pointA))
    context['LatLonB'] = str((pointB))
    return context


def LatLonToQUTMSID(latitude, longitude, altitude, level):
    context = {}

    level = int(level)
    gridBasedOnUserInput = encoder.QUTMSEncoder(latitude, longitude, level)
    altitudeBase32ID = encoder.getQrsAlt32ID(level, altitude)

    QTMCode = gridBasedOnUserInput.getQTMIDs()
    QTM32Code = encoder.getQUTMS32ID(str(QTMCode))
    QTM32Code_word = QTM32Code[0]
    QTM32Code_alpha = QTM32Code[1]

    context['QTMCode'] = QTMCode
    context['QTM32Code'] = QTM32Code_word
    context['QUTMS_GeoGnomo_Code'] = QTM32Code_alpha
    if altitudeBase32ID <> '':
        context['QUTMS_Quarternary_Code'] = QTM32Code_alpha + '@' + altitudeBase32ID

    latlonCenter = decoder.QUTMSDecoder(QTM32Code_alpha, level).getCenter()  # used this to get connected latlon
    context['LatLonCenter'] = str(latlonCenter)
    LatCenter = latlonCenter[0]
    LonCenter = latlonCenter[1]
    calculatedQtmsGrid = encoder.QUTMSEncoder(LatCenter, LonCenter, level)

    leftNeighbor = calculatedQtmsGrid.LEFT_NEIGHBOR().getQTMIDs()
    rightNeighbor = calculatedQtmsGrid.RIGHT_NEIGHBOR().getQTMIDs()
    topNeighbor = calculatedQtmsGrid.TOP_NEIGHBOR().getQTMIDs()
    bottomNeighbor = calculatedQtmsGrid.BOTTOM_NEIGHBOR().getQTMIDs()

    Left_Neighbor_Code = encoder.getQUTMS32ID(str(leftNeighbor))[1]
    Right_Neighbor_Code = encoder.getQUTMS32ID(str(rightNeighbor))[1]
    Top_Neighbor_Code = encoder.getQUTMS32ID(str(topNeighbor))[1]
    Bottom_Neighbor_Code = encoder.getQUTMS32ID(str(bottomNeighbor))[1]

    left_abcd = decoder.QUTMSDecoder(Left_Neighbor_Code, level).getABCD()
    right_abcd = decoder.QUTMSDecoder(Right_Neighbor_Code, level).getABCD()
    top_abcd = decoder.QUTMSDecoder(Top_Neighbor_Code, level).getABCD()
    bottom_abcd = decoder.QUTMSDecoder(Bottom_Neighbor_Code, level).getABCD()

    context['Left_LatLonA'] = str((left_abcd[0]))
    context['Left_LatLonB'] = str((left_abcd[1]))
    context['Left_LatLonC'] = str((left_abcd[2]))
    context['Left_LatLonD'] = str((left_abcd[3]))
    context['Right_LatLonA'] = str((right_abcd[0]))
    context['Right_LatLonB'] = str((right_abcd[1]))
    context['Right_LatLonC'] = str((right_abcd[2]))
    context['Right_LatLonD'] = str((right_abcd[3]))
    context['Top_LatLonA'] = str((top_abcd[0]))
    context['Top_LatLonB'] = str((top_abcd[1]))
    context['Top_LatLonC'] = str((top_abcd[2]))
    context['Top_LatLonD'] = str((top_abcd[3]))
    context['Bottom_LatLonA'] = str((bottom_abcd[0]))
    context['Bottom_LatLonB'] = str((bottom_abcd[1]))
    context['Bottom_LatLonC'] = str((bottom_abcd[2]))
    context['Bottom_LatLonD'] = str((bottom_abcd[3]))

    context['Left_Neighbor'] = encoder.getQUTMS32ID(str(leftNeighbor))[0]  # returns GeoGnomo code
    context['Right_Neighbor'] = encoder.getQUTMS32ID(str(rightNeighbor))[0]
    context['Top_Neighbor'] = encoder.getQUTMS32ID(str(topNeighbor))[0]
    context['Bottom_Neighbor'] = encoder.getQUTMS32ID(str(bottomNeighbor))[0]

    abcd = decoder.QUTMSDecoder(QTM32Code_alpha, level).getABCD()
    context['LatLonA'] = str((abcd[0]))
    context['LatLonB'] = str((abcd[1]))
    context['LatLonC'] = str((abcd[2]))
    context['LatLonD'] = str((abcd[3]))
    context['area'] = decoder.QUTMSDecoder(QTM32Code_alpha, level).getArea()
    return context


def QUTMSIDToLatLon(qutms32code, level):
    context = {}
    QTM32Code = str(qutms32code).split("@")[0]
    if "@" in str(qutms32code):
        altitude = str(qutms32code).split("@")[1]
    else:
        altitude = "N/A"
    context['altitude'] = altitude
    level = int(level)
    rq = decoder.QUTMSDecoder(QTM32Code, level)
    # get centroid lat lon from the given geognomo code
    LatLonCenter = rq.getCenter()
    context['LatLonCenter'] = str((LatLonCenter))
    # use centroid of the above rec to calc neighbouring codes
    Lat = rq.getCenter()[0]
    Lon = rq.getCenter()[1]

    q = encoder.QUTMSEncoder(Lat, Lon, level)
    QTMCode = q.getQTMIDs()
    QTM32Code = encoder.getQUTMS32ID(str(QTMCode))
    QTM32Code_alpha = QTM32Code[1]

    l = q.LEFT_NEIGHBOR().getQTMIDs()
    r = q.RIGHT_NEIGHBOR().getQTMIDs()
    t = q.TOP_NEIGHBOR().getQTMIDs()
    b = q.BOTTOM_NEIGHBOR().getQTMIDs()
    # get base32 codes for neighbor polygons:
    Left_Neighbor_Code = encoder.getQUTMS32ID(str(l))[1]
    Right_Neighbor_Code = encoder.getQUTMS32ID(str(r))[1]
    Top_Neighbor_Code = encoder.getQUTMS32ID(str(t))[1]
    Bottom_Neighbor_Code = encoder.getQUTMS32ID(str(b))[1]
    # get latlon for the neighbor polygons:
    left_abcd = decoder.QUTMSDecoder(Left_Neighbor_Code, level).getABCD()
    right_abcd = decoder.QUTMSDecoder(Right_Neighbor_Code, level).getABCD()
    top_abcd = decoder.QUTMSDecoder(Top_Neighbor_Code, level).getABCD()
    bottom_abcd = decoder.QUTMSDecoder(Bottom_Neighbor_Code, level).getABCD()

    # store all relevant codes in dictionary:
    context['Left_LatLonA'] = str((left_abcd[0]))
    context['Left_LatLonB'] = str((left_abcd[1]))
    context['Left_LatLonC'] = str((left_abcd[2]))
    context['Left_LatLonD'] = str((left_abcd[3]))
    context['Right_LatLonA'] = str((right_abcd[0]))
    context['Right_LatLonB'] = str((right_abcd[1]))
    context['Right_LatLonC'] = str((right_abcd[2]))
    context['Right_LatLonD'] = str((right_abcd[3]))
    context['Top_LatLonA'] = str((top_abcd[0]))
    context['Top_LatLonB'] = str((top_abcd[1]))
    context['Top_LatLonC'] = str((top_abcd[2]))
    context['Top_LatLonD'] = str((top_abcd[3]))
    context['Bottom_LatLonA'] = str((bottom_abcd[0]))
    context['Bottom_LatLonB'] = str((bottom_abcd[1]))
    context['Bottom_LatLonC'] = str((bottom_abcd[2]))
    context['Bottom_LatLonD'] = str((bottom_abcd[3]))
    context['Left_Neighbor'] = encoder.getQUTMS32ID(str(l))[0]  # returns GeoGnomo code
    context['Right_Neighbor'] = encoder.getQUTMS32ID(str(r))[0]
    context['Top_Neighbor'] = encoder.getQUTMS32ID(str(t))[0]
    context['Bottom_Neighbor'] = encoder.getQUTMS32ID(str(b))[0]

    # Get same data for the centroid
    abcd = decoder.QUTMSDecoder(QTM32Code_alpha, level).getABCD()
    context['LatLonA'] = str((abcd[0]))
    context['LatLonB'] = str((abcd[1]))
    context['LatLonC'] = str((abcd[2]))
    context['LatLonD'] = str((abcd[3]))
    context['area'] = decoder.QUTMSDecoder(QTM32Code_alpha, level).getArea()

    return context

