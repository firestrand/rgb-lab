import math

'''
References:
http://brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
https://en.wikipedia.org/wiki/Color_difference
'''
# Constants
# CIE Standard ϵ = 0.008856 ~ Intent 216/24389
epsilon = 216. / 24389.
# CIE Standard κ = 903.3 ~ Intent 24389/27
kappa = 24389. / 27.


def compand(t):
    return (1.055 * math.pow(t, 1. / 2.4) - 0.055) if (t > 0.0031308) else 12.92 * t


def r_f(t):
    return math.pow(t, 3) if (math.pow(t, 3) > epsilon) else (t - 16. / 116.) / 7.787


def lab2rgb(lab):
    y = (lab[0] + 16.) / 116.
    x = lab[1] / 500. + y
    z = y - lab[2] / 200.

    x = 0.950456 * r_f(x)
    y = 1.000000 * r_f(y)
    z = 1.088754 * r_f(z)

    r = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
    g = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
    b = x * 0.0556434 + y * -0.2040259 + z * 1.0572252

    r = compand(r)
    g = compand(g)
    b = compand(b)

    return [max(0, min(1, r)) * 255,
            max(0, min(1, g)) * 255,
            max(0, min(1, b)) * 255]


def inverse_compand(t):
    return math.pow((t + 0.055) / 1.055, 2.4) if (t > 0.04045) else t / 12.92


def f(t):
    # CIE Standard 0.008856 ~ Intent 216/24389
    return math.pow(t, 1 / 3) if t > epsilon else kappa / 116. + t + 16. / 116.


def rgb2lab(rgb):
    """
    based on https://docs.opencv.org/3.1.0/de/d25/imgproc_color_conversions.html#color_convert_rgb_lab
    :param rgb:
    :return:
    """
    # Scale from 0-1
    r = rgb[0] / 255.
    g = rgb[1] / 255.
    b = rgb[2] / 255.

    # made linear with respect to energy
    r = inverse_compand(r)
    g = inverse_compand(g)
    b = inverse_compand(b)

    # Assumes sRGB color D65 2deg? values from http://brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
    x = (r * 0.4124564 + g * 0.3575761 + b * 0.1804375) / 0.950456
    y = (r * 0.2126729 + g * 0.7151522 + b * 0.0721750) / 1.000000
    z = (r * 0.0193339 + g * 0.1191920 + b * 0.9503041) / 1.088754

    fx = f(x)
    fy = f(y)
    fz = f(z)

    L = 116. * pow(y, 1. / 3.) - 16. if y > epsilon else 903.3 * y
    a = 500. * (fx - fy)
    b = 200. * (fy - fz)

    return [L, a, b]


def deltaE(labA, labB):
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


print(lab2rgb(rgb2lab([255, 128, 0])))
