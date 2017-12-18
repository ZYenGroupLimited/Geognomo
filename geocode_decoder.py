from __future__ import division
import os, math, json
import base32_data

base32Data = base32_data.getBase32Data()

class IcoDecoder:
    def __init__(self, id, k):
        self.id = str(id)
        self.k = int(k)

    def icos(self):
        if "," in self.id:
            QTM32ID_list = self.id.split(',')
            for d in base32Data:
                if d['Word'] == QTM32ID_list[0]:
                    icos = d['Decimal']
        else:
            QTM32ID_alphalist = list(self.id)
            for d in base32Data:
                if d['Code'] == QTM32ID_alphalist[0]:
                    icos = d['Decimal']
        icos = int(icos)
        return icos

    def covertToQTMIDs(self):
        if "," in self.id:
            QTM32ID_list = self.id.split(',')
            t = '';
            bin32_list = []
            for i in QTM32ID_list[1:]:
                for d in base32Data:
                    if i == d['Word']:
                        t = d['Binary Code']
                        #print t
                bin32_list.append(t)
        else:
            QTM32ID_alphalist = list(self.id)
            t = '';
            bin32_list = []
            for i in QTM32ID_alphalist[1:]:
                for d in base32Data:
                    if i == d['Code']:
                        t = d['Binary Code']
                bin32_list.append(t)

        #print "bin32_list" + str(bin32_list)
        bin32_str = ''.join([str(e) for e in bin32_list])
        if len(bin32_str) != self.k * 2:
            if ((2 * self.k) % 5 != 0):
                bin32_str = bin32_str[:-5] + bin32_str[-((2 * self.k) % 5):]
            else:
                bin32_str = bin32_str[:-5]
        # removing zero we have inserted before
        n = 2
        bin_list = [bin32_str[i:i + n] for i in range(0, len(bin32_str), n)]
        QTMID_list = []
        for e in bin_list:
            if e == "00":
                QTMID_list.extend("0")
            if e == "01":
                QTMID_list.extend("1")
            if e == "10":
                QTMID_list.extend("2")
            if e == "11":
                QTMID_list.extend("3")
        QTMID_str = ''.join([str(e) for e in QTMID_list[:]])
        return str(self.icos()) + "," + QTMID_str


def getRowCol(QTMID, K):
    I = 2 ** K
    J = 2 * I - 1
    qtmcode = QTMID.split(",")[1]
    l = list(qtmcode)
    P = 1
    n = I
    i = 1
    j = 1

    l = [int(m) for m in l]
    for ak in l:
        if ak == 1:
            if P == 1:
                i = i + n / 2
                n = n / 2
            else:
                n = n / 2
        if ak == 2 or ak == 3:
            if P == 1:
                n = n / 2
            else:
                i = i + n / 2
                n = n / 2
        if ak == 0:
            if P == 1:
                n = n / 2
                P = -P
            else:
                i = i + n / 2
                P = -P
                n = n / 2
    ai = i

    n = I
    for ak in l:
        if ak == 1:
            n = n / 2
            i = i - n
        if ak == 2:
            n = n / 2
        if ak == 3:
            j = j + n
            n = n / 2
        if ak == 0:
            n = n / 2
            j = j + 2 * (n - i) + 1
            i = n - i + 1
    return (ai, j)


def getCentreXY(i, j):
    if j % 2 != 0:
        Ox = i / float(2) + (j - 1) / float(2)
        Oy = math.sqrt(3) * i / float(2) - float(1) / math.sqrt(3)
    else:
        Ox = i / float(2) + (j - 1) / float(2)
        Oy = math.sqrt(3) * (i - 1) / float(2) + float(1) / math.sqrt(3)

    return (Ox, Oy)


def covertToLatLon(QTMID, Px, Py):
    QTMCode = QTMID.split(",")[1]
    icos = int(QTMID.split(",")[0])
    k = len(QTMCode)

    if icos <= 5:
        LAT = (math.pi / 2 - math.atan(0.5)) * Py / (2 ** (k - 1) * math.sqrt(3))
        r = LAT / (math.pi / 2 - math.atan(0.5))
        if Py != math.sqrt(3) * 2 ** (k - 1):
            LON = ((Px / 2 ** (k - 1)) - r) * math.pi / ((1 - r) * 5)
        else:
            LON = 0
        LAT = LAT + math.atan(0.5)
        LON = LON + ((icos - 1) * 2 * math.pi / 5)

    elif icos > 5 and icos <= 10:
        LAT = Py * 2 * math.atan(0.5) / (2 ** (k - 1) * math.sqrt(3))
        LAT = math.atan(0.5) - LAT
        LON = Px * 2 * math.pi / (5 * 2 ** k)
        LON = LON + ((icos - 6) * 2 * math.pi / 5)

    elif icos > 10 and icos <= 15:
        LAT = Py * 2 * math.atan(0.5) / (2 ** (k - 1) * math.sqrt(3))
        LAT = LAT + math.atan(-0.5)
        LON = Px * 2 * math.pi / (5 * 2 ** k)
        LON = LON + math.pi / 5 + ((icos - 11) * 2 * math.pi / 5)
        if LON > 2 * math.pi:
            LON = LON - 2 * math.pi
    else:
        LAT = (math.pi / 2 - math.atan(0.5)) * Py / (2 ** (k - 1) * math.sqrt(3))
        r = LAT / (math.pi / 2 - math.atan(0.5))
        if Py != math.sqrt(3) * 2 ** (k - 1):
            LON = ((Px / 2 ** (k - 1)) - r) * math.pi / ((1 - r) * 5)
        else:
            LON = 0

        LAT = -LAT + math.atan(-0.5)
        LON = LON + math.pi / 5 + ((icos - 16) * 2 * math.pi / 5)
        if LON > 2 * math.pi:
            LON = LON - 2 * math.pi

    lat = round(LAT * 180 / math.pi, 6)
    lon = round(LON * 180 / math.pi, 6)
    if lon > 180:
        lon = lon - 360
        lon = round(lon, 6)

    if (lat <= -90 or lat >= 90) and (lon <= -180 or lon > 180):
        return str(("N/A", "N/A"))
    else:
        return str((lat, lon))


def getCentreLatLon(QTM32Code, K):
    rev_qtm = IcoDecoder(QTM32Code, K)
    QTMID = rev_qtm.covertToQTMIDs()
    IJ = getRowCol(QTMID, K)
    Oxy = getCentreXY(IJ[0], IJ[1])
    latlon = covertToLatLon(QTMID, Oxy[0], Oxy[1])
    return latlon


class QUTMSDecoder:
    def __init__(self, qtmid, level):
        self.qtmid = str(qtmid)
        idlist = qtmid.split('-')
        self.code = idlist[1]  # geognomo area code
        self.zone = idlist[0]  # UTM Zone
        self.level = int(level)

    def getZoneDim(self):  # get UTM grid code (level 0!)
        zone = list(self.zone)
        getZoneDim = [0, 0, 0]
        latzones = ['C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M',
                    'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']
        if zone == ['0', '0', 'A']:
            getZoneDim = [(0, 0), 10, 180]
        elif zone == ['0', '0', 'B']:
            getZoneDim = [(0, 180), 10, 180]
        elif zone == ['0', '0', 'Y']:
            getZoneDim = [(174, 0), 6, 180]
        elif zone == ['0', '0', 'Z']:
            getZoneDim = [(174, 180), 6, 180]
        else:
            if zone == ['3', '1', 'X']:
                getZoneDim = [(72, 180), 12, 9]
            elif zone == ['3', '3', 'X']:
                getZoneDim = [(72, 189), 12, 12]
            elif zone == ['3', '5', 'X']:
                getZoneDim = [(72, 201), 12, 12]
            elif zone == ['3', '7', 'X']:
                getZoneDim = [(72, 213), 12, 9]
            elif zone == ['3', '1', 'V']:
                getZoneDim = [(56, 180), 8, 3]
            elif zone == ['3', '2', 'V']:
                getZoneDim = [(56, 183), 8, 9]
            else:
                lonzone = [zone[0], zone[1]]
                lonzone = ''.join(map(str, lonzone))  # joins the longitude code digits
                for index, item in enumerate(latzones):
                    if item == zone[2]:
                        left = (((index + 1) * 8 + 2), (int(lonzone) * 6 - 6))  # get the leftcorner point
                        getZoneDim = [left, 8, 6]
        return getZoneDim

    def covertToQTMIDs(self):
        if "," in self.code:
            QTM32ID_list = self.code.split(',')
            # print data
            t = ''
            bin32_list = []
            for i in QTM32ID_list[0:]:
                for d in base32Data:
                    if i == d['Word']:
                        t = d['Binary Code']
                bin32_list.append(t)
        else:
            QTM32ID_alphalist = list(self.code)
            t = ''
            bin32_list = []
            for i in QTM32ID_alphalist[0:]:
                for d in base32Data:
                    if i == d['Code']:
                        t = d['Binary Code']
                bin32_list.append(t)
        bin32_str = ''.join([str(e) for e in bin32_list])
        if len(bin32_str) != self.level * 2:
            if ((2 * self.level) % 5 != 0):
                bin32_str = bin32_str[:-5] + bin32_str[-((2 * self.level) % 5):]
            else:
                bin32_str = bin32_str[:-5]
        # removing zero we have inserted before
        n = 2
        bin_list = [bin32_str[i:i + n] for i in range(0, len(bin32_str), n)]

        QTMID_list = []
        for e in bin_list:
            if e == "00":
                QTMID_list.extend("0")
            if e == "01":
                QTMID_list.extend("1")
            if e == "10":
                QTMID_list.extend("2")
            if e == "11":
                QTMID_list.extend("3")
        QTMID_str = ''.join([str(e) for e in QTMID_list[:]])

        return str(QTMID_str)

    def getABCD(self):
        qtmcode = str(self.covertToQTMIDs())
        leftpoint = [0, 0]  # ADDED
        getZoneDim = self.getZoneDim()
        leftpoint[0] = getZoneDim[0][0] - 90
        leftpoint[1] = getZoneDim[0][1] - 180
        # size of rectangle of level 0 grid
        latdim = getZoneDim[1]
        londim = getZoneDim[2]
        l = list(qtmcode)

        k = len(l)
        for i in range(0, k):
            latdim /= 2
            londim /= 2
            if l[i] == "0":
                leftpoint[0] += latdim
            elif l[i] == "1":
                leftpoint[0] += latdim
                leftpoint[1] += londim
            elif l[i] == "3":
                leftpoint[1] += londim

        # clockwise from bottom-left
        LatLonA = (leftpoint[0], leftpoint[1])
        LatLonB = (leftpoint[0] + latdim, leftpoint[1])
        LatLonC = (leftpoint[0] + latdim, leftpoint[1] + londim)
        LatLonD = (leftpoint[0], leftpoint[1] + londim)

        return (LatLonA, LatLonB, LatLonC, LatLonD)

    def getCenter(self):
        vertexA = self.getABCD()[0]
        vertexB = self.getABCD()[1]
        vertexC = self.getABCD()[2]
        centerLatitude = (vertexA[0] + vertexB[0]) / 2
        centerLongitude = (vertexB[1] + vertexC[1]) / 2
        return (centerLatitude, centerLongitude)

    def getArea(self):
        ABCD = self.getABCD()
        latitudeA = ABCD[0][0] * math.pi / 180.0
        longitudeA = ABCD[0][1] * math.pi / 180.0
        latitudeB = ABCD[1][0] * math.pi / 180.0
        longitudeC = ABCD[2][1] * math.pi / 180.0
        equatorialEarthRadius = float(6378.1)
        area = (abs(math.sin(latitudeB) - math.sin(latitudeA))) * (abs(longitudeC - longitudeA))\
               * equatorialEarthRadius ** 2
        return (area)


