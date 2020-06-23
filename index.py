from netCDF4 import Dataset as NetCDFFile 
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

nc = NetCDFFile('/Users/Usuario/Desktop/twodegreessubset.nc')

lat = nc.variables['latitude'][:]
lon = nc.variables['longitude'][:]
time = nc.variables['time'][:]
t2 = nc.variables['p2t'][:] # 2 meter temperature
mslp = nc.variables['msl'][:] # mean sea level pressure
u = nc.variables['p10u'][:] # 10m u-component of winds
v = nc.variables['p10v'][:] # 10m v-component of winds

map = Basemap(projection='merc',llcrnrlon=-96.854178,llcrnrlat=-55.776573,urcrnrlon=151.054818,urcrnrlat=77.466028,resolution='i')

map.drawcoastlines()
map.drawstates()
map.drawcountries()
map.drawlsmask(land_color='Linen', ocean_color='#CCFFFF') # can use HTML names or codes for colors
map.drawcounties() # you can even add counties (and other shapefiles!)

lons,lats= np.meshgrid(lon-180,lat) # for this dataset, longitude is 0 through 360, so you need to subtract 180 to properly display on map
x,y = map(lons,lats)

clevs = np.arange(960,1040,4)
cs = map.contour(x,y,mslp[0,:,:]/100.,clevs,colors='blue',linewidths=1.)

temp = map.contourf(x,y,t2[4,:,:])
cb = map.colorbar(temp,"bottom", size="5%", pad="2%")
plt.title('2m Temperature')
cb.set_label('Temperature (K)')


plt.show()