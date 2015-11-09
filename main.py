# astropy-1.0.6

from astropy import units as u
from astropy.coordinates import EarthLocation
from astropy.time import Time

# TODO: change height value
stationCoords = EarthLocation(lat=44.93*u.deg, lon=40.98*u.deg, height=0*u.km)
print 'Station (Armavir) coordinates: ' + str(stationCoords)

# TODO: use timezone shift
time = Time('2015-11-09T00:00:00.000Z')
