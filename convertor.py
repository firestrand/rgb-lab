import math

'''
Reference:
http://brucelindbloom.com

Whites
Illuminant	X	Y	Z
A	1.09850	1.00000	0.35585
B	0.99072	1.00000	0.85223
C	0.98074	1.00000	1.18232
D50	0.96422	1.00000	0.82521
D55	0.95682	1.00000	0.92149
D65	0.95047	1.00000	1.08883
D75	0.94972	1.00000	1.22638
E	1.00000	1.00000	1.00000
F2	0.99186	1.00000	0.67393
F7	0.95041	1.00000	1.08747
F11	1.00962	1.00000	0.64350
'''

# Constants
# CIE Standard ϵ = 0.008856 ~ Intent 216/24389
epsilon = 216. / 24389.
# CIE Standard κ = 903.3 ~ Intent 24389/27
kappa = 24389. / 27.
# sRGB white D65 2deg - Data Source OpenCV?
white = [0.950456, 1.000000, 1.088754]


def inverse_compand(t):
    return math.pow((t + 0.055) / 1.055, 2.4) if (t > 0.04045) else t / 12.92


def rgb2xyz(rgb):
    # Scale from 0-1
    r = rgb[0] / 255.
    g = rgb[1] / 255.
    b = rgb[2] / 255.

    # made linear with respect to energy sRGB
    r = inverse_compand(r)
    g = inverse_compand(g)
    b = inverse_compand(b)

    # Assumes sRGB color D65 2deg? values from http://brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
    x = (r * 0.4124564 + g * 0.3575761 + b * 0.1804375)
    y = (r * 0.2126729 + g * 0.7151522 + b * 0.0721750)
    z = (r * 0.0193339 + g * 0.1191920 + b * 0.9503041)

    return [x, y, z]


def xyzf(t):
    return math.pow(t, 1 / 3) if t > epsilon else (kappa * t + 16.) / 116.


def xyz2lab(xyz):
    x = xyz[0] / white[0]
    y = xyz[1] / white[1]
    z = xyz[2] / white[2]
    fx = xyzf(x)
    fy = xyzf(y)
    fz = xyzf(z)
    L = 116. * fy - 16.
    a = 500. * (fx - fy)
    b = 200. * (fy - fz)
    return [L, a, b]


def lab2xyz(lab):
    L = lab[0]
    a = lab[1]
    b = lab[2]

    fy = (L + 16.) / 116.
    fx = (a / 500.) + fy
    fz = fy - (b / 200.)

    fx3 = math.pow(fx, 3)
    fz3 = math.pow(fz, 3)

    x = fx3 if fx3 > epsilon else (116. * fx - 16.) / kappa
    y = math.pow(fy, 3) if L > kappa * epsilon else L / kappa
    z = fz3 if fz3 > epsilon else (116. * fz - 16.) / kappa

    return [x * white[0], y * white[1], z * white[2]]


def compand(t):
    return (1.055 * math.pow(t, 1. / 2.4) - 0.055) if (t > 0.0031308) else 12.92 * t


def xyz2rgb(xyz):
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]

    # Assumes sRGB color D65 2deg? values from http://brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
    r = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
    g = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
    b = x * 0.0556434 + y * -0.2040259 + z * 1.0572252

    r = compand(r)
    g = compand(g)
    b = compand(b)

    return [max(0, min(1, r)) * 255,
            max(0, min(1, g)) * 255,
            max(0, min(1, b)) * 255]
