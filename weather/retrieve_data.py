"""
*** retrieve_data v2.0 ***
- component of the weather package included in REFIR 20.0 -
- Script to weather data from GFS and ERA5 datasets -

Copyright (C) 2020 Tobias Dürig, Fabio Dioguardi
==============                     ===================
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
at your option any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

If you wish to contribute to the development of REFIR or to reports bugs or other problems with
the software, please write an email to me.

Contact: tobi@hi.is, fabiod@bgs.ac.uk


RNZ170318FS
"""

import urllib.request
import urllib.error
from datetime import datetime, date, timedelta
from read import extract_data_gfs
import os
from shutil import copyfile
from pathos.multiprocessing import Pool, ThreadingPool

def wtfile_download(url, wtfile_dwnl):
    print('Downloading forecast file ' + url)
    urllib.request.urlretrieve(url, wtfile_dwnl)

def elaborate_wtfiles(wtfile,wtfile_int,wtfile_prof,abs_validity, zoom, lon_corner, lat_corner, slon_source, slat_source):
    cwd = os.getcwd()
    if zoom:
        os.system('wgrib2 ' + wtfile + ' -set_grib_type same -new_grid_winds earth -new_grid latlon ' + lon_corner + ':400:0.01 ' + lat_corner + ':400:0.01 ' +
                wtfile_int)
    else:
        copyfile(os.path.join(cwd,wtfile),os.path.join(cwd,wtfile_int))
    print('Saving weather data along the vertical at the vent location')
    os.system('wgrib2 ' + wtfile_int + ' -s -lon ' + slon_source + ' ' + slat_source + '  >' + wtfile_prof)
    # Extract and elaborate weather data
    extract_data_gfs(abs_validity, wtfile_prof)

def gfs_forecast_retrieve(lon_source,lat_source,nfcst, time_in):
    cwd = os.getcwd()
    slon_source_left = str(lon_source - 2)
    slon_source_right = str(lon_source + 2)
    slat_source_bottom = str(lat_source - 2)
    slat_source_top = str(lat_source + 2)
    if(lon_source < 0):
        lon_source = 360 + lon_source
    slon_source = str(lon_source)
    slat_source = str(lat_source)
    lon_corner = str(int(lon_source - 2))
    lat_corner = str(int(lat_source - 2))
    if time_in != 999:
        now = str(time_in)
    else:
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
    zooms = []
    lon_corners = []
    lat_corners = []
    slon_sources = []
    slat_sources = []
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
    anl = "{:02d}".format(ianl)
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
        fcst = 'f' + "{:03d}".format(ifcst)
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
        fcst = 'f' + "{:03d}".format(ifcst)
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
            try:
                url = 'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?file=' + wtfile_dwnl + '&all_lev=on&var_HGT=on&var_TMP=on&var_UGRD=on&var_VGRD=on&subregion=&leftlon=' + slon_source_left + '&rightlon=' + slon_source_right + '&toplat=' + slat_source_top + '&bottomlat=' + slat_source_bottom + '&dir=%2Fgfs.' + year_anl + month_anl + day_anl + '%2F' + anl
                urllib.request.urlopen(url)
                zoom = False
            except:
                url = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + year_anl + month_anl + day_anl + '/' + anl + '/' + wtfile_dwnl
                urllib.request.urlopen(url)
                zoom = True
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
            zooms.append(zoom)
            lon_corners.append(lon_corner)
            lat_corners.append(lat_corner)
            slon_sources.append(slon_source)
            slat_sources.append(slat_source)
    try:
        pool = ThreadingPool(nfcst)
        pool.map(wtfile_download,urls,wtfiles)
    except:
        print('No new weather data downloaded')

    if len(wtfiles) > 0:
        pool_1 = ThreadingPool(len(wtfiles))
        pool_1.map(elaborate_wtfiles,wtfiles,wtfiles_int,wtfiles_prof,abs_validities, zooms, lon_corners, lat_corners, slon_sources, slat_sources)

def era5_retrieve(lon_source,lat_source,eruption_start,eruption_stop):
    from read import extract_data_era5
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

    def elaborate_data_era5(validity, wtfile_prof_step):
        # Extract and elaborate weather data
        extract_data_era5(validity, wtfile_prof_step)

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

    # Extract and elaborate weather data
    max_number_processes = 100
    if len(validities) > max_number_processes:
        n_elaborated_days = 0
        pools = []
        n_pool = 0
        while n_elaborated_days <= len(validities):
            end = n_elaborated_days + max_number_processes
            if end > len(validities):
                end = len(validities)
            n_elaborated_days = end
            pools.append(n_pool)
            n_pool += 1
            if n_elaborated_days == len(validities):
                break
        n_elaborated_days = 0
        n_pool = 0
        while n_elaborated_days <= len(validities):
            start = n_elaborated_days
            end = n_elaborated_days + max_number_processes
            if end > len(validities):
                end = len(validities)
            try:
                pools[n_pool] = ThreadingPool(max_number_processes)
                pools[n_pool].map(elaborate_data_era5, validities[start:end],wtfiles_prof_step[start:end])
            except:
                print('Unable to process reanalysis weather data')
                exit()
            n_elaborated_days = end
            n_pool += 1
            if n_elaborated_days == len(validities):
                break
    else:
        pool = ThreadingPool(len(validities))
        pool.map(elaborate_data_era5, validities, wtfiles_prof_step)


def gfs_past_forecast_retrieve(lon_source,lat_source,eruption_start,eruption_stop):
    def datespan(startDate, endDate, delta=timedelta(days=1)):
        currentDate = startDate
        while currentDate < endDate:
            yield currentDate
            currentDate += delta

    cwd = os.getcwd()
    slon_source_left = str(lon_source - 2)
    slon_source_right = str(lon_source + 2)
    slat_source_bottom = str(lat_source - 2)
    slat_source_top = str(lat_source + 2)
    if(lon_source < 0):
        lon_source = 360 + lon_source
    slon_source = str(lon_source)
    slat_source = str(lat_source)
    lon_corner = str(int(lon_source - 2))
    lat_corner = str(int(lat_source - 2))

    if eruption_start.hour < 6:
        dt = eruption_start.hour
    elif 6 <= eruption_start.hour < 12:
        dt = eruption_start.hour - 6
    elif 12 <= eruption_start.hour < 18:
        dt = eruption_start.hour - 12
    else:
        dt = eruption_start.hour - 18
    data_folder = os.path.join(cwd, 'raw_reanalysis_weather_data_' + eruption_start.strftime('%Y') + eruption_start.strftime('%m') + eruption_start.strftime('%d') + '/')
    first_analysis = eruption_start - timedelta(hours=dt)
    ifcst = dt
    urls = []
    wtfiles = []
    wtfiles_int = []
    wtfiles_prof = []
    abs_validities = []
    zooms = []
    lon_corners = []
    lat_corners = []
    slon_sources = []
    slat_sources = []
    for analysis in datespan(first_analysis,eruption_stop,timedelta(hours=6)):
        year = str(analysis.year)
        month = "{:02d}".format(analysis.month)
        day = "{:02d}".format(analysis.day)
        hour = "{:02d}".format(analysis.hour)
        ianl = analysis.hour
        while ifcst < 6:
            ival = ianl + ifcst
            eruption_current = datetime(analysis.year,analysis.month,analysis.day,ival)
            if eruption_current > eruption_stop:
                break
            validity = "{:02d}".format(ival)
            fcst = "{:03d}".format(ifcst)
            month_validity = year + month
            day_validity = month_validity + day
            abs_validity = day_validity + validity
            elaborated_prof_file = 'profile_data_' + abs_validity + '.txt'
            elaborated_prof_file_path = os.path.join(data_folder,elaborated_prof_file)
            print('Checking if ' + elaborated_prof_file + ' exists in ' + data_folder)
            print(elaborated_prof_file_path,os.path.isfile(elaborated_prof_file_path))
            if os.path.isfile(elaborated_prof_file_path):
                print('File ' + elaborated_prof_file + ' already available in ' + data_folder)
                ifcst = ifcst + 1
                continue
            data_folder = os.path.join(cwd,'raw_reanalysis_weather_data_'+ day_validity + '/')
            wtfile_dwnl = 'gfs.t' + hour + 'z.pgrb2.0p25.f' + fcst
            wtfile = 'weather_data_' + year + month + day + hour + '_' + fcst
            wtfile_path = os.path.join(data_folder,wtfile)
            wtfile_int = 'weather_data_interpolated_' + year + month + day + hour + '_' + fcst
            wtfile_prof = 'profile_' + year + month + day + hour + validity + '.txt'
            url1 = 'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?file=' + wtfile_dwnl + '&all_lev=on&var_HGT=on&var_TMP=on&var_UGRD=on&var_VGRD=on&subregion=&leftlon=' + slon_source_left + '&rightlon=' + slon_source_right + '&toplat=' + slat_source_top + '&bottomlat=' + slat_source_bottom + '&dir=%2Fgfs.' + year + month + day + '%2F' + hour
            url2 = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + year + month + day + '/' + hour + '/' + wtfile_dwnl
            print('Checking if ' + wtfile + ' exists')
            if os.path.isfile(wtfile_path):
                print('File ' + wtfile + ' found')
                copyfile(wtfile_path, wtfile)
            else:
                try:
                    try:
                        url = url1
                        urllib.request.urlopen(url)
                        zoom = False
                    except:
                        url = url2
                        urllib.request.urlopen(url)
                        zoom = True
                except:
                    try:
                        new_analysis = analysis - timedelta(hours=6)
                        new_ifcst = ifcst + 6
                        new_year = str(new_analysis.year)
                        new_month = "{:02d}".format(new_analysis.month)
                        new_day = "{:02d}".format(new_analysis.day)
                        new_hour = "{:02d}".format(new_analysis.hour)
                        ianl_new = new_analysis.hour
                        ival_new = ianl_new + new_ifcst
                        validity = "{:02d}".format(ival_new)
                        fcst = "{:03d}".format(new_ifcst)
                        month_validity = new_year + new_month
                        day_validity = month_validity + new_day
                        abs_validity = day_validity + validity
                        elaborated_prof_file = 'profile_data_' + abs_validity + '.txt'
                        elaborated_prof_file_path = os.path.join(data_folder, elaborated_prof_file)
                        print('Checking if ' + elaborated_prof_file + ' exists in ' + data_folder)
                        if os.path.isfile(elaborated_prof_file_path):
                            print('File ' + elaborated_prof_file + ' already available in ' + data_folder)
                            continue
                        data_folder = os.path.join(cwd, 'raw_reanalysis_weather_data_' + day_validity + '/')
                        wtfile_dwnl = 'gfs.t' + new_hour + 'z.pgrb2.0p25.f' + fcst
                        wtfile = 'weather_data_' + new_year + new_month + new_day + new_hour + '_' + fcst
                        wtfile_int = 'weather_data_interpolated_' + new_year + new_month + new_day + new_hour + '_' + fcst
                        wtfile_prof = 'profile_' + new_year + new_month + new_day + new_hour + validity + '.txt'
                        url1 = 'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?file=' + wtfile_dwnl + '&all_lev=on&var_HGT=on&var_TMP=on&var_UGRD=on&var_VGRD=on&subregion=&leftlon=' + slon_source_left + '&rightlon=' + slon_source_right + '&toplat=' + slat_source_top + '&bottomlat=' + slat_source_bottom + '&dir=%2Fgfs.' + new_year + new_month + new_day + '%2F' + new_hour
                        url2 = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.' + new_year + new_month + new_day + '/' + new_hour + '/' + wtfile_dwnl
                        try:
                            url = url1
                            urllib.request.urlopen(url)
                            zoom = False
                        except:
                            url = url2
                            urllib.request.urlopen(url)
                            zoom = True
                    except:
                        print('GFS data not available. Retrying with ERA5')
                        return False
                urls.append(url)
                wtfiles.append(wtfile)
                wtfiles_int.append(wtfile_int)
                wtfiles_prof.append(wtfile_prof)
                abs_validities.append(abs_validity)
                zooms.append(zoom)
                lon_corners.append(lon_corner)
                lat_corners.append(lat_corner)
                slon_sources.append(slon_source)
                slat_sources.append(slat_source)
            ifcst = ifcst + 1
        ifcst = 0
    try:
        pool = ThreadingPool(len(wtfiles))
        pool.map(wtfile_download, urls, wtfiles)
    except:
        print('No new weather data downloaded')
    if len(wtfiles) > 0:
        pool_1 = ThreadingPool(len(wtfiles))
        pool_1.map(elaborate_wtfiles, wtfiles, wtfiles_int, wtfiles_prof, abs_validities, zooms, lon_corners,
                   lat_corners, slon_sources, slat_sources)

    return (True)
