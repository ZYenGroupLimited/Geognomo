from __future__ import division
import numpy
import math
import integer2base
import base32_data

BASE32DATA = base32_data.getBase32Data()


class IcoEncoder:

    def __init__(self, latitude, longitude, level):
        self.latitude = float(latitude) * math.pi / 180  # degrees to radians
        # convert longitude so that it goes from 0 to 360
        # degrees heading East from the prime meridian
        if float(longitude) < 0:
            longitude = float(longitude) + 360
        self.longitude = float(longitude) * math.pi / 180
        self.level = int(level)

    def icosahedron(self):
        latitude = self.latitude
        longitude = self.longitude
        # Top Pyramid
        if latitude >= math.atan(0.5):
            icosahedron = int(5 * longitude / (2 * math.pi)) + 1
        # Bottom Pyramid - offset angle with Top Pyramid is math.pi/5
        elif latitude <= math.atan(-0.5):
            icosahedron = int(5 * (longitude - math.pi / 5) / (2 * math.pi)) + 16
            if icosahedron == 15:
                icosahedron = 20
        # Middle Band
        else:
            # Initial Middle Band Division
            topPyramidAbove = int(5 * longitude / (2 * math.pi))
            a = numpy.matrix([[topPyramidAbove * 2 * math.pi / 5, 1],
                              [topPyramidAbove * 2 * math.pi / 5 + math.pi / 5, 1]])
            b = numpy.array([math.atan(0.5), math.atan(-0.5)])
            leftEdges = numpy.linalg.solve(a, b)
            c = numpy.matrix([[((topPyramidAbove + 1)) * 2 * math.pi / 5, 1],
                              [topPyramidAbove * 2 * math.pi / 5 + math.pi / 5, 1]])
            d = numpy.array([math.atan(0.5), math.atan(-0.5)])
            rightEdges = numpy.linalg.solve(c, d)
            if latitude < leftEdges[0] * longitude + leftEdges[1]:
                if topPyramidAbove == 0:
                    icosahedron = 15
                else:
                    icosahedron = topPyramidAbove + 10
            if latitude >= leftEdges[0] * longitude + leftEdges[1] and latitude > rightEdges[0] * longitude \
                    + rightEdges[1]:
                icosahedron = topPyramidAbove + 6
            if latitude <= rightEdges[0] * longitude + rightEdges[1]:
                icosahedron = topPyramidAbove + 11
        return icosahedron

    def covertToXY(self):
        latitude = self.latitude
        longitude = self.longitude
        level = self.level
        icosahedron = self.icosahedron()
        # move the left corner to (0,0)
        if icosahedron <= 5:
            longitude = longitude - ((icosahedron - 1) * 2 * math.pi / 5)
            latitude = latitude - math.atan(0.5)
        elif icosahedron > 5 and icosahedron <= 10:
            longitude = longitude - ((icosahedron - 6) * 2 * math.pi / 5)
            latitude = math.atan(0.5) - latitude
        elif icosahedron > 10 and icosahedron <= 15:
            longitude = longitude - math.pi / 5 - ((icosahedron - 11) * 2 * math.pi / 5)
            latitude = latitude + math.atan(0.5)
            if longitude < 0:
                longitude = longitude + 2 * math.pi
        else:
            longitude = longitude - math.pi / 5 - ((icosahedron - 16) * 2 * math.pi / 5)
            latitude = -latitude - math.atan(0.5)
            if longitude < 0:
                longitude = longitude + 2 * math.pi
        # Top & Bottom Pyramid
        if icosahedron <= 5 or icosahedron >= 16:
            r = latitude / (math.pi / 2 - math.atan(0.5))
            pointX = 2 ** (level - 1) * (r + 5 * longitude * (1 - r) / math.pi)
            pointY = 2 ** (level - 1) * math.sqrt(3) * r
        # Middle Band
        else:
            pointX = (5 * 2 ** (level - 1) * longitude) / math.pi
            pointY = (2 ** (level - 2) * math.sqrt(3) * latitude) / math.atan(0.5)
        pointXY = (pointX, pointY)
        c = "lat: " + str(self.latitude) + ", lon:" + str(self.longitude) + ", x:" + str(pointX) + ", y:" + str(pointY)
        return pointXY

    def getRowCol(self):
        maxNumberOfColumn = 2 ** (self.level - 1) * math.sqrt(3)
        maxNumberOfRow = 2 ** self.level
        if abs(self.latitude) == 90:
            row = 2 ** self.level
            column = 1
        else:
            pointXY = self.covertToXY()
            row = int(abs(pointXY[1]) * maxNumberOfRow / maxNumberOfColumn) + 1
            column = 2 * int(pointXY[0] - (row - 1) / float(2)) + 1
        return row, column


def getABCD(rowIndex, columnIndex): #change to getVertexABCD
    pointAx = (rowIndex - 1) / float(2) + (columnIndex - 1) / float(2)
    pointAy = math.sqrt(3) * (rowIndex - 1) / float(2)
    pointBx = rowIndex / float(2) + (columnIndex - 1) / float(2)
    pointBy = math.sqrt(3) * rowIndex / float(2)
    pointCx = rowIndex / float(2) + columnIndex / float(2)
    pointCy = math.sqrt(3) * (rowIndex - 1) / float(2)
    pointDx = rowIndex / float(2) + (columnIndex - 1) / float(2) + float(1)
    pointDy = math.sqrt(3) * rowIndex / float(2)
    return [(pointAx, pointAy), (pointBx, pointBy), (pointCx, pointCy), (pointDx, pointDy)]


def getABC(rowIndex, columnIndex): #change to getVertexABC
    if columnIndex % 2 != 0:
        pointAx = (rowIndex - 1) / float(2) + (columnIndex - 1) / float(2)
        pointAy = math.sqrt(3) * (rowIndex - 1) / float(2)
        pointBx = rowIndex / float(2) + (columnIndex - 1) / float(2)
        pointBy = math.sqrt(3) * rowIndex / float(2)
        pointCx = rowIndex / float(2) + columnIndex / float(2)
        pointCy = math.sqrt(3) * (rowIndex - 1) / float(2)
        return [(pointAx, pointAy), (pointBx, pointBy), (pointCx, pointCy)]
    else:
        pointBx = rowIndex / float(2) + (columnIndex - 2) / float(2)
        pointBy = math.sqrt(3) * rowIndex / float(2)
        pointDx = rowIndex / float(2) + columnIndex / float(2)
        pointDy = math.sqrt(3) * rowIndex / float(2)
        pointCx = rowIndex / float(2) + (columnIndex - 1) / float(2)
        pointCy = math.sqrt(3) * (rowIndex - 1) / float(2)
        return [(pointBx, pointBy), (pointDx, pointDy), (pointCx, pointCy)]


def getAdjustedRowCol(latitude, longitude, level):
    qtm = IcoEncoder(latitude, longitude, level)
    pointXY = qtm.covertToXY()
    pointX = pointXY[0]
    pointY = pointXY[1]
    rowColumn = qtm.getRowCol()
    adjustedRow = rowColumn[0]
    adjustedColumn = rowColumn[1]
    # Left side
    if (pointY - math.sqrt(3) * pointX) > ((1 - adjustedColumn) * math.sqrt(3) / float(2)):
        adjustedColumn = adjustedColumn - 1
    # Right side
    else:
        if (pointY + math.sqrt(3) * pointX > math.sqrt(3) * (adjustedRow + (adjustedColumn - 1) / float(2))):
            adjustedColumn = adjustedColumn + 1
    return (adjustedRow, adjustedColumn)


def EAST_NEIGHBOR_ICOS(icosahedron):
    return (icosahedron + 1 - 5 * (icosahedron > 4) + 9 * (icosahedron > 5) - 9 * (icosahedron > 10) - 5 * (icosahedron > 14) + 10 * (icosahedron > 15) - 5 * (icosahedron == 20))


def WEST_NEIGHBOR_ICOS(icosahedron):
    return (icosahedron + 4 - 5 * (icosahedron > 1) + 10 * (icosahedron > 5) - 5 * (icosahedron > 6) - 9 * (icosahedron > 10) + 9 * (icosahedron > 15) - 5 * (icosahedron > 16))


def NORTH_NEIGHBOR_ICOS(icosahedron):
    return (((icosahedron - 1) % 10 > 4) * (icosahedron - 5))


def SOUTH_NEIGHBOR_ICOS(icosahedron):
    return (((icosahedron - 1) % 10 < 5) * (icosahedron + 5))


def LEFT_NEIGHBOR(level, rowIndex, columnIndex, icosahedron):
    ai = rowIndex
    if columnIndex == 1:
        if icosahedron >= 6 and icosahedron <= 15:
            rowIndex = 2 ** level + 1 - rowIndex
        else:
            rowIndex = ai
        columnIndex = 2 * (2 ** level - rowIndex) + 1
        leftNeighborIcosahedron = WEST_NEIGHBOR_ICOS(icosahedron)
    else:
        rowIndex = ai
        columnIndex = columnIndex - 1
        leftNeighborIcosahedron = icosahedron
    return (leftNeighborIcosahedron, rowIndex, columnIndex)


def RIGHT_NEIGHBOR(level, rowIndex, columnIndex, icosahedron):
    ai = rowIndex
    if columnIndex == 2 * (2 ** level - rowIndex) + 1:
        if icosahedron >= 6 and icosahedron <= 15:
            rowIndex = 2 ** level + 1 - rowIndex
        else:
            rowIndex = ai
        columnIndex = 1
        rightNeighborIcosahedron = EAST_NEIGHBOR_ICOS(icosahedron)
    else:
        rowIndex = ai
        columnIndex = columnIndex + 1
        rightNeighborIcosahedron = icosahedron
    return (rightNeighborIcosahedron, rowIndex, columnIndex)


def TOP_NEIGHBOR(level, rowIndex, columnIndex, icosahedron): #TODO: remove level
    if rowIndex == 1:
        if math.ceil(float(icosahedron) / 5) % 2 == 0 and columnIndex % 2 != 0:
            topNeighborIcosahedron = NORTH_NEIGHBOR_ICOS(icosahedron)
        # if triangle direction is positive
        elif math.ceil(float(icosahedron) / 5) % 2 != 0 and columnIndex % 2 != 0:
            topNeighborIcosahedron = SOUTH_NEIGHBOR_ICOS(icosahedron)
        else:
            topNeighborIcosahedron = icosahedron
            rowIndex = rowIndex + 1
            columnIndex = columnIndex - 1
    else:
        if columnIndex % 2 == 0:
            rowIndex = rowIndex + 1
            columnIndex = columnIndex - 1
        else:
            rowIndex = rowIndex - 1
            columnIndex = columnIndex + 1
        topNeighborIcosahedron = icosahedron
    return (topNeighborIcosahedron, rowIndex, columnIndex)


def getQTMIDs(level, rowIndex, columnIndex, icosahedron):
    # Find out each digit of geocode
    n = 2 ** level
    QTMID_list = []
    for k in range(0, level):
        if rowIndex > n / 2:
            # Top - reset i
            QTMID_list.append(1)
            n = n / 2
            rowIndex = rowIndex - n
        else:
            # left corner
            if columnIndex < 2 * (n / 2 - rowIndex + 1):
                QTMID_list.append(2)
                n = n / 2
            else:
                # right corner - reset j
                if columnIndex > n:
                    QTMID_list.append(3)
                    n = n / 2
                    columnIndex = columnIndex - 2 * n
                else:
                    # center
                    QTMID_list.append(0)
                    columnIndex = columnIndex - n + 2 * rowIndex - 1
                    rowIndex = n / 2 - rowIndex + 1
                    n = n / 2
    QTMID = ''.join([str(e) for e in QTMID_list])
    return str(icosahedron) + "," + QTMID


def getQTM32ID(QTMID):
    QTMID_list = list(str(QTMID).split(",")[1])
    icosahedron = str(QTMID).split(",")[0]
    bin_list = []
    for e in QTMID_list:
        if e == '0':
            bin_list.extend((0, 0))
        if e == '1':
            bin_list.extend((0, 1))
        if e == '2':
            bin_list.extend((1, 0))
        if e == '3':
            bin_list.extend((1, 1))
    bin_str = ''.join([str(e) for e in bin_list])
    remainder = len(bin_str) % 5
    appendStr = ''
    if remainder != 0:  # if remainder is 0 it means its multiple of five
        for num in range(0, 5 - remainder):  # number of 0 we want to add to make it multiple of 5
            appendStr += "0"
    bin_str = bin_str[:len(bin_str) - remainder] + appendStr + bin_str[len(bin_str) - remainder:]
    n = 5
    bin32_list = [bin_str[i: i + n] for i in range(0, len(bin_str), n)]  # making chuck of five bits
    QTM32ID_list = []
    QTM32ID_alphalist = []
    base32Word = ''
    base32Code = ''
    for i in bin32_list:
        for d in BASE32DATA:
            if i == d['Binary Code']:
                base32Word = d['Word']
                base32Code = d['Code']
        QTM32ID_list.append(base32Word)
        QTM32ID_alphalist.append(base32Code)
    QTM32ID_str = ','.join([str(e) for e in QTM32ID_list])
    QTM32ID_alpha = ''.join([str(e) for e in QTM32ID_alphalist])
    icosahedronWordRepresentation = ''
    icosahedronCodeRepresentation = ''
    for d in BASE32DATA:
        if int(icosahedron) == d['Decimal']:
            icosahedronWordRepresentation = d['Word']
            icosahedronCodeRepresentation = d['Code']
    return (str(icosahedronWordRepresentation) + "," + QTM32ID_str, str(icosahedronCodeRepresentation) + QTM32ID_alpha)


def getAlt32ID(level, altitude):  #TODO: getAltitudeBase32ID
    altitude = float(altitude)
    averageRadiusOfEarth = 6378137
    circumference = 2 * math.pi * averageRadiusOfEarth
    n = (2 ** level) * 5
    average = circumference / n
    if altitude >= 0:
        sign = 1
    else:
        sign = -1
    alt = int(math.ceil((sign * altitude) / average))
    altitudeID = integer2base.int2base(sign * alt, 32)
    altitudeCode = ''
    altitudeBase32ID = []
    if sign < 0:
        altitudeBase32ID.append('-')
    for i in altitudeID.split(','):
        for data in BASE32DATA:
            if i == str(data['Decimal'] + 1):
                altitudeCode = data['Code']
        altitudeBase32ID.append(altitudeCode)
    return ''.join([str(i) for i in altitudeBase32ID])


class QUTMSEncoder:

    def __init__(self, latitude, longitude, level):
        # adjust ranges
        self.latitude = float(latitude) + 90
        self.longitude = float(longitude) + 180
        self.level = int(level)

    def mgrs(self):  # latitude bands
        latitude = self.latitude
        longitude = self.longitude

        latzones = ['C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M',
                    'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']
        zone = []
        # NOTE: pad 0 in front of digits/letter to ensure the UTM Zone code is always 3 char long!!!
        # North Pole
        if latitude >= 174:
            if longitude >= 180:
                zone = ('00Z')
                return str(zone)
            if longitude < 180:
                zone = ('00Y')
                return str(zone)

        # South Pole
        if latitude < 10:
            if longitude >= 180:
                zone = ('00B')
                return str(zone)
            if longitude < 180:
                zone = ('00A')
                return str(zone)

        latitude = latitude - 10
        m = int(math.ceil(latitude / 8))
        if m == 21:
            m = int(20)
        num = int(math.ceil(longitude / 6))
        num = '{:02d}'.format(num)  # pads Zero in front if single digit
        zone.insert(0, int(num))  # zone[0]=math.ceil(lon/6
        zone.insert(1, latzones[m - 1])  # zone[1]=latzones[m-1]

        if m == 20 and zone[
            0] == 32:  # exceptions to grid (check in paper for more info- the rectangle size is different than normal.)
            if longitude < 189:
                zone[0] = 31
            if longitude >= 189:
                zone[0] = 33
        if m == 20 and zone[0] == 34:
            if longitude < 201:
                zone[0] = 33
            if longitude >= 201:
                zone[0] = 35
        if m == 20 and zone[0] == 36:
            if longitude < 213:
                zone[0] = 35
            if longitude >= 213:
                zone[0] = 37
        if m == 18 and zone[0] == 31:
            if longitude >= 183:
                zone[0] = 32

        mgrs = ''.join(map(str, zone))
        return mgrs

    def getZoneDim(self):
        zone = list(self.mgrs())
        getZoneDim = [0, 0, 0]
        latzones = ['C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M',
                    'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']

        if zone == ['0', '0', 'A']:
            getZoneDim = [(0, 0), 10, 180]
            return getZoneDim
        elif zone == ['0', '0', 'B']:
            getZoneDim = [(0, 180), 10, 180]
            return getZoneDim
        elif zone == ['0', '0', 'Y']:
            getZoneDim = [(174, 0), 6, 180]
            return getZoneDim
        elif zone == ['0', '0', 'Z']:
            getZoneDim = [(174, 180), 6, 180]
            return getZoneDim
        elif zone == ['3', '1', 'X']:
            getZoneDim = [(72, 180), 12, 9]
            return getZoneDim
        elif zone == ['3', '3', 'X']:
            getZoneDim = [(72, 189), 12, 12]
            return getZoneDim
        elif zone == ['3', '5', 'X']:
            getZoneDim = [(72, 201), 12, 12]
            return getZoneDim
        elif zone == ['3', '7', 'X']:
            getZoneDim = [(72, 213), 12, 9]
            return getZoneDim
        elif zone == ['3', '1', 'V']:
            getZoneDim = [(56, 180), 8, 3]
            return getZoneDim
        elif zone == ['3', '2', 'V']:
            getZoneDim = [(56, 183), 8, 9]
            return getZoneDim
        else:
            lonzone = [zone[0], zone[1]]
            lonzone = ''.join(map(str, lonzone))  # joins the longitude code digits
            for index, item in enumerate(latzones):
                if item == zone[2]:
                    left = (((index + 1) * 8 + 2), (int(lonzone) * 6 - 6))  # get the leftcorner point
                    getZoneDim = [left, 8, 6]
                    return getZoneDim

    def LEFT_NEIGHBOR(self):
        latitude = self.latitude - 90  # get the original latitude value
        longitude = self.longitude - 180  # get the orignal longitude value
        zone = self.mgrs()
        level = self.level
        # exceptions
        if zone == '00Y':  # first four are polar regions
            londim = 180 / 2 ** level
            longitude += londim
        elif zone == '00Z':
            londim = 180 / 2 ** level
            longitude += londim
        elif zone == '00A':
            londim = 180 / 2 ** level
            longitude += londim
        elif zone == '00B':
            londim = 180 / 2 ** level
            longitude += londim
        elif zone == '31X':
            londim = 9 / 2 ** level
            longitude += londim
        elif zone == '33X':
            londim = 12 / 2 ** level
            longitude += londim
        elif zone == '35X':
            londim = 12 / 2 ** level
            longitude += londim
        elif zone == '37X':
            londim = 9 / 2 ** level
            longitude += londim
        elif zone == '32V':
            londim = 9 / 2 ** level
            longitude += londim
        elif zone == '31V':
            londim = 3 / 2 ** level
            longitude += londim
        else:
            londim = 6 / 2 ** level  # NOTE: GENERIC CASE!
            longitude += londim

        return (QUTMSEncoder(latitude, longitude, level))

    def RIGHT_NEIGHBOR(self):
        latitude = self.latitude - 90
        longitude = self.longitude - 180
        zone = self.mgrs()
        level = self.level
        # exceptions
        if zone == '00Y':  # first four are polar regions
            londim = 180 / 2 ** level
            longitude -= londim
        elif zone == '00Z':
            londim = 180 / 2 ** level
            longitude -= londim
        elif zone == '00A':
            londim = 180 / 2 ** level
            longitude -= londim
        elif zone == '00B':
            londim = 180 / 2 ** level
            longitude -= londim
        elif zone == '33X':
            londim = 9 / 2 ** level
            longitude -= londim
        elif zone == '35X':
            londim = 12 / 2 ** level
            longitude -= londim
        elif zone == '37X':
            londim = 12 / 2 ** level
            longitude -= londim
        elif zone == '32V':
            londim = 3 / 2 ** level
            longitude -= londim
        else:
            londim = 6 / 2 ** level  # NOTE: GENERIC CASE!
            longitude -= londim

        return (QUTMSEncoder(latitude, longitude, level))

    def TOP_NEIGHBOR(self):
        level = self.level
        latitude = self.latitude - 90
        longitude = self.longitude - 180
        zone = self.mgrs()
        # exceptions
        if zone == '00Y':
            latdim = 6 / 2 ** level
            latitude += latdim
        elif zone == '00Z':
            latdim = 6 / 2 ** level
            latitude += latdim
        elif zone == '00A':
            latdim = 10 / 2 ** level
            latitude += latdim
        elif zone == '00B':
            latdim = 10 / 2 ** level
            latitude += latdim
        elif 'X' in zone[0]:
            latdim = 12 / 2 ** level
            latitude += latdim
        else:
            latdim = 8 / 2 ** level  # GENERIC CASE
            latitude += latdim
        return (QUTMSEncoder(latitude, longitude, level))

    def BOTTOM_NEIGHBOR(self):
        level = self.level
        latitude = self.latitude - 90
        longitude = self.longitude - 180
        zone = self.mgrs()
        # Exceptions
        if zone == '00Y':
            latdim = 12 / 2 ** level
            latitude -= latdim
        elif zone == '00Z':
            latdim = 12 / 2 ** level
            latitude -= latdim
        elif zone == '00A':
            latdim = 10 / 2 ** level
            latitude -= latdim
        elif zone == '00B':
            latdim = 10 / 2 ** level
            latitude -= latdim
        else:
            latdim = 8 / 2 ** level  # GENERIC CASE
            latitude -= latdim
        return (QUTMSEncoder(latitude, longitude, level))

    def getQTMIDs(self):
        # Find out each digit of geocode

        level = self.level
        latitude = self.latitude
        longitude = self.longitude
        zone = self.mgrs()
        getZoneDim = self.getZoneDim()

        left = getZoneDim[0]
        latdim = getZoneDim[1]
        londim = getZoneDim[2]

        latitude = latitude - left[0]
        longitude = longitude - left[1]

        code = [0] * level

        for i in range(0, level):
            if longitude < londim / 2:
                if latitude < latdim / 2:
                    code[i] = 2
                else:
                    code[i] = 0
                    latitude -= (latdim / 2)
            else:
                if latitude < latdim / 2:
                    code[i] = 3
                    longitude -= (londim / 2)
                else:
                    code[i] = 1
                    latitude -= (latdim / 2)
                    longitude -= (londim / 2)
            latdim /= 2
            londim /= 2
        QTMID = ''.join(map(str, code))
        return str(zone) + "," + QTMID


def getQUTMS32ID(QTMID):

    QTMID_list = list(str(QTMID).split(",")[1])
    icos = str(QTMID).split(",")[0]

    bin_list = []
    for e in QTMID_list:
        if e == '0':
            bin_list.extend((0, 0))
        if e == '1':
            bin_list.extend((0, 1))
        if e == '2':
            bin_list.extend((1, 0))
        if e == '3':
            bin_list.extend((1, 1))
    bin_str = ''.join([str(e) for e in bin_list])
    remainder = len(bin_str) % 5  # counting remainder
    appendStr = ''
    if remainder != 0:  # if remainder is 0 it means its multiple of five
        for num in range(0, 5 - remainder):  # number of 0 we want to add to make it multiple of 5
            appendStr += "0"
    bin_str = bin_str[:len(bin_str) - remainder] + appendStr + bin_str[len(bin_str) - remainder:]
    n = 5
    bin32_list = [bin_str[i:i + n] for i in range(0, len(bin_str), n)]  # making chuck of five bits
    #print ("bin32_list" + str(bin32_list))
    # same old code
    QTM32ID_list = []
    QTM32ID_alphalist = []
    w = ''
    c = ''
    for i in bin32_list:
        for d in BASE32DATA:
            if i == d['Binary Code']:
                w = d['Word']
                c = d['Code']
        QTM32ID_list.append(w)
        QTM32ID_alphalist.append(c)
    QTM32ID_str = ','.join([str(e) for e in QTM32ID_list])
    QTM32ID_alpha = ''.join([str(e) for e in QTM32ID_alphalist])

    return (str(icos) + "-" + QTM32ID_str, str(icos) + "-" + QTM32ID_alpha)


class QrsGrid:

    def __init__(self, latitude, longitude, level):
        self.latitude = float(latitude) + 90
        if float(longitude) < 0:
            self.longitude = float(longitude) + 360
        else:
            self.longitude = float(longitude)
        self.level = int(level)

    def rectangle(self):
        latitude = self.latitude
        longitude = self.longitude
        if latitude < 60:
            rectangle = int(math.floor(longitude / 60) + 13)
        elif 120 > latitude >= 60:
            rectangle = int(math.floor(longitude / 60) + 7)
        elif latitude >= 120:
            rectangle = int(math.floor(longitude / 60) + 1)
        return rectangle

    def QTMID(self):
        latitude = self.latitude
        longitude = self.longitude
        level = self.level
        leftpoint = [0, 0]
        rectangle = int(self.rectangle())
        if rectangle < 7:
            leftpoint[0] = 120
            leftpoint[1] = (rectangle - 1) * 60
        elif 13 > rectangle >= 7:
            leftpoint[0] = 60
            leftpoint[1] = (rectangle - 7) * 60
        elif rectangle > 12:
            leftpoint[0] = 0
            leftpoint[1] = (rectangle - 13) * 60
        code = [1] * level
        latdim = float(60)
        londim = float(60)
        latitude -= leftpoint[0]
        longitude -= leftpoint[1]
        for i in range(0, level):
            if longitude < londim / 2:
                if latitude < latdim / 2:
                    code[i] = 2
                else:
                    code[i] = 0
                    latitude -= (latdim / 2)
            if longitude >= londim / 2:
                if latitude < latdim / 2:
                    code[i] = 3
                    longitude -= (londim / 2)
                else:
                    code[i] = 1
                    latitude -= (latdim / 2)
                    longitude -= (londim / 2)
            latdim /= 2
            londim /= 2
        conc_code = ''.join(map(str, code))
        return str(rectangle) + "," + conc_code

    def LEFT_NEIGHBOR(self):
        leftlatitude = self.latitude - 90
        if self.longitude < 180:
            leftlongitude = self.longitude - 360
        else:
            leftlongitude = self.longitude
        level = int(self.level)
        londim = 60 / 2 ** level
        if leftlongitude < londim - 180:
            leftlongitude += 360 - londim
        else:
            leftlongitude -= londim
        return QrsGrid(leftlatitude, leftlongitude, level)

    def RIGHT_NEIGHBOR(self):
        latitude = self.latitude - 90
        if self.longitude < 180:
            longitude = self.longitude - 360
        else:
            longitude = self.longitude
        level = int(self.level)
        londim = 60 / 2 ** level
        if longitude > 180 - londim:
            longitude -= (360 - londim)
        else:
            longitude += londim
        return QrsGrid(latitude, longitude, level)

    def TOP_NEIGHBOR(self):
        latitude = self.latitude - 90
        if self.longitude < 180:
            longitude = self.longitude - 360
        else:
            longitude = self.longitude
        level = int(self.level)
        latdim = 60 / 2 ** level

        if latitude > 90 - latdim:
            if longitude < 0:
                longitude += 180
            else:
                longitude -= 180
        else:
            latitude += latdim
        return QrsGrid(latitude, longitude, level)

    def BOTTOM_NEIGHBOR(self):
        latitude = self.latitude - 90
        if self.longitude < 180:
            longitude = self.longitude - 360
        else:
            longitude = self.longitude
        level = int(self.level)
        latdim = 60 / 2 ** level
        if latitude < latdim - 90:
            if longitude < 0:
                longitude += 180
            else:
                longitude -= 180
        else:
            latitude -= latdim
        return QrsGrid(latitude, longitude, level)


def getQrsAlt32ID(level, altitude):
    altitude = float(altitude)
    equatorialEarthRadius = 6378137
    earthCircumference = 2 * math.pi * equatorialEarthRadius
    n = (2 ** level) * 3

    avg = earthCircumference / n
    if altitude >= 0:
        sign = 1
    else:
        sign = - 1

    alt = int(math.ceil((sign * altitude) / avg))
    altID = integer2base.int2base(sign * alt, 32)
    c = ''
    alt32ID = []
    if sign < 0:
        alt32ID.append('-')
    for i in altID.split(','):
        for d in BASE32DATA:
            if i == str(d['Decimal'] + 1):
                c = d['Code']
        alt32ID.append(c)
    return ''.join([str(i) for i in alt32ID])
