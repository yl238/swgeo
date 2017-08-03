import numpy as np
import matplotlib.pyplot as plt
import folium


class GeoIndex(object):
    def __init__(self, geoindex=None, latitude=None, longitude=None, decimal=None):
        self.geo_index = geoindex
        self.latitude = latitude
        self.longitude = longitude
        self.decimal = decimal

    def __repr__(self):
        return "({}, {}, {}, {})".format(self.geo_index,
                                         self.latitude,
                                         self.longitude,
                                         self.decimal)

    @classmethod
    def from_latlon(cls, latitude, longitude, decimal=4):
        """Create a GeoIndex object from a point by specifying the longitude and latitude values
        and the number of decimal places desired (default = 4)
        """
        if np.abs(latitude) > 90:
            raise ValueError("Invalid input: latitude must lie between -90 and 90.")
        if np.abs(longitude) > 180:
            raise ValueError("Invalid input: longitude must lie between -180 and 180.")
        exponent = decimal + 3
        lat = str(int((latitude + 90) * 10 ** decimal)).zfill(exponent)
        lon = str(int((longitude + 180) * 10 ** decimal)).zfill(exponent)
        geoindex = lat + lon
        return cls(geoindex, latitude, longitude, decimal)

    @classmethod
    def from_string(cls, geoindex):
        """Create a GeoIndex object from its string representation"""
        exponent = len(geoindex) // 2
        decimal = exponent - 3
        lat = float(geoindex[:exponent]) / 10 ** decimal - 90.
        lon = float(geoindex[exponent:]) / 10 ** decimal - 180.
        if exponent * 2 != len(geoindex):
            raise ValueError("Invalid GeoIndex: Geoindex must contain an even number of digits.")
        if np.abs(lat) > 90:
            raise ValueError("Invalid GeoIndex: latitude must lie between -90 and 90.")
        if np.abs(lon) > 180:
            raise ValueError("Invalid GeoIndex: longitude must lie between -180 and 180.")
        return cls(geoindex, lat, lon, decimal)

    def get_geoindex(self):
        return self.geo_index

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_coords(self):
        return self.latitude, self.longitude

    def get_decimal(self):
        return self.decimal

    def plot_folium(self, map, **kwargs):
        d = 10 ** -self.decimal / 2
        lats = [self.latitude - d, self.latitude + d, self.latitude + d, self.latitude - d, self.latitude - d]
        lons = [self.longitude- d, self.longitude - d, self.longitude + d, self.longitude + d, self.longitude - d]
        coords = zip(lats, lons)
        geoindex_box = folium.PolyLine(locations=coords, **kwargs)
        map.add_child(geoindex_box)

    def plot(self, **kwargs):
        d = 10 ** -self.decimal / 2
        lats = [self.latitude - d, self.latitude + d, self.latitude + d, self.latitude - d, self.latitude - d]
        lons = [self.longitude - d, self.longitude - d, self.longitude + d, self.longitude + d, self.longitude - d]
        plt.plot(lons, lats, **kwargs)

    def get_neighbours(self, m=3, n=3):
        """Get the list of geo_indices neighbouring the specified geoindex"""
        neighbour_geo_indices = []
        for ilat in range(-n, n+1):
            for ilon in range(-m, m+1):
                new_latitude = self.latitude + ilat * 10 **-self.decimal
                new_longitude = self.longitude + ilon * 10 ** -self.decimal
                new_geoindex = self.from_latlon(new_latitude, new_longitude, self.decimal)
                neighbour_geo_indices.append(new_geoindex)
        return neighbour_geo_indices