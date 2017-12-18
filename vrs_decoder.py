import math
from decimal import Decimal


def VrsDecode(qtm32code):
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
                'M', 'N', 'P', 'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y',
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    code32 = list(qtm32code)
    number = 0
    length = len(code32)
    for i in range(length):
        base32Index = alphabet.index(code32[i])
        number = number + base32Index * 32 ** (length - i - 1)
    code = []
    if number < 640001:
        maxsum = 320000
        code.insert(1, ((number - number % maxsum) / maxsum))
        number = number % maxsum
        maxsum = maxsum / 2
        code.insert(2, ((number - number % maxsum) / maxsum))
        number = number % maxsum
        maxsum = maxsum / 4
        code.insert(3, ((number - number % maxsum) / maxsum))
        number = number % maxsum
        maxsum = maxsum / 4
        for i in range(5):
            code.insert(i + 4, ((number - number % maxsum) / maxsum))
            # +4 since .insert appends element at i'th position
            number = number % maxsum
            maxsum = maxsum / 10
    if number > 640000:
        k = math.floor(math.log(number, 10) - math.log(8, 10)) + 1
        k = int(k)
        maxsum = 4 * 10 ** k
        code.insert(1, (number - number % maxsum) / maxsum)
        number = number % maxsum
        maxsum = int(maxsum / 4)
        for i in range(k + 1):
            code.insert(i + 1, ((number - number % int(maxsum)) / int(maxsum)))
            number = int(number % int(maxsum))
            maxsum = (maxsum / 10)
    if (len(code) == 8):
        latitude1 = Decimal((100 * code[0])) + Decimal((10 * code[4]))
        longitude1 = Decimal((100 * code[2])) + Decimal((10 * code[6]))
        latitude2 = latitude1 + Decimal((100 * code[1])) + Decimal((10 * code[5]))
        longitude2 = longitude1 + Decimal((100 * code[3])) + Decimal((10 * code[7]))
    if (len(code) > 8):
        latitude1 = 0
        longitude1 = 0
        k = int((len(code) - 8) / 2)
        for i in range(k):
            latitude1 = latitude1 + (Decimal((code[2 * i] * 100))) / Decimal((10 ** (i)))
            # imp. use Decimal module else python uses floating point arithmetic, giving 'incorrect' results
            longitude1 = longitude1 + (Decimal((code[2 * i + 1] * 100)) / Decimal((10 ** (i))))
        for i in range(2):
            latitude1 = latitude1 + Decimal((code[2 * k + 4 * (i + 1) - 4] * 100)) / Decimal((10 ** (k + i)))
            longitude1 = longitude1 + Decimal((code[2 * k + 4 * (i + 1) - 2] * 100)) / Decimal((10 ** (k + i)))
        latitude2 = latitude1
        longitude2 = longitude1
        for i in range(2):
            latitude2 = latitude2 + Decimal((code[2 * k + 4 * (i + 1) - 3] * 100)) / Decimal(10 ** (k + i))
            longitude2 = longitude2 + Decimal((code[2 * k + 4 * (i + 1) - 1] * 100)) / Decimal(10 ** (k + i))
    pointA = (float(latitude1 - 90), float(longitude1 - 180))
    pointB = (float(latitude2 - 90), float(longitude2 - 180))
    return (pointA, pointB)


def VrsArea(pointA, pointB):
    latitudeA = pointA[0] * math.pi / 180.0
    longitudeA = pointA[1] * math.pi / 180.0
    latitudeB = pointB[0] * math.pi / 180.0
    longitudeB = pointB[1] * math.pi / 180.0
    equatorialEarthRadius = float(6378.1)
    area = abs((math.sin(latitudeB) - math.sin(latitudeA))) * abs((longitudeB - longitudeA)) \
           * equatorialEarthRadius ** 2
    return (area)
