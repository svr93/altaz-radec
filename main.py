# astropy-1.0.6

from astropy import units as u
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.time import Time
import numpy as np

stationLatDeg=44.93*u.deg # dec
stationLngDeg=40.98*u.deg # ra
# TODO: change height value
stationCoords = EarthLocation(lat=stationLatDeg, lon=stationLngDeg, height=0*u.km)
print 'Station (Armavir) coordinates: ' + str(stationCoords)

# TODO: use timezone shift
time = Time('2015-11-09T00:00:00.000Z')

altAzDistance=1250 # km

# TODO: check Armavir station viewing angles/distances
# TODO: check distance param (alt: 45 deg; 1250 / Math.sqrt(2) = 884)
targetCoords = SkyCoord(
    az=45*u.deg,
    alt=45*u.deg,
    # distance=1250*u.km,
    location=stationCoords,
    obstime=time,
    frame='altaz'
)

targetCoordsITRS = targetCoords.transform_to('itrs')
# ---> incorrect result for near-Earth objects (need distance)
print 'Target coordinates in ITRS system: ' + str(targetCoordsITRS)

targetLat=targetCoordsITRS.spherical.lat.to('rad') # dec, rad
targetLng=targetCoordsITRS.spherical.lon.to('rad') # ra, rad

stationLat=stationLatDeg.to('rad') # dec, rad
stationLng=stationLngDeg.to('rad') # ra, rad

print str(targetLat) + '~' + str(targetLng)
print str(stationLat) + '~' + str(stationLng)

# http://spiff.rit.edu/classes/phys373/lectures/radec/radec.html
# cos(y) = sin(dec1)sin(dec2) + cos(dec1)cos(dec2)cos(ra1 - ra2)

angularDistCos=np.sin(stationLat) * np.sin(targetLat) + \
    np.cos(stationLat) * np.cos(targetLat) * np.cos(stationLng - targetLng)   

angularDist = np.arccos(angularDistCos)
print 'Angular distance between station and target: ' + str(angularDist)

# cos theorem: altAzDistance * altAzDistance =
# earthRadiusDyn * earthRadiusDyn + c * c - 2 * earthRadiusDyn * c * angularDistCos

# c * c - 2 * earthRadiusDyn * angularDistCos * c -
# altAzDistance * altAzDistance + earthRadiusDyn * earthRadiusDyn = 0

earthRadiusDyn = 6371 # km, temporarily

C = - altAzDistance * altAzDistance + earthRadiusDyn * earthRadiusDyn
B = - 2 * earthRadiusDyn * angularDistCos
A = 1

print B * B - 4 * A * C

# x1 = (-B - SQRT(B * B - 4 * A * C)) / (2 * A)
# x2 = (-B + SQRT(B * B - 4 * A * C)) / (2 * A)
