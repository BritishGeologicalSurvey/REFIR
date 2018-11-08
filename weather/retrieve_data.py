"""
*** retrieve_data v1.0 ***
- component of the weather package included in REFIR 19.0 -
- Script to weather data from GFS and ERA-Interim datasets -

Copyright (C) 2018 Tobias Dürig, Fabio Dioguardi
==============                     ===================
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option               any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.                                   If not, see <https://www.gnu.org/licenses/>.

If you wish to contribute to the development of REFIR or to reports bugs or other problems with
the software, please write an email to me.

Contact: tobi@hi.is, fabiod@bgs.ac.uk


RNZ170318FS
"""


def gfs_forecast_retrieve(lon_source,lat_source):
    import urllib.request
    import urllib.error
    #	import urllib2
    from datetime import datetime, date, timedelta
    from read import extract_data_gfs
    import os
    from shutil import copyfile

    if(lon_source < 0):
        lon_source = 360 + lon_source
    now = str(datetime.utcnow())
    yesterday = str(datetime.utcnow().today() - timedelta(1))
    year = now[0:4]
    month = now[5:7]
    day = now[8:10]
    hour = now[11:13]
    year_yst = yesterday[0:4]
    month_yst = yesterday[5:7]
    day_yst = yesterday[8:10]

    # Find last GFS analysis
    ihour = int(hour)
    if 0 <= ihour < 6:
        ianl = 0
    elif 6 <= ihour < 12:
        ianl = 6
    elif 12 <= ihour < 18:
        ianl = 12
    else:
        ianl = 18
    if ianl < 10:
        anl = '0' + str(ianl)
    else:
        anl = str(ianl)
    url = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + year + month + day + anl
    try:
        # urllib2.urlopen(url)
        urllib.request.urlopen(url)
    # except urllib2.HTTPError:
    except urllib.error.HTTPError as e:
        #	checksLogger.error('HTTPError = ' + str(e.code))
        ianl = ianl - 6
        print('Analysis file at ' + anl + 'z not yet available. Retrieving the latest available')
    # except urllib2.URLError:
    except urllib.error.URLError as e:
        #   	checksLogger.error('URLError = ' + str(e.reason))
        ianl = ianl - 6
        print('Analysis file at ' + anl + 'z not yet available. Retrieving the latest available')
    if ianl < 0:  # this is in case the analysis at 00z is not available; in this case, ianl = -6 from above, hence must be corrected. Additionally, the variable ianl will be updated later otherwise it would affect ifcst
        year = year_yst
        month = month_yst
        day = day_yst
        anl = '18'
    elif 0 <= ianl < 10:
        anl = '0' + str(ianl)
    else:
        anl = str(ianl)
    url = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + year + month + day + anl
    print('Most up to date GFS analysis: ' + url)

    # Retrieve weather data that best matches current time
    ifcst = ihour - ianl
    if ianl < 0:
        ianl = 18

    if ifcst < 10:
        fcst = 'f00' + str(ifcst)
    elif 10 < ifcst < 100:
        fcst = 'f0' + str(ifcst)
    else:
        fcst = 'f' + str(ifcst)
    wtfile = 'gfs.t' + anl + 'z.pgrb2.0p25.' + fcst
    url = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + year + month + day + anl + '/' + wtfile
    try:
        # urllib2.urlopen(url)
        urllib.request.urlopen(url)
    # except urllib2.HTTPError:
    except urllib.error.HTTPError as e:
        #       checksLogger.error('HTTPError = ' + str(e.code))
        ianl = ianl - 6
        ifcst = ifcst + 6
        print('Forecast file ' + wtfile + ' not yet available. Retrieving the equivalent from the previous forecast')
    except urllib.error.URLError as e:
        # except urllib2.URLError:
        #      checksLogger.error('URLError = ' + str(e.reason))
        ianl = ianl - 6
        ifcst = ifcst + 6
        print('Forecast file ' + wtfile + ' not yet available. Retrieving the equivalent from the previous forecast')

    if ianl < 10:
        anl = '0' + str(ianl)
    else:
        anl = str(ianl)

    slon_source = str(lon_source)
    slat_source = str(lat_source)
    lon_corner = str(int(lon_source))
    lat_corner = str(int(lat_source))

    data_folder = 'raw_forecast_weather_data_'+ year + month + day + '/'

    ival = ianl + ifcst
    if ival < 10:
        validity = '0' + str(ival)
    else:
        validity = str(ival)
    if ifcst < 10:
        fcst = 'f00' + str(ifcst)
    elif 10 <= ifcst < 100:
        fcst = 'f0' + str(ifcst)
    else:
        fcst = 'f' + str(ifcst)
    abs_validity = year + month + day + validity
    elaborated_prof_file = 'profile_data_' + abs_validity + '.txt'
    print('Checking if ' + elaborated_prof_file + ' exists in ' + data_folder)
    if os.path.isfile(data_folder + elaborated_prof_file):
        print('File ' + elaborated_prof_file + ' already available in ' + data_folder)
    else:
        wtfile_dwnl = 'gfs.t' + anl + 'z.pgrb2.0p25.' + fcst
        wtfile = 'weather_data_' + year + month + day + anl + '_' + fcst
        wtfile_int = 'weather_data_interpolated_' + year + month + day + anl + '_' + fcst
        wtfile_prof = 'profile_' + year + month + day + anl + validity + '.txt'
        url = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + year + month + day + anl + '/' + wtfile_dwnl
        print('Checking if ' + wtfile + ' exists')
        if os.path.isfile(data_folder + wtfile):
            print('File ' + wtfile + ' found')
            copyfile('raw_forecast_weather_data_' + year + month + day + '/' + wtfile, wtfile)
        else:
            print('Downloading forecast file ' + url)
            urllib.request.urlretrieve(url, wtfile)
        # Interpolate data to a higher resolution grid
        print('Interpolating weather data to a finer grid around the source')
        os.system(
            'wgrib2 ' + wtfile + ' -set_grib_type same -new_grid_winds earth -new_grid latlon ' + lon_corner + ':100:0.01 ' + lat_corner + ':100:0.01 ' + wtfile_int)
        print('Saving weather data along the vertical at the vent location')
        os.system('wgrib2 ' + wtfile_int + ' -s -lon ' + slon_source + ' ' + slat_source + '  >' + wtfile_prof)
        # Extract and elaborate weather data
        extract_data_gfs(year, month, day, abs_validity, wtfile_prof)

def era_interim_retrieve(lon_source,lat_source,eruption_start,eruption_stop):
    from ecmwfapi import ECMWFDataServer
    from read import extract_data_erain
    import os
    if(lon_source < 0):
        lon_source = 360 + lon_source
    year_start = eruption_start[0:4]
    month_start = eruption_start[4:6]
    day_start = eruption_start[6:8]
    hour_start = eruption_start[8:10]
    year_stop = eruption_stop[0:4]
    month_stop = eruption_stop[4:6]
    day_stop = eruption_stop[6:8]
    hour_stop = eruption_stop[8:10]
    slon_source = str(lon_source)
    slat_source = str(lat_source)
    date = year_start + '-' + month_start + '-' + day_start + '/to/' + year_stop + '-' + month_stop + '-' + day_stop
    date_bis = year_start + '-' + month_start + '-' + day_start + '_to_' + year_stop + '-' + month_stop + '-' + day_stop
    lat_SW = str(int(lat_source) - 2)
    lon_SW = str(int(lon_source) - 2)
    lat_NE = str(int(lat_source) + 2)
    lon_NE = str(int(lon_source) + 2)
    lon_corner = str(int(lon_source))
    lat_corner = str(int(lat_source))
    area = lat_SW + '/' + lon_SW + '/' + lat_NE + '/' + lon_NE

    wtfile = 'weather_data_' + date_bis

    print('Checking if file ' + wtfile + ' exists')

    if os.path.isfile(wtfile):
        print('File ' + wtfile + 'found')
    else:
        print('Downloading file from ERA Interim database')
        server = ECMWFDataServer()
        try:
            server.retrieve({
            "class": "ei",
            "dataset": "interim",
            "expver": "1",
            'date': date,
            'area': area,
            "grid": "0.75/0.75",
            "levelist": "1/2/3/5/7/10/20/30/50/70/100/125/150/175/200/225/250/300/350/400/450/500/550/600/650/700/750/775/800/825/850/875/900/925/950/975/1000",
            "levtype": "pl",
            "param": "129.128/130.128/131.128/132.128",
            "step": "0",
            "stream": "oper",
            "time": "00:00:00/06:00:00/12:00:00/18:00:00",
            "type": "an",
            'target': "pressure_level.grib"
            })
        except:
            print('Unable to retrieve ERA Interim data')

    # Convert grib1 to grib2 with the NOAA Perl script. To make it more portable and avoiding the need to set up many paths, I have included in the package also the required files and scripts that are originally available in the grib2 installation folder
    print('Converting grib1 data to grib2')

    os.system('grib_set -s edition=2 pressure_level.grib ' + wtfile)
    wtfile_prof = 'profile_' + date_bis + '.txt'
    print('Saving weather data along the vertical at the vent location')
    os.system('wgrib2 ' + wtfile + ' -s -lon ' + slon_source + ' ' + slat_source + '  >' + wtfile_prof)
    # Split wtfile_prof into multiple file, each one for a specific time step
    splitLen = 148
    outputBase = 'profile_'
    input = open(wtfile_prof, 'r',encoding="utf-8", errors="surrogateescape")
    count = 0
    dest = None
    steps = []
    for line in input:
        if count % splitLen == 0:
            if dest: dest.close()
            first_line = line.split(':')
            val = first_line[2].split('d=')
            dest = open(outputBase + val[1] + '.txt', 'w',encoding="utf-8", errors="surrogateescape")
            steps.append(val[1])
        dest.write(line)
        count += 1
    input.close()
    dest.close()
    for validity in steps:
        year = validity[0:4]
        month = validity[4:6]
        day = validity[6:8]
        hour = validity[8:10]
        wtfile_prof_step = 'profile_' + validity + '.txt'
        # Extract and elaborate weather data
        extract_data_erain(year, month, day, validity, wtfile_prof_step)

def gfs_past_forecast_retrieve(lon_source,lat_source,eruption_start,eruption_stop):
    import urllib.request
    import urllib.error
    import os
    from shutil import copyfile
    from datetime import datetime,timedelta
    from read import extract_data_gfs

    def datespan(startDate, endDate, delta=timedelta(days=1)):
        currentDate = startDate
        while currentDate < endDate:
            yield currentDate
            currentDate += delta

    if(lon_source < 0):
        lon_source = 360 + lon_source
    slon_source = str(lon_source)
    slat_source = str(lat_source)
    lon_corner = str(int(lon_source))
    lat_corner = str(int(lat_source))

    if eruption_start.hour < 6:
        dt = eruption_start.hour
    elif 6 <= eruption_start.hour < 12:
        dt = eruption_start.hour - 6
    elif 12 <= eruption_start.hour < 18:
        dt = eruption_start.hour - 12
    else:
        dt = eruption_start.hour - 18

    data_folder = 'raw_reanalysis_weather_data_' + str(eruption_start.year) + str(eruption_start.month) + str(eruption_start.day) + '/'
    first_analysis = eruption_start - timedelta(hours=dt)
    ifcst = dt
    count = 1
    for analyses in datespan(first_analysis,eruption_stop,timedelta(hours=6)):
        year = str(analyses.year)
        month = str(analyses.month)
        if len(month) == 1:
            month = '0' + month
        day = str(analyses.day)
        if len(day) == 1:
            day = '0' + day
        hour = str(analyses.hour)
        ianl = analyses.hour
        if (len(hour)) == 1:
            hour = '0' + hour
        while ifcst < 6:
            ival = ianl + ifcst
            eruption_current = datetime(analyses.year,analyses.month,analyses.day,ival)
            if eruption_current > eruption_stop:
                break
            if ival < 10:
                validity = '0' + str(ival)
            else:
                validity = str(ival)
            if ifcst < 10:
                fcst = '00' + str(ifcst)
            elif 10 <= ifcst < 100:
                fcst = '0' + str(ifcst)
            else:
                fcst = str(ifcst)
            month_validity = year + month
            day_validity = month_validity + day
            abs_validity = day_validity + validity
            elaborated_prof_file = 'profile_data_' + abs_validity + '.txt'
            print('Checking if ' + elaborated_prof_file + ' exists in ' + data_folder)
            if os.path.isfile(data_folder + elaborated_prof_file):
                print('File ' + elaborated_prof_file + ' already available in ' + data_folder)
                continue
            wtfile_dwnl = month_validity + '/' + day_validity + '/' + 'gfs_4_' + day_validity + '_' + hour + '00_' + fcst + '.grb2'
            wtfile = 'weather_data_' + year + month + day + hour + '_' + fcst
            wtfile_int = 'weather_data_interpolated_' + year + month + day + hour + '_' + fcst
            wtfile_prof = 'profile_' + year + month + day + hour + validity + '.txt'
            url1 = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + year + month + day + hour + '/gfs.t' + hour + 'z.pgrb2.0p25.f' + fcst
            url2 = 'https://nomads.ncdc.noaa.gov/data/gfs4/' + wtfile_dwnl
            print('Checking if ' + wtfile + ' exists')
            if os.path.isfile('raw_reanalysis_weather_data_'+ day_validity + '/' + wtfile):
                print('File ' + wtfile + ' found')
                copyfile('raw_reanalysis_weather_data_'+ day_validity + '/' + wtfile,wtfile)
            else:
                print('Downloading forecast file ' + url1)
                try:
                    urllib.request.urlretrieve(url1, wtfile)
                except:
                    print('Error. Url ' + url1 + ' is not available')
                    if ifcst == 0 or ifcst == 3:
                        print('Downloading forecast file ' + url2)
                        count = 1000
                        try:
                            urllib.request.urlretrieve(url2, wtfile)
                        except:
                            print('Error. Url ' + url2 + ' is not available')
                            ifcst = ifcst + 1
                            return (False)
                    else:
                        if count == 1:
                            ifcst = ifcst - 1
                        else:
                            ifcst = ifcst + 1
                        continue
            # Interpolate data to a higher resolution grid
            print('Interpolating weather data to a finer grid around the source')
            os.system(
                'wgrib2 ' + wtfile + ' -set_grib_type same -new_grid_winds earth -new_grid latlon ' + lon_corner + ':100:0.01 ' + lat_corner + ':100:0.01 ' + wtfile_int)
            print('Saving weather data along the vertical at the vent location')
            os.system('wgrib2 ' + wtfile + ' -s -lon ' + slon_source + ' ' + slat_source + '  >' + wtfile_prof)
            # Extract and elaborate weather data
            extract_data_gfs(year, month, day, abs_validity, wtfile_prof)
            ifcst = ifcst + 1
        ifcst = 0

    return (True)