def gfs_forecast_retrieve(lon_source, lat_source):
    import urllib.request
    import urllib.error
    #	import urllib2
    from datetime import datetime, date, timedelta
    from read import extract_data_gfs
    import os
    now = str(datetime.utcnow())
    yesterday = str(date.today() - timedelta(1))
    year = now[0:4]
    month = now[5:7]
    day = now[8:10]
    hour = now[11:13]
    year_yst = yesterday[0:4]
    month_yst = yesterday[5:7]
    day_yst = yesterday[8:10]

    # Find last GFS analysis
    ihour = int(hour)
    if 0 < ihour < 6:
        ianl = 0
    elif 6 < ihour < 12:
        ianl = 6
    elif 12 < ihour < 18:
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
    elif 0 < ianl < 10:
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

    fcst_list = [ifcst, ifcst + 1, ifcst + 2, ifcst + 3, ifcst + 4]
    for ifcst in fcst_list:
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
        wtfile_dwnl = 'gfs.t' + anl + 'z.pgrb2.0p25.' + fcst
        wtfile = 'weather_data_' + year + month + day + anl + '_' + fcst
        wtfile_int = 'weather_data_interpolated_' + year + month + day + anl + '_' + fcst
        wtfile_prof = 'profile_' + year + month + day + anl + validity + '.txt'
        url = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + year + month + day + anl + '/' + wtfile_dwnl
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


# Move all weather data into the folder weather
#	os.system('mkdir weather')
#	os.system('mv profile_* weather_* tropopause_* weather/gfs')

def era_interim_retrieve(eruption_start, eruption_stop, lon_source, lat_source):
    from ecmwfapi import ECMWFDataServer
    from read import extract_data_erain
    import os

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

    server = ECMWFDataServer()
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

    # Convert grib1 to grib2 with the NOAA Perl script. To make it more portable and avoiding the need to set up many paths, I have included in the package also the required files and scripts that are originally available in the grib2 installation folder
    print('Converting grib1 data to grib2')

    wtfile = 'weather_data_' + date_bis
    os.system('grib_set -s edition=2 pressure_level.grib ' + wtfile)
    wtfile_prof = 'profile_' + date_bis + '.txt'
    print('Saving weather data along the vertical at the vent location')
    os.system('wgrib2 ' + wtfile + ' -s -lon ' + slon_source + ' ' + slat_source + '  >' + wtfile_prof)
    # Split wtfile_prof into multiple file, each one for a specific time step
    splitLen = 148
    outputBase = 'profile_'
    input = open(wtfile_prof, 'r')
    count = 0
    dest = None
    steps = []
    for line in input:
        if count % splitLen == 0:
            if dest: dest.close()
            first_line = line.split(':')
            val = first_line[2].split('d=')
            dest = open(outputBase + val[1] + '.txt', 'w')
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
