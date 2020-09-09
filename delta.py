import math


def deltaE_CIE1976(labA, labB):
    """
    CIE76 def of deltaE
    :param labA:
    :param labB:
    :return:
    """
    deltaL = labA[0] - labB[0]
    deltaA = labA[1] - labB[1]
    deltaB = labA[2] - labB[2]
    i = math.pow(deltaL, 2) + math.pow(deltaA, 2) + math.pow(deltaB, 2)
    return math.sqrt(i)


def deltaE_CIE1994(labA, labB):
    """
    Based on CIE94 def of deltaE
    https://en.wikipedia.org/wiki/Color_difference
    :param labA:
    :param labB:
    :return:
    """
    deltaL = labA[0] - labB[0]
    c1 = math.sqrt(labA[1] * labA[1] + labA[2] * labA[2])
    c2 = math.sqrt(labB[1] * labB[1] + labB[2] * labB[2])
    deltaC = c1 - c2
    deltaA = labA[1] - labB[1]
    deltaB = labA[2] - labB[2]
    deltaH = math.pow(deltaA, 2) + math.pow(deltaB, 2) - math.pow(deltaC, 2)
    deltaH = 0 if deltaH < 0 else math.sqrt(deltaH)
    # Sc = 1 + K1 * C1 where K1 for graphic arts = 0.045
    sc = 1.0 + 0.045 * c1
    # Sh = 1 + K2 * C1 where K2 for graphic arts = 0.015
    sh = 1.0 + 0.015 * c1
    # deltaL / (kL * SL) where kL and SL for graphic arts is 1 => equal to deltaL
    i = math.pow(deltaL, 2) + math.pow(deltaC / sc, 2) + math.pow(deltaH / sh, 2)
    return math.sqrt(i)


def deltaE_CIE2000(labA, labB):
    """
    CIE2000 def of deltaE
    :param labA:
    :param labB:
    :return:
    """
    L1 = labA[0]
    L2 = labB[0]
    a1 = labA[1]
    a2 = labB[1]
    b1 = labA[2]
    b2 = labB[2]
    deltaL = L2 - L1
    C1 = math.sqrt(a1 ** 2 + b1 ** 2)
    C2 = math.sqrt(a2 ** 2 + b2 ** 2)
    CAvg = (C1 + C2) / 2.
    G = 0.50 * (1. - math.sqrt(CAvg ** 7 / (CAvg ** 7 + 25. ** 7)))
    a1_p = a1 * (1. + G)
    a2_p = a2 * (1. + G)
    C1_p = math.sqrt(a1_p ** 2 + b1 ** 2)
    C2_p = math.sqrt(a2_p ** 2 + b2 ** 2)
    CAvg_p = (C1_p + C2_p) / 2.
    atan_a1_p = math.degrees(math.atan(b1 / a1_p))
    atan_a2_p = math.degrees(math.atan(b2 / a2_p))
    h1_p = atan_a1_p + 360 if atan_a1_p < 0 else atan_a1_p
    h2_p = atan_a2_p + 360 if atan_a2_p < 0 else atan_a2_p
    HAvg_p = (h1_p + h2_p + 360.) / 2. if abs(h1_p - h2_p) > 180. else (h1_p + h2_p) / 2.

    #TODO: Complete implementation
    #deltaC = c1 - c2
    #deltaA = labA[1] - labB[1]
    #deltaB = labA[2] - labB[2]
    #deltaH = math.pow(deltaA, 2) + math.pow(deltaB, 2) - math.pow(deltaC, 2)
    #deltaH = 0 if deltaH < 0 else math.sqrt(deltaH)
    # Sc = 1 + K1 * C1 where K1 for graphic arts = 0.045
    #sc = 1.0 + 0.045 * c1
    # Sh = 1 + K2 * C1 where K2 for graphic arts = 0.015
    #sh = 1.0 + 0.015 * c1
    # deltaL / (kL * SL) where kL and SL for graphic arts is 1 => equal to deltaL
    #i = math.pow(deltaL, 2) + math.pow(deltaC / sc, 2) + math.pow(deltaH / sh, 2)
    #return math.sqrt(i)
