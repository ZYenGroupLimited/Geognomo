import math
import base32_data


BASE32DATA = base32_data.getBase32Data()

class QrsDecode:
    def __init__(self, id, k):
        self.id = str(id)
        self.k = int(k)

    def rec(self):
        if "," in self.id:
            QTM32ID_list = self.id.split(',')
            for d in BASE32DATA:
                if d['Word'] == QTM32ID_list[0]:
                    rec = d['Decimal']
        else:
            QTM32ID_alphalist = list(self.id)
            for d in BASE32DATA:
                if d['Code'] == QTM32ID_alphalist[0]:
                    rec = d['Decimal']
        rec = int(rec)
        return rec

    def covertToQTMIDs(self):
        if "," in self.id:
            QTM32ID_list = self.id.split(',')
            t = '';
            bin32_list = []
            for i in QTM32ID_list[1:]:
                for d in BASE32DATA:
                    if i == d['Word']:
                        t = d['Binary Code']
                        #print (t)
                bin32_list.append(t)
        else:
            QTM32ID_alphalist = list(self.id)
            t = '';
            bin32_list = []
            for i in QTM32ID_alphalist[1:]:
                for d in BASE32DATA:
                    if i == d['Code']:
                        t = d['Binary Code']
                bin32_list.append(t)

        #print ("bin32_list" + str(bin32_list))
        bin32_str = ''.join([str(e) for e in bin32_list])
        if len(bin32_str) != self.k * 2:
            if ((2 * self.k) % 5 != 0):
                bin32_str = bin32_str[:-5] + bin32_str[-((2 * self.k) % 5):]
            else:
                bin32_str = bin32_str[:-5]
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
        return str(self.rec()) + "," + QTMID_str

    def getABCD(self):
        QTMID = str(self.covertToQTMIDs())

        qtmcode = QTMID.split(",")[1]
        rec = int(QTMID.split(",")[0])
        l = list(qtmcode)

        leftpoint = [0, 0]
        if rec < 7:
            leftpoint = [30, (rec - 1) * 60]
        elif rec > 6 and rec < 13:
            leftpoint = [-30, (rec - 1) * 60]
        elif rec > 12:
            leftpoint = [-90, (rec - 1) * 60]

        if leftpoint[1] > 180:  # possible reason why QRS not working for part of the map???
            leftpoint[1] -= 360

        k = len(l)
        dim = float(60)
        for i in range(0, k):
            dim /= 2
            if l[i] == "0":
                leftpoint[0] += dim
            elif l[i] == "1":
                leftpoint[0] += dim
                leftpoint[1] += dim
            elif l[i] == "3":
                leftpoint[1] += dim

        # clockwise from bottom-left
        LatLonA = (leftpoint[0], leftpoint[1])
        LatLonB = (leftpoint[0] + dim, leftpoint[1])
        LatLonC = (leftpoint[0] + dim, leftpoint[1] + dim)
        LatLonD = (leftpoint[0], leftpoint[1] + dim)

        return (LatLonA, LatLonB, LatLonC, LatLonD)

    def getCenter(self):
        A = self.getABCD()[0]  #####changes made here
        B = self.getABCD()[1]
        C = self.getABCD()[2]

        CenterLat = (A[0] + B[0]) / 2
        CenterLon = (B[1] + C[1]) / 2

        return (CenterLat, CenterLon)

    def getArea(self):
        ABCD = self.getABCD()
        latA = ABCD[0][0] * math.pi / 180.0
        lonA = ABCD[0][1] * math.pi / 180.0
        latB = ABCD[1][0] * math.pi / 180.0
        lonC = ABCD[2][1] * math.pi / 180.0
        R = float(6378.1)
        area = (abs(math.sin(latB) - math.sin(latA))) * (abs(lonC - lonA)) * R ** 2
        return (area)