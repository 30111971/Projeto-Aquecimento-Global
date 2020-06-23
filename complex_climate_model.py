import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
import climlab
from scipy.optimize import brentq
import math

def plot_sounding(collist):
    color_cycle=['r', 'g', 'b', 'y']
    # col is either a column model object or a list of column model objects
    if isinstance(collist, climlab.Process):
        # make a list with a single item
        collist = [collist]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i, col in enumerate(collist):
        zstar = -np.log(col.lev/climlab.constants.ps)
        ax.plot(col.Tatm, zstar, color=color_cycle[i])
        ax.plot(col.Ts, 0, 'o', markersize=12, color=color_cycle[i])
    #ax.invert_yaxis()
    yticks = np.array([1000., 750., 500., 250., 100., 50., 20., 10.])
    ax.set_yticks(-np.log(yticks/1000.))
    ax.set_yticklabels(yticks)
    ax.set_xlabel('Temperature (K)')
    ax.set_ylabel('Pressure (hPa)')
    ax.grid()
    return ax

def OLRanom(eps):
    col.subprocess['LW'].absorptivity = eps
    col.compute_diagnostics()
    return col.diagnostics['OLR'] - 239.

ncep_url = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/ncep.reanalysis.derived/"
ncep_air = nc.Dataset( ncep_url + "pressure/air.mon.1981-2010.ltm.nc" )
level = ncep_air.variables['level'][:]
lat = ncep_air.variables['lat'][:]

zstar = -np.log(level/1000)

Tzon = np.mean(ncep_air.variables['air'][:],axis=(0,3))
Tglobal = np.average( Tzon , weights=np.cos(np.deg2rad(lat)), axis=1) + climlab.constants.tempCtoK

col = climlab.GreyRadiationModel()
lev = col.lev
Tinterp = np.flipud(np.interp(np.flipud(lev), np.flipud(level), np.flipud(Tglobal)))

col.Ts[:] = Tglobal[0]
col.Tatm[:] = Tinterp

epsarray = np.linspace(0.01, 0.1, 100)
OLRarray = np.zeros_like(epsarray)

# col está em equilibro térmico
eps = brentq(OLRanom, 0.01, 0.1)
col.subprocess['LW'].absorptivity = eps

col2 = climlab.process_like(col)

def log(a):
    return math.log(a)

absorptivityChangeRate = 1.0005
years = 90
# Aumentando a taxa de absorção de radiação com amplo comprimento de onda
for i in range(years):
    col2.subprocess['LW'].absorptivity *= absorptivityChangeRate
    col2.integrate_years(1.)
    col2.compute_diagnostics()
    absorptivityChangeRate += -(1/(log(1/(absorptivityChangeRate-1))*(1/((absorptivityChangeRate-1)*((absorptivityChangeRate-1)-(1/(log(1/(absorptivityChangeRate-1))*(1/(absorptivityChangeRate-1)))))))))
    print(col2.Ts)

#print(col2.diagnostics['OLR'])
#print(col2.Ts)

#RF = -(col2.diagnostics['OLR'] - col.diagnostics['OLR'])
re = climlab.process_like(col)
for i in range(years):
    re.integrate_years(1.)
    re.compute_diagnostics()

rce = climlab.RadiativeConvectiveModel(adj_lapse_rate=6.)
rce.subprocess['LW'].absorptivity = eps

plot_sounding([col2, re])

