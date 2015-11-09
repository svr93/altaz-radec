# astropy-1.0.6

from astropy import units as u
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.time import Time
import numpy as np

stationLat=44.93*u.deg # dec
stationLng=40.98*u.deg # ra
# TODO: change height value
stationCoords = EarthLocation(lat=stationLat, lon=stationLng, height=0*u.km)
print 'Station (Armavir) coordinates: ' + str(stationCoords)

# TODO: use timezone shift
time = Time('2015-11-09T00:00:00.000Z')

altAzDistance=1250*u.km

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

targetCoordsICRS = targetCoords.transform_to('icrs')
# ---> correct (?) result
print 'Target coordinates in ICRS system: ' + str(targetCoordsICRS)

targetLat=targetCoordsICRS.data.lat # dec
targetLng=targetCoordsICRS.data.lon # ra

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
