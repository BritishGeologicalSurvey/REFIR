"""
*** radar_converter v1.0 ***
- component of REFIR 20.0 -
- Script to convert IMO radar files into REFIR-readable files -

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

def retrieve_icelandic_radar(volc_id):
    from datetime import datetime,date,timedelta
    import urllib.request
    import urllib.error
    global file_name,val_date,year,month,day,hour
    now = str(datetime.utcnow())
    yesterday = str(date.today() - timedelta(1))
    year_now = now[0:4]
    month_now = now[5:7]
    day_now = now[8:10]
    hour_now = now[11:13]
    minute_now = now[14:16]
    secs_now = now[17:19]
    year_yst = yesterday[0:4]
    month_yst = yesterday[5:7]
    day_yst = yesterday[8:10]
    hour_yst = yesterday[11:13]

    if volc_id == 0:
        volc_name = 'eyjaf'
    elif volc_id == 1:
        volc_name = 'katla'
    elif volc_id == 2:
        volc_name =  'hekla'
    elif volc_id == 3:
        volc_name = 'grims'
    elif volc_id == 4:
        volc_name = 'vestm'
    elif volc_id == 5:
        volc_name = 'barda'
    elif volc_id == 6:
        volc_name = 'kverk'
    elif volc_id == 7:
        volc_name = 'oraef'
    elif volc_id == 8:
        volc_name = 'askja'
    elif volc_id == 9 or volc_id == 10:
        volc_name = 'keili'
    else:
        volc_name = 'ovaent'

    url_dir = 'http://brunnur.vedur.is/radar/vespa/' + volc_name + '/'
    try:
        urllib.request.urlopen(url_dir)
    except urllib.error.HTTPError as e:
        print('Volcano folder not available')
    except urllib.error.URLError as e:
        print('Volcano folder not available')

    year = year_now
    month = month_now
    day = day_now
    val_date = year + '-' + month + '-' + day
    hour = hour_now
    try:
        file_name = 'eht_' + volc_name + '_' + year + '-' + month + '-' + day + '.txt'
        url = url_dir + file_name
        print('Downloading file ' + file_name + ' from ' + url_dir)
        urllib.request.urlretrieve(url, file_name)
    except urllib.error.HTTPError as e:
        print('File not yet available. Retrieving the previous one')
        # Retrieve yesterday files, just in case they contain usable data (e.g. data very close to midnight and time now
        # is shortly after midnight
        year = year_yst
        month = month_yst
        day = day_yst
        hour = hour_yst
        try:
            file_name = 'eht_' + volc_name + '_' + year + '-' + month + '-' + day + '.txt'
            url = url_dir + file_name
            print('Downloading file ' + file_name + ' from ' + url_dir)
            urllib.request.urlretrieve(url, file_name)
        except urllib.error.HTTPError as e:
            print('No usable data available')

def process_radar_file():
    # Create files that can be read by REFIR
    records = []
    records_time = []
    val_time = []
    radar_type = []
    # Keflavik
    H1_iskef = []
    H2_iskef = []
    H_avg_iskef = []
    time_iskef = []
    hour_iskef = []
    minute_iskef = []
    # X-Band 1
    H1_isx1 = []
    H2_isx1 = []
    H_avg_isx1 = []
    time_isx1 = []
    hour_isx1 = []
    minute_isx1 = []
    # X-Band 2
    H1_isx2 = []
    H2_isx2 = []
    H_avg_isx2 = []
    time_isx2 = []
    hour_isx2 = []
    minute_isx2 = []
    # Egilsstadir
    H1_isegs = []
    H2_isegs = []
    H_avg_isegs = []
    time_isegs = []
    hour_isegs = []
    minute_isegs = []

    nrecords = 0
    nrecords_iskef = 0
    nrecords_isx1 = 0
    nrecords_isx2 = 0
    nrecords_isegs = 0


    # Function for extracting the two heights from the records
    def search_value(record):
        global heights
        heights = []
        for k in range(2, len(record)):
            if record[k]:
                heights.append(float(record[k]))

    try:
        file = open(file_name,encoding="utf-8", errors="surrogateescape")
        for line in file:
            nrecords += 1
            records.append(line.split(' '))

        # Extract heights for each radar type
        for i in range(1, nrecords):
            val_time.append(records[i][0].split('_'))
            radar_type.append(records[i][1])
            if radar_type[i-1] == 'iskef':
                nrecords_iskef += 1
                time_iskef.append(val_time[i-1][1])
                search_value(records[i])
                H1_iskef.append(heights[0])
                H2_iskef.append(heights[1])
            elif radar_type[i-1] == 'isx1':
                nrecords_isx1 += 1
                time_isx1.append(val_time[i-1][1])
                search_value(records[i])
                H1_isx1.append(heights[0])
                H2_isx1.append(heights[1])
            elif radar_type[i-1] == 'isx2':
                nrecords_isx2 += 1
                time_isx2.append(val_time[i-1][1])
                search_value(records[i])
                H1_isx2.append(heights[0])
                H2_isx2.append(heights[1])
            else:
                nrecords_isegs += 1
                time_isegs.append(val_time[i-1][1])
                search_value(records[i])
                H1_isegs.append(heights[0])
                H2_isegs.append(heights[1])

        for j in range(0, max(nrecords_iskef,nrecords_isx1,nrecords_isx2,nrecords_isegs)):
            if j < nrecords_iskef and nrecords_iskef != 0:
                #H_avg_iskef.append(0.5 * (H1_iskef[j] + H2_iskef[j]))
                H_avg_iskef.append((0.5 * (H1_iskef[j] + H2_iskef[j]))/1000)
                hour_iskef.append(time_iskef[j][0:2])
                minute_iskef.append(time_iskef[j][3:5])
            if j < nrecords_isx1 and nrecords_isx1 != 0:
                #H_avg_isx1.append(0.5 * (H1_isx1[j] + H2_isx1[j]))
                H_avg_isx1.append((0.5 * (H1_isx1[j] + H2_isx1[j]))/1000)
                hour_isx1.append(time_isx1[j][0:2])
                minute_isx1.append(time_isx1[j][3:5])
            if j < nrecords_isx2 and nrecords_isx2 != 0:
                #H_avg_isx2.append(0.5 * (H1_isx2[j] + H2_isx2[j]))
                H_avg_isx2.append((0.5 * (H1_isx2[j] + H2_isx2[j]))/1000)
                hour_isx2.append(time_isx2[j][0:2])
                minute_isx2.append(time_isx2[j][3:5])
            if j < nrecords_isegs and nrecords_isegs != 0:
                #H_avg_isegs.append(0.5 * (H1_isegs[j] + H2_isegs[j]))
                H_avg_isegs.append((0.5 * (H1_isegs[j] + H2_isegs[j]))/1000)
                hour_isegs.append(time_isegs[j][0:2])
                minute_isegs.append(time_isegs[j][3:5])

        with open('radar_iskef.txt','w',encoding="utf-8", errors="surrogateescape") as f_iskef, open('radar_isx1.txt','w',encoding="utf-8", errors="surrogateescape") as f_isx1, open('radar_isx2.txt','w',encoding="utf-8", errors="surrogateescape") as f_isx2, open('radar_isegs.txt','w',encoding="utf-8", errors="surrogateescape") as f_isegs:
            f_iskef.write('Date       Time     Year Mo  D Hr Mn Height\n\n')
            f_isx1.write('Date       Time     Year Mo  D Hr Mn Height\n\n')
            f_isx2.write('Date       Time     Year Mo  D Hr Mn Height\n\n')
            f_isegs.write('Date       Time     Year Mo  D Hr Mn Height\n\n')

            for j in range(0, max(nrecords_iskef,nrecords_isx1,nrecords_isx2,nrecords_isegs)):
                if j < nrecords_iskef and nrecords_iskef != 0:
                    f_iskef.write('{0:10s} {1:8s} {2:4s} {3:2s} {4:2s} {5:2s} {6:2s}  {7:3.1f}\n'.format(val_date, time_iskef[j], year, month, day, hour_iskef[j], minute_iskef[j], H_avg_iskef[j]))
                if j < nrecords_isx1 and nrecords_isx1 != 0:
                    f_isx1.write('{0:10s} {1:8s} {2:4s} {3:2s} {4:2s} {5:2s} {6:2s}  {7:3.1f}\n'.format(val_date, time_isx1[j], year, month, day, hour_isx1[j], minute_isx1[j], H_avg_isx1[j]))
                if j < nrecords_isx2 and nrecords_isx2 != 0:
                    f_isx2.write('{0:10s} {1:8s} {2:4s} {3:2s} {4:2s} {5:2s} {6:2s}  {7:3.1f}\n'.format(val_date, time_isx2[j], year, month, day, hour_isx2[j], minute_isx2[j], H_avg_isx2[j]))
                if j < nrecords_isegs and nrecords_isegs != 0:
                    f_isegs.write('{0:10s} {1:8s} {2:4s} {3:2s} {4:2s} {5:2s} {6:2s}  {7:3.1f}\n'.format(val_date, time_isegs[j], year, month, day, hour_isegs[j], minute_isegs[j], H_avg_isegs[j]))
    except:
        print("File " + file_name + " not found")
