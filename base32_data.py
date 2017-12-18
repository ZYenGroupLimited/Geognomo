import os
import json


def getBase32Data():
    full_path = os.path.realpath(__file__)
    file_path = '%s/base32.json' % os.path.dirname(full_path)
    f = open(file_path)
    data = json.load(f)
    return data
