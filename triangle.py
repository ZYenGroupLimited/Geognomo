import math
import geocode_encoder as encoder
import geocode_decoder as decoder


def toRadians(degree):
    return degree * math.pi / 180.0


def getDistance(latitude1, longitude1, latitude2, longitude2):
    RadiusOfEarth = 6378
    # Haversine formula: https://en.wikipedia.org/wiki/Haversine_formula
    differenceOfLatitudes = toRadians(latitude1) - toRadians(latitude2)
    differenceOfLongitudes = toRadians(longitude1) - toRadians(longitude2)
    s = (math.pow(math.sin(differenceOfLatitudes / 2), 2) + math.cos(toRadians(latitude1))
         * math.cos(toRadians(latitude2)) * math.pow(math.sin(differenceOfLongitudes / 2), 2))
    distanceBetween2Points = 2 * RadiusOfEarth * math.asin(math.sqrt(s))
    return distanceBetween2Points


def getArea(QTMID, i, j):  # Heron's Formula for the area of a triangle: https://www.mathopenref.com/heronsformula.html
    vertices = encoder.getABC(i, j)
    verticesLatitudeLongitudeMatrix = []
    for pointxy in vertices:
        pointsLatitudeLongitude = decoder.covertToLatLon(QTMID, pointxy[0], pointxy[1])
        pointsLatitudeLongitude = pointsLatitudeLongitude.replace('(', '').replace(')', '').replace(' ', '').split(",")
        pointsLatitudeLongitude = [float(i) for i in pointsLatitudeLongitude]
        verticesLatitudeLongitudeMatrix.append(pointsLatitudeLongitude)
    distanceAB = getDistance(verticesLatitudeLongitudeMatrix[0][0], verticesLatitudeLongitudeMatrix[0][1],
                             verticesLatitudeLongitudeMatrix[1][0], verticesLatitudeLongitudeMatrix[1][1])
    distanceBC = getDistance(verticesLatitudeLongitudeMatrix[1][0], verticesLatitudeLongitudeMatrix[1][1],
                             verticesLatitudeLongitudeMatrix[2][0], verticesLatitudeLongitudeMatrix[2][1])
    distanceCA = getDistance(verticesLatitudeLongitudeMatrix[2][0], verticesLatitudeLongitudeMatrix[2][1],
                             verticesLatitudeLongitudeMatrix[0][0], verticesLatitudeLongitudeMatrix[0][1])
    halfOfPerimeter = (distanceAB + distanceBC + distanceCA) / 2
    areaOfTriangle = math.sqrt(halfOfPerimeter * (halfOfPerimeter - distanceAB) * (halfOfPerimeter - distanceBC)
                               * (halfOfPerimeter - distanceCA))
    return areaOfTriangle
