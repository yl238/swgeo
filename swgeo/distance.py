import numpy as np
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    Parameters
    ----------
    lon1: longitude of the first point
    lat1: latitude of the first point
    lon2: longitude of the second point
    lat2: latitude of the second point

    Returns
    -------
    float or numpy array, great circle distance between (lon1, lat1) and (lon2, lat2)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371000  # Radius of earth in meters. Use 3956 for miles
    return c * r
