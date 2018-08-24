from retrieve_data import era_interim_retrieve
from retrieve_data import gfs_forecast_retrieve
import os
from datetime import datetime, date, timedelta

mode = 'forecast'  # This will be an input
lon_source = 350  # this will be an input in the function
lat_source = 41.06  # this will be an input in the function
eruption_start = '2010041700'
eruption_stop = '2010041918'

if mode == 'reanalysis':
    era_interim_retrieve(eruption_start, eruption_stop, lon_source, lat_source)  # eruption_start, eruption_stop will be an input
elif mode == 'forecast':
    gfs_forecast_retrieve(lon_source, lat_source)
now = str(datetime.utcnow())
year = now[0:4]
month = now[5:7]
day = now[8:10]
hour = now[11:13]
minute = now[14:16]
folder = 'data_' + year + month + day + hour + minute
os.system('mkdir ' + folder)
if (os.name == 'posix'):
    os.system('mv pressure_level.grib weather_* profile_* tropopause_* ' + folder)
elif (os.name == 'nt'):
    os.system('move pressure_level.grib ' + folder)
    os.system('move weather_* ' + folder)
    os.system('move profile_* ' + folder)
