"""
*** satellite_radiance v1.0 ***
- component of the weather package included in REFIR 20.0 -
- Script to estimate top plume height from radiance in the channel 10.8 micron

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

def satellite_radiance_refir(profile_data_files_path,year,month,day,hour,minute,volc_lat,volc_lon):
    # Import the "gdal" and "gdal_array" submodules from within the "osgeo" module
    from osgeo import gdal #If the code works, include in the conda environment
    from osgeo import gdal_array #If the code works, include in the conda environment
    import numpy as np
    import utm #If the code works, include in the conda environment
    import string
    import os
    import datetime
    import math

    c1 = 1.19096e8 #W m-2 sr-1 um4
    c2 = 1.43879e4 #um K
    wave_length = 10.8 #um

    def extract_volc_position(volc_lat,volc_lon,header_file):

        def vincenty(a, f, point1, point2, miles=False):
            """
            Vincenty's formula (inverse method) to calculate the distance (in
            kilometers or miles) between two points on the surface of a spheroid
            """
            MILES_PER_KILOMETER = 0.621371
            MAX_ITERATIONS = 200
            CONVERGENCE_THRESHOLD = 1e-12
            # Modified to get a and f as input and then calculate b
            f = 1 / f
            b = (1 - f) * a

            # short-circuit coincident points
            if point1[0] == point2[0] and point1[1] == point2[1]:
                return 0.0

            U1 = math.atan((1 - f) * math.tan(math.radians(point1[0])))
            U2 = math.atan((1 - f) * math.tan(math.radians(point2[0])))
            L = math.radians(point2[1] - point1[1])
            Lambda = L

            sinU1 = math.sin(U1)
            cosU1 = math.cos(U1)
            sinU2 = math.sin(U2)
            cosU2 = math.cos(U2)

            for iteration in range(MAX_ITERATIONS):
                sinLambda = math.sin(Lambda)
                cosLambda = math.cos(Lambda)
                sinSigma = math.sqrt((cosU2 * sinLambda) ** 2 +
                                     (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
                if sinSigma == 0:
                    return 0.0  # coincident points
                cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
                sigma = math.atan2(sinSigma, cosSigma)
                sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
                cosSqAlpha = 1 - sinAlpha ** 2
                try:
                    cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
                except ZeroDivisionError:
                    cos2SigmaM = 0
                C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha))
                LambdaPrev = Lambda
                Lambda = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma *
                                                       (cos2SigmaM + C * cosSigma *
                                                        (-1 + 2 * cos2SigmaM ** 2)))
                if abs(Lambda - LambdaPrev) < CONVERGENCE_THRESHOLD:
                    break  # successful convergence
            else:
                return None  # failure to converge

            uSq = cosSqAlpha * (a ** 2 - b ** 2) / (b ** 2)
            A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
            B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
            deltaSigma = B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma *
                                                               (-1 + 2 * cos2SigmaM ** 2) - B / 6 * cos2SigmaM *
                                                               (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2SigmaM ** 2)))
            s = b * A * (sigma - deltaSigma)

            s /= 1000  # meters to kilometers
            print(s)
            if miles:
                s *= MILES_PER_KILOMETER  # kilometers to miles
            return round(s, 6)

        alphabet = string.ascii_uppercase
        alphabet_utm = []
        for i in range(len(alphabet)):
            if alphabet[i] != "I" and alphabet[i] != "O":
                alphabet_utm.append(alphabet[i])
    # Read hdr file for extracting the georeferencing point coordinates
        records1 = []
        hdr_file = open(header_file,"r",encoding="utf-8", errors="surrogateescape")
        for line in hdr_file:
            records1.append(line.split('='))
        for nline in range(len(records1)):
            if records1[nline][0] == 'map info ':
                map_info_line = nline
            else:
                nline += 1
        records2 = records1[map_info_line][1].split(', ')
        center_x_pixel = float(records2[1])
        center_y_pixel = float(records2[2])
        center_x_utm = float(records2[3])
        center_y_utm = float(records2[4])
        pixel_size_x = float(records2[5])
        pixel_size_y = float(records2[6])
        records3 = records1[map_info_line + 1][1].split('"')
        utm_zone_info = records3[1].split('_')[2]
        spheroid_info = records3[8].split(']]')
        spheroid_info = spheroid_info[0].split(',')
        a = float(spheroid_info[1])
        f = float(spheroid_info[2])

        if len(utm_zone_info) == 3:
            center_zone_number = int(utm_zone_info[:2])
            center_zone_letter = utm_zone_info[2:3]
        else:
            center_zone_number = int(utm_zone_info[:1])
            center_zone_letter = utm_zone_info[1:2]

        center_lat, center_lon = utm.to_latlon(center_x_utm,center_y_utm,center_zone_number,center_zone_letter)
        distance = vincenty(a,f,(center_lat,center_lon),(volc_lat,volc_lon)) * 1000
        lon_distance_vinc = vincenty(a,f,(volc_lat,center_lon),(volc_lat,volc_lon)) * 1000
        if volc_lon < center_lon:
            lon_distance_vinc = - lon_distance_vinc
        #lat_distance_vinc = vincenty(a,f,(center_lat,volc_lon),(volc_lat,volc_lon)) * 1000
        lat_distance_pitagora = math.sqrt(distance**2 - lon_distance_vinc ** 2)
        if volc_lat > center_lat:
            #lat_distance_vinc = - lat_distance_vinc
            lat_distance_pitagora = -lat_distance_pitagora

        nx_pixels = lon_distance_vinc / pixel_size_x
        #ny_pixels = lat_distance_vinc / pixel_size_y
        ny_pixels_pitagora = lat_distance_pitagora / pixel_size_y

        i_volc = int(round(center_y_pixel)) + ny_pixels_pitagora
        j_volc = int(round(center_x_pixel)) + nx_pixels

        return i_volc, j_volc

    def extract_min_rad(i_volc,j_volc,sat_file):
        # Function to extract the minimum value of the radiance in the area of interest and its position in the array
        # Open a GDAL dataset
        dataset = gdal.Open(sat_file, gdal.GA_ReadOnly)
        # Allocate our array using the first band's datatype
        image_datatype = dataset.GetRasterBand(1).DataType
        image = np.zeros((dataset.RasterYSize, dataset.RasterXSize, dataset.RasterCount),
                         dtype=gdal_array.GDALTypeCodeToNumericTypeCode(image_datatype))

        # Loop over all bands in dataset
        for b in range(dataset.RasterCount):
            # Remember, GDAL index is on 1, but Python is on 0 -- so we add 1 for our GDAL calls
            band = dataset.GetRasterBand(b + 1)
            # Read in the band's data into the third dimension of our array
            image[:, :, b] = band.ReadAsArray() #b=8 is our band of interest, TIR10.8

        # Extract values of radiance in the area of interest (10 * 10 pixels around the volcano location)
        radiance_volc_area = []
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if i_volc - 5 <= i <= i_volc + 5:
                    if j_volc - 5 <= j <= j_volc + 5:
                        radiance_volc_area.append([i, j, image[i,j,8]])

        # Find the minimum value and its location
        min_rad = 1000000000
        for k in range(len(radiance_volc_area)):
            if(radiance_volc_area[k][2]) <= min_rad:
                min_rad = radiance_volc_area[k][2]
                i_min_rad = radiance_volc_area[k][0]
                j_min_rad = radiance_volc_area[k][1]
        return i_min_rad, j_min_rad, min_rad

    def extract_heights(prof_file,t_rad):
        records1 = []
        tmp_k = []
        hgt = []
        with open(prof_file, 'r', encoding="utf-8", errors="surrogateescape") as f1:
            next(f1)
            nlines = 0
            for line in f1:
                nlines += 1
                records1.append(line.split('     '))
            for i in range(0, nlines):
                hgt.append(float(records1[i][0]))
                tmp_k.append(float(records1[i][2]))
        for i in range(nlines -1, 0, -1):
            if tmp_k[i-1] < t_rad < tmp_k[i]:
                slope = (hgt[i-1] - hgt[i])/(tmp_k[i-1] - tmp_k[i])
                q = hgt[i-1] - slope * tmp_k[i-1]
                height = slope * t_rad + q
                break
        t_rad_max = t_rad + 2
        for i in range(nlines -1, 0, -1):
            if tmp_k[i-1] < t_rad_max < tmp_k[i]:
                slope = (hgt[i - 1] - hgt[i]) / (tmp_k[i - 1] - tmp_k[i])
                q = hgt[i-1] - slope * tmp_k[i-1]
                height_min = slope * t_rad_max + q
                break
        t_rad_min = t_rad - 2
        for i in range(nlines -1, 0, -1):
            if tmp_k[i-1] < t_rad_min < tmp_k[i]:
                slope = (hgt[i - 1] - hgt[i]) / (tmp_k[i - 1] - tmp_k[i])
                q = hgt[i-1] - slope * tmp_k[i-1]
                height_max = slope * t_rad_min + q
                break
        return height, height_max, height_min

    year_s = str(year)
    if month < 10:
        month_s = '0' + str(month)
    else:
        month_s = str(month)
    if day < 10:
        day_s = '0' + str(day)
    else:
        day_s = str(day)
    if hour < 10:
        hour_s = '0' + str(hour)
    else:
        hour_s = str(hour)
    if minute < 10:
        minute_s = '0' + str(minute)
    else:
        minute_s = str(minute)

    time_now = year_s + month_s + day_s + hour_s + minute_s
    time_now_s = datetime.datetime.strptime(time_now,'%Y%m%d%H%M')
    weather_file_name = 'profile_data_' + year_s + month_s + day_s + hour_s + '.txt'
    profile_data_file = os.path.join(profile_data_files_path, weather_file_name)
    if not os.path.exists(profile_data_file):
        hour -= 1
        if hour < 10:
            hour_s = '0' + str(hour)
        else:
            hour_s = str(hour)
        weather_file_name = 'profile_data_' + year_s + month_s + day_s + hour_s + '.txt'
        profile_data_file = os.path.join(profile_data_files_path, weather_file_name)
        if not os.path.exists(profile_data_file):
            hour -= 1
            if hour < 10:
                hour_s = '0' + str(hour)
            else:
                hour_s = str(hour)
            weather_file_name = 'profile_data_' + year_s + month_s + day_s + hour_s + '.txt'
            profile_data_file = os.path.join(profile_data_files_path, weather_file_name)
            if not os.path.exists(profile_data_file):
                return
    satellite_folder = os.path.join(os.getcwd(),'satellite')
    files_list = os.listdir(satellite_folder)
    sat_files = []
    sat_hdr_files = []
    sat_times = []
    for file in files_list:
        if file[-3:] == 'hdr':
            file_full_path = os.path.join(satellite_folder, file)
            sat_hdr_files.append(file_full_path)
        elif file[0:7] == 'SEVIRI_':
            file_full_path = os.path.join(satellite_folder,file)
            sat_files.append(file_full_path)
            sat_time_i = file[-15:-7]+file[-6:-2]
            sat_time_s = datetime.datetime.strptime(sat_time_i, '%Y%m%d%H%M')
            sat_times.append(sat_time_s)
    i = 0
    for time in sat_times:
        time_delta = (time_now_s - time).total_seconds()
        # Only extract heights and update fix_OBSin.txt when the time now coincides with the time of the satellite retrieval
        if 0 <= time_delta < 300:
            i_volc, j_volc = extract_volc_position(volc_lat, volc_lon, sat_hdr_files[i])
            i_min_rad, j_min_rad, min_rad = extract_min_rad(i_volc, j_volc, sat_files[i])
            t_rad = c2 / wave_length / np.log((c1 / np.power(wave_length, 5.) / min_rad) + 1.)
            height, height_max, height_min = extract_heights(profile_data_file,t_rad)
            obs_flag = 1 # Flag to update the fix_OBSin file
            time_obs = datetime.datetime.strftime(time, '%m %d %Y %H:%M:%S')
            return time_obs, height, height_max, height_min, obs_flag
        else:
            i += 1
    time_obs = 'NA'
    height = 0
    height_min = 0
    height_max = 0
    obs_flag = 0
    return time_obs, height, height_max, height_min, obs_flag



