import math


def VrsCode(latitude1, longitude1, latitude2, longitude2):
    # no class for VRS encoder...only reproduce VRS code for given pair of lat,lon
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
                'M', 'N', 'P', 'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y',
                '0', '1', '2', '3', '4', '5', '6', '7', '8','9']
    # not using JSON file since the base32 alphabets are different
    latitude1 = float(latitude1) + 90
    longitude1 = float(longitude1) + 180
    latitude2 = float(latitude2) + 90
    longitude2 = float(longitude2) + 180
    latitude = min(latitude1, latitude2) / 1000
    longitude = min(longitude1, longitude2) / 1000
    differenceOfLatitude = abs(latitude1 - latitude2) / 1000
    differenceOfLongitude = abs(longitude1 - longitude2) / 1000
    latitudeVector = [0] * 9
    longitudeVector = [0] * 9
    differenceOfLatitudeVector = [0] * 9
    differenceOfLongitudeVector = [0] * 9

    for i in range(9):
        latitudeVector[i] = math.floor(latitude * 10)
        latitude = latitude * 10 - math.floor(latitude * 10)
        longitudeVector[i] = math.floor(longitude * 10)
        longitude = longitude * 10 - math.floor(longitude * 10)
        differenceOfLatitudeVector[i] = math.floor(differenceOfLatitude * 10)
        differenceOfLatitude = differenceOfLatitude * 10 - math.floor(differenceOfLatitude * 10)
        differenceOfLongitudeVector[i] = math.floor(differenceOfLongitude * 10)
        differenceOfLongitude = differenceOfLongitude * 10 - math.floor(differenceOfLongitude * 10)

    k = 0
    j = 1
    while k < 1:
        if differenceOfLatitudeVector[j - 1] != 0:
            k = j
        if differenceOfLongitudeVector[j - 1] != 0:
            k = j
        j += 1
    code = [0] * (2 * k + 6)
    if k > 1:
        for i in range(k - 1):
            code[2 * i] = latitudeVector[i]
            code[2 * i + 1] = longitudeVector[i]
    code[2 * k - 2] = latitudeVector[k - 1]
    code[2 * k - 1] = differenceOfLatitudeVector[k - 1]
    code[2 * k] = longitudeVector[k - 1]
    code[2 * k + 1] = differenceOfLongitudeVector[k - 1]
    code[2 * k + 2] = latitudeVector[k]
    code[2 * k + 3] = differenceOfLatitudeVector[k]
    code[2 * k + 4] = longitudeVector[k]
    code[2 * k + 5] = differenceOfLongitudeVector[k]

    number = 0
    maxsum = 1
    if k > 1:
        for i in range(2 * k + 4):
            number = number + (code[2 * (k - 1) + 7 - i]) * (10 ** (i))
            maxsum = maxsum * 10
        number = number + code[1] * maxsum
        maxsum = 4 * maxsum
        number = number + code[0] * maxsum
        maxsum = 2 * maxsum
    if k < 2:
        for i in range(4):
            number = number + code[9 - i - 2] * (10 ** i)
            maxsum = maxsum * 10
        for i in range(2):
            number = number + code[5 - i - 2] * maxsum
            maxsum = maxsum * 4
        for i in range(2):
            number = number + code[3 - i - 2] * maxsum
            maxsum = maxsum * 2
    length = int(math.ceil(math.log(number, 32)))
    code32 = [0] * length
    for i in range(length):
        r = (number % 32) + 1
        code32[length - i - 1] = alphabet[int(r - 1)]
        number = ((number - (number % 32)) // 32)  # // to get int back (else produces float type)
    code32 = ''.join(map(str, code32))
    return code32
