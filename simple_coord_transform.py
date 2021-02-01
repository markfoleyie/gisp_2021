import utilities.gdal_workaround
import pyproj

lat = 53.5
lon = -8.0

easting = 200000
northing = 250000

# This makes an object that can transform one CRS 94326 in this case) to another (29903 in this case). We also make sure
# that it's always xy, i.e. lon, lat never lat, lon
transformer = pyproj.Transformer.from_crs(4326, 29903, always_xy=True)

# Apply the ntransformation
x, y = transformer.transform(lon, lat)
print(f"Turned Lat: {lat}, Lon: {lon} into IG Easting: {x}, Northing: {y}")

# Do the same, except in the opposite direction, i.e 29903 -> 4326
transformer = pyproj.Transformer.from_crs(29903, 4326, always_xy=True)
x, y = transformer.transform(easting, northing)
print(f"Turned IG Easting: {easting}, Northing: {northing} into Lon: {x}, Lat: {y}")
