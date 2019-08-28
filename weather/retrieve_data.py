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


def gfs_forecast_retrieve(lon_source,lat_source,nfcst):
    import urllib.request
    import urllib.error
    from datetime import datetime, date, timedelta
    from read import extract_data_gfs
    import os
    from shutil import copyfile
    from pathos.multiprocessing import Pool, ThreadingPool

    def wtfile_download(url, wtfile_dwnl):
        import urllib.request
        import urllib.error
        print('Downloading forecast file ' + url)
        urllib.request.urlretrieve(url, wtfile_dwnl)

    def elaborate_wtfiles(wtfile,wtfile_int,wtfile_prof,abs_validity):
        import os
        os.system(
            'wgrib2 ' + wtfile + ' -set_grib_type same -new_grid_winds earth -new_grid latlon ' + lon_corner + ':100:0.01 ' + lat_corner + ':100:0.01 ' +
            wtfile_int)
        print('Saving weather data along the vertical at the vent location')
        os.system('wgrib2 ' + wtfile_int + ' -s -lon ' + slon_source + ' ' + slat_source + '  >' + wtfile_prof)
        # Extract and elaborate weather data
        extract_data_gfs(year, month, day, abs_validity, wtfile_prof)

    cwd = os.getcwd()
    if(lon_source < 0):
        lon_source = 360 + lon_source

    now = str(datetime.utcnow())
    yesterday = str(datetime.utcnow().today() - timedelta(1))
    year= now[0:4]
    month = now[5:7]
    day = now[8:10]
    hour = now[11:13]
    year_yst = yesterday[0:4]
    month_yst = yesterday[5:7]
    day_yst = yesterday[8:10]
    urls = []
    wtfiles = []
    wtfiles_int = []
    wtfiles_prof = []
    abs_validities = []

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
    year_anl = year
    month_anl = month
    day_anl = day
    url = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + year_anl + month_anl + day_anl + '/' +  anl
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
        anl = '18'
        year_anl = year_yst
        month_anl = month_yst
        day_anl = day_yst
    elif 0 <= ianl < 10:
        anl = '0' + str(ianl)
    else:
        anl = str(ianl)
    url = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + year_anl + month_anl + day_anl + '/' + anl
    print('Most up to date GFS analysis: ' + url)

    data_folder = os.path.join(cwd,'raw_forecast_weather_data_'+ year + month + day + '/')
    # Retrieve weather data that best matches current time
    ifcst = ihour - ianl
    if ianl < 0:
        ianl = 18
        ifcst = ihour + 6
    # Check all forecast files are available
    max_ifcst = ifcst + nfcst
    while ifcst < max_ifcst:
        if ifcst < 10:
            fcst = 'f00' + str(ifcst)
        elif 10 <= ifcst < 100:
            fcst = 'f0' + str(ifcst)
        else:
            fcst = 'f' + str(ifcst)
        wtfile_dwnl = 'gfs.t' + anl + 'z.pgrb2.0p25.' + fcst
        url = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + year_anl + month_anl + day_anl + '/' + anl + '/' + wtfile_dwnl
        try:
            # urllib2.urlopen(url)
            urllib.request.urlopen(url)
        # except urllib2.HTTPError:
        except urllib.error.HTTPError as e:
            #       checksLogger.error('HTTPError = ' + str(e.code))
            ianl = ianl - 6
            ifcst = ifcst + 6
            print('Forecast file ' + wtfile_dwnl + ' not yet available. Retrieving the equivalent from the previous forecast')
            urls = []
            wtfiles = []
            max_ifcst = ifcst + nfcst
        except urllib.error.URLError as e:
            # except urllib2.URLError:
            #      checksLogger.error('URLError = ' + str(e.reason))
            ianl = ianl - 6
            ifcst = ifcst + 6
            print('Forecast file ' + wtfile_dwnl + ' not yet available. Retrieving the equivalent from the previous forecast')
            urls = []
            wtfiles = []
            max_ifcst = ifcst + nfcst
        if ianl < 0:
            ianl = 18
            year_anl = year_yst
            month_anl = month_yst
            day_anl = day_yst
            anl = str(ianl)
        elif 0 <= ianl < 10:
            anl = '0' + str(ianl)
        else:
            anl = str(ianl)
        ival = ianl + ifcst
        if ival < 10:
            validity = '0' + str(ival)
        elif ival >= 24:
            ival = ival - 24
            validity = '0' + str(ival)
        else:
            validity = str(ival)
        if ifcst < 10:
            fcst = 'f00' + str(ifcst)
        elif 10 <= ifcst < 100:
            fcst = 'f0' + str(ifcst)
        else:
            fcst = 'f' + str(ifcst)
        wtfile_dwnl = 'gfs.t' + anl + 'z.pgrb2.0p25.' + fcst
        abs_validity = year + month + day + validity
        elaborated_prof_file = 'profile_data_' + abs_validity + '.txt'
        elaborated_prof_file_path = os.path.join(data_folder, elaborated_prof_file)
        print('Checking if ' + elaborated_prof_file + ' exists in ' + data_folder)
        if os.path.isfile(elaborated_prof_file_path):
            print('File ' + elaborated_prof_file + ' already available in ' + data_folder)
            ifcst += 1
        else:
            abs_validities.append(abs_validity)
            wtfile = 'weather_data_' + year_anl + month_anl + day_anl + anl + '_' + fcst
            wtfile_int = 'weather_data_interpolated_' + year_anl + month_anl + day_anl + anl + '_' + fcst
            wtfile_prof = 'profile_' + year + month + day + anl + validity + '.txt'
            url = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + year_anl + month_anl + day_anl + '/' + anl + '/' + wtfile_dwnl
            print('Checking if ' + wtfile + ' exists in ' + data_folder)
            if os.path.isfile(data_folder + wtfile):
                print('File ' + wtfile + ' found')
                copyfile('raw_forecast_weather_data_' + year + month + day + '/' + wtfile, wtfile)
                ifcst += 1
            else:
                urls.append(url)
                ifcst += 1
            wtfiles.append(wtfile)
            wtfiles_int.append(wtfile_int)
            wtfiles_prof.append(wtfile_prof)
    try:
        pool = ThreadingPool(nfcst)
        pool.map(wtfile_download,urls,wtfiles)
    except:
        print('No new weather data downloaded')
    slon_source = str(lon_source)
    slat_source = str(lat_source)
    lon_corner = str(int(lon_source))
    lat_corner = str(int(lat_source))

    pool_1 = ThreadingPool(len(wtfiles))
    pool_1.map(elaborate_wtfiles,wtfiles,wtfiles_int,wtfiles_prof,abs_validities)
    #for i in range(0,len(wtfiles)-1):
    #    # Interpolate data to a higher resolution grid
    #    print('Interpolating weather data to a finer grid around the source')
    #    os.system(
    #        'wgrib2 ' + wtfiles[i] + ' -set_grib_type same -new_grid_winds earth -new_grid latlon ' + lon_corner + ':100:0.01 ' + lat_corner + ':100:0.01 ' + wtfiles_int[i])
    #    print('Saving weather data along the vertical at the vent location')
    #    os.system('wgrib2 ' + wtfiles_int[i] + ' -s -lon ' + slon_source + ' ' + slat_source + '  >' + wtfiles_prof[i])
    #    # Extract and elaborate weather data
    #    extract_data_gfs(year, month, day, abs_validities[i], wtfiles_prof[i])

def era_interim_retrieve(lon_source,lat_source,eruption_start,eruption_stop):
    from ecmwfapi import ECMWFDataServer
    from read import extract_data_erain
    import os
    from shutil import copyfile
    cwd = os.getcwd()
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
    #data_folder = 'raw_reanalysis_weather_data_' + year_start + month_start + day_start + '/'
    data_folder = os.path.join(cwd,'raw_reanalysis_weather_data_' + year_start + month_start + day_start + '/')
    wtfile = 'weather_data_' + date_bis
    wtfile_path = os.path.join(cwd,data_folder,wtfile)
    grib_file = "pressure_level.grib"
    grib_file_path = os.path.join(cwd,data_folder,grib_file)
    print('Checking if file ' + wtfile + ' exists in ' + data_folder)

    #if os.path.isfile(wtfile):
    if os.path.isfile(wtfile_path):
        print('File ' + wtfile + ' found')
        copyfile(wtfile_path,wtfile)
        copyfile(grib_file_path,grib_file)
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

def era5_retrieve(lon_source,lat_source,eruption_start,eruption_stop):
    from read import extract_data_erain
    import os
    from shutil import copyfile
    from datetime import timedelta as td, datetime

    def era5_request(index):
        import cdsapi
        print('Downloading file from ERA5 database')
        c = cdsapi.Client()
        try:
            c.retrieve(
             'reanalysis-era5-pressure-levels',
             {
                 'pressure_level': [
                     '1', '2', '3',
                     '5', '7', '10',
                     '20', '30', '50',
                     '70', '100', '125',
                     '150', '175', '200',
                     '225', '250', '300',
                     '350', '400', '450',
                     '500', '550', '600',
                     '650', '700', '750',
                     '775', '800', '825',
                     '850', '875', '900',
                     '925', '950', '975',
                     '1000'
                 ],
                 'variable': [
                     'geopotential', 'temperature',
                     'u_component_of_wind', 'v_component_of_wind'
                 ],
                 'time': [
                     '00:00', '01:00', '02:00',
                     '03:00', '04:00', '05:00',
                     '06:00', '07:00', '08:00',
                     '09:00', '10:00', '11:00',
                     '12:00', '13:00', '14:00',
                     '15:00', '16:00', '17:00',
                     '18:00', '19:00', '20:00',
                     '21:00', '22:00', '23:00'
                 ],
                 'product_type': 'reanalysis',
                 'year': years[index],
                 'day': days[index],
                 'month': months[index],
                 'area': area,
                 'format': 'grib'
             },
                str(index) + '.grib')
        except:
            print('Unable to retrieve ERA5 data')

    cwd = os.getcwd()
    year_start = eruption_start[0:4]
    month_start = eruption_start[4:6]
    day_start = eruption_start[6:8]
    year_stop = eruption_stop[0:4]
    month_stop = eruption_stop[4:6]
    day_stop = eruption_stop[6:8]
    slon_source = str(lon_source)
    slat_source = str(lat_source)
    date_bis = year_start + '-' + month_start + '-' + day_start + '_to_' + year_stop + '-' + month_stop + '-' + day_stop
    data_folder = os.path.join(cwd,'raw_reanalysis_weather_data_' + year_start + month_start + day_start + '/')
    wtfile = 'weather_data_' + date_bis
    wtfile_path = os.path.join(cwd,data_folder,wtfile)
    grib_file = "pressure_level.grib"
    grib_file_path = os.path.join(cwd,data_folder,grib_file)
    print('Checking if file ' + wtfile + ' exists in ' + data_folder)

    if os.path.isfile(wtfile_path):
        print('File ' + wtfile + ' found')
        copyfile(wtfile_path,wtfile)
        copyfile(grib_file_path,grib_file)
    else:
        # Define area
        lat_N = int(lat_source) + 2
        lat_S = int(lat_source) - 2
        lon_W = int(lon_source) - 2
        lon_E = int(lon_source) + 2
        area = [lat_N,lon_W,lat_S,lon_E]
        # Define time vectors
        #start = datetime.strptime(eruption_start, '%Y-%m-%d %H:%M:%S')
        #stop = datetime.strptime(eruption_stop, '%Y-%m-%d %H:%M:%S')
        start = datetime.strptime(eruption_start, '%Y%m%d%H')
        stop = datetime.strptime(eruption_stop, '%Y%m%d%H')
        delta = td(days=1)
        dt_eruption = stop - start
        dt_eruption_seconds = dt_eruption.total_seconds()
        dt_eruption_days = int(divmod(dt_eruption_seconds, 86400)[0]) + 1
        day = start
        nmax_days = 20 # This looks like the optimal number of days to split
        jmax = int(dt_eruption_days / nmax_days)
        days = [[0 for k in range(0, nmax_days)] for j in range(0, jmax + 1)]
        years = []
        months = []
        j = 0
        while j <= jmax:
            k = 0
            years.append(str(day)[0:4])
            months.append(str(day)[5:7])
            while k <= nmax_days - 1:
                if day > start and str(day)[8:10] == '01' and k > 0:
                    j_zeros = j # Check where the 0s are
                    k += 1
                else:
                    days[j][k] = str(day)[8:10]
                    day += delta
                    if day > stop:
                        break
                k += 1
            j += 1
        # Remove zeros from days array
        try:
            for k in range(0,nmax_days-1):
                days[j_zeros].remove(0)
        except:
            print('No more zeros found in days')
        # Remove zeros from days array
        try:
            for k in range(0,nmax_days-1):
                days[jmax].remove(0)
        except:
            print('No more zeros found in days')

        filenames_s = ''
        if jmax == 0:
            era5_request(jmax)
            filenames_s = str(jmax) + '.grib'
        else:
            for j in range(0,jmax + 1):
                era5_request(j)
                filenames_s = filenames_s + ' ' + str(j) + '.grib'
        # Merge all files
        try:
            if os.system('cat ' + filenames_s + '> pressure_level.grib') != 0: #Linux command to concatenate files
                if os.system('type ' + filenames_s + ' > pressure_level.grib') != 0: #Windows command to concatenate files
                    raise Exception
                else:
                    print('Grib files successfully concatenated')
        except:
            print('Unable to concatenate grib files')
        # Delete all unconcatenated source files
        try:
            if os.system('rm ' + filenames_s) != 0: #Linux command to concatenate files
                if os.system('del ' + filenames_s) != 0: #Windows command to concatenate files
                    raise Exception
                else:
                    print('Unconcatenated source files removed')
        except:
            print('No source grib files found')

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
    validities = []
    years = []
    months = []
    days = []
    wtfiles_prof_step = []
    for validity in steps:
        validities.append(validity)
        year = validity[0:4]
        years.append(year)
        month = validity[4:6]
        months.append(month)
        day = validity[6:8]
        days.append(day)
        hour = validity[8:10]
        wtfile_prof_step = 'profile_' + validity + '.txt'
        wtfiles_prof_step.append(wtfile_prof_step)
        #extract_data_erain(year, month, day, validity, wtfile_prof_step)

    # Extract and elaborate weather data
    pool = ThreadingPool(len(validities))
    pool.map(elaborate_data_erain, years, months, days, validities, wtfiles_prof_step)

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

    cwd = os.getcwd()
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

    #data_folder = 'raw_reanalysis_weather_data_' + str(eruption_start.year) + str(eruption_start.month) + str(eruption_start.day) + '/'
    data_folder = os.path.join(cwd,'raw_reanalysis_weather_data_' + str(eruption_start.year) + str(eruption_start.month) + str(eruption_start.day) + '/')
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
            elaborated_prof_file_path = os.path.join(data_folder,elaborated_prof_file)
            print('Checking if ' + elaborated_prof_file + ' exists in ' + data_folder)
            #if os.path.isfile(data_folder + elaborated_prof_file):
            if os.path.isfile(elaborated_prof_file_path):
                print('File ' + elaborated_prof_file + ' already available in ' + data_folder)
                break
                #continue
            data_folder = os.path.join(cwd,'raw_reanalysis_weather_data_'+ day_validity + '/')
            wtfile_dwnl = month_validity + '/' + day_validity + '/' + 'gfs_4_' + day_validity + '_' + hour + '00_' + fcst + '.grb2'
            wtfile = 'weather_data_' + year + month + day + hour + '_' + fcst
            wtfile_path = os.path.join(data_folder,wtfile)
            wtfile_int = 'weather_data_interpolated_' + year + month + day + hour + '_' + fcst
            wtfile_prof = 'profile_' + year + month + day + hour + validity + '.txt'
            url1 = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + year + month + day + '/' + hour + '/gfs.t' + hour + 'z.pgrb2.0p25.f' + fcst
            url2 = 'https://nomads.ncdc.noaa.gov/data/gfs4/' + wtfile_dwnl
            print('Checking if ' + wtfile + ' exists')
            if os.path.isfile(wtfile_path):
            #if os.path.isfile('raw_reanalysis_weather_data_'+ day_validity + '/' + wtfile):
                print('File ' + wtfile + ' found')
                #copyfile('raw_reanalysis_weather_data_'+ day_validity + '/' + wtfile,wtfile)
                copyfile(wtfile_path, wtfile)
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
