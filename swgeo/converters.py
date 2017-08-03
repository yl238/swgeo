import numpy as np


def geo_to_cart(lon, lat, alt):
    """
    Converts geographical coordinates (lon, lat, alt) on WGS84 ellipsoid
    to Cartesian coordinates (x, y, z).

    Parameters
    ----------
    Geocentric coordinates
    lat: latitude of the position
    lon: longitude of position
    alt: height of position

    Returns
    -------
    tuple of floats or numpy arrays, cartesian coordinates

    """
    rlat, rlon = map(np.radians, [lat, lon])

    a = 6378137  # major axis
    f = 1. / 298.257223563  # flattening of the earth
    b = a * (1 - f)  # minor axis

    e2 = 1 - (b / a) ** 2  # square of the first numerical eccentricity of ellipsoid

    N = a / np.sqrt(1 - e2 * np.sin(rlat) ** 2)

    x = (N + alt) * np.cos(rlat) * np.cos(rlon)
    y = (N + alt) * np.cos(rlat) * np.sin(rlon)
    z = ((b / a) ** 2 * N + alt) * np.sin(rlat)

    return x, y, z


def cart_to_geo(x, y, z):
    """Converts from Cartesian coordinates (x, y, z) to geographical coordinates
    (lat, lon, h) on a WGS84 ellipsoid.

    Parameters
    ----------
    x: float or numpy array, x-coordinate
    y: float or numpy array, y-coordinate
    z: float or numpy array, z-coordinate

    Returns
    -------
    tuple of floats or numpy arrays, geographical coordinates

    """
    if x == 0 or y == 0 or z == 0:
        return "Cartesian coordinates cannot be zero"
    a = 6378137  # major axis
    f = 1. / 298.257223563  # flattening of the earth

    rlon = np.arctan2(y, x)
    e2 = (2 - f) * f / ((1 - f) ** 2)
    c = a * np.sqrt(1 + e2)
    rlat = np.arctan(z / (np.sqrt(x ** 2 + y ** 2) * (1 - (2 - f)) * f))

    h = 0.1
    oldh = 0
    index = 1
    while abs(h - oldh) > 1.e-12 and index < 15:
        oldh = h
        N = c / np.sqrt(1 + e2 * np.cos(rlat) ** 2)
        rlat = np.arctan(z / ((np.sqrt(x ** 2 + y ** 2)) * (1 - (2 - f) * f * N / (N + h))))
        h = np.sqrt(x ** 2 + y ** 2) / np.cos(rlat) - N
        index += 1

    lat, lon = map(np.degrees, [rlat, rlon])
    return lon, lat, h
