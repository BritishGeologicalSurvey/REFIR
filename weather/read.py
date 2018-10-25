# -*- coding: utf-8 -*-
"""
*** read v1.0 ***
- component of the weather package included in REFIR 19.0 -
- Script to extract the weather data profile above the eruptive source from GFS and ERA-Interim data -

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


def extract_data_gfs(year, month, day, validity, wtfile_prof_step):
    from calc_wt_par import weather_parameters
    file = open(wtfile_prof_step, "r",encoding="utf-8", errors="surrogateescape")
    records1 = []
    records2 = []
    values = []
    nrecords = 0
    for line in file:
        nrecords += 1
        records1.append(line.split(':'))
        records2.append(line.split('val='))
    level = []
    u_tmp = []
    v_tmp = []
    hgt_tmp = []
    tmp_k_tmp = []
    mb_tmp = []
    u = []
    v = []
    wind = []
    hgt = []
    tmp_k = []
    tmp_c = []
    mb = []
    p = []
    i = 0
    while i < nrecords - 1:
        level = records1[i][4]
        if level[-2:] == 'mb':
            if records1[i][3] == 'UGRD':
                u_tmp.append(records2[i][1])
                mb_tmp.append(records1[i][4].split(' '))
            elif records1[i][3] == 'VGRD':
                v_tmp.append(records2[i][1])
            elif records1[i][3] == 'HGT':
                hgt_tmp.append(records2[i][1])
            elif records1[i][3] == 'TMP':
                tmp_k_tmp.append(records2[i][1])
        elif level == '2 m above ground':
            if records1[i][3] == 'TMP':
                tmp_k_tmp.append(records2[i][1])
                hgt_tmp.append('2')
        elif level == '10 m above ground':
            if records1[i][3] == 'UGRD':
                u_tmp.append(records2[i][1])
                mb_tmp.append(records1[i][4].split(' '))
            elif records1[i][3] == 'VGRD':
                v_tmp.append(records2[i][1])
        i += 1
    for i in range(0, len(u_tmp)):
        u.append(float(u_tmp[i]))
        v.append(float(v_tmp[i]))
        wind.append((u[i] ** 2 + v[i] ** 2) ** 0.5)
        hgt.append(float(hgt_tmp[i]))
        tmp_k.append(float(tmp_k_tmp[i]))
        tmp_c.append(tmp_k[i] - 273.15)
        mb.append(float(mb_tmp[i][0]))
        p.append(mb[i] * 100)
    p[len(u_tmp) - 1] = 100000
    prof_file = 'profile_data_' + validity + '.txt'
    wt_output = open(prof_file, 'w',encoding="utf-8", errors="surrogateescape")
    wt_output.write('  HGT[m]         P[Pa]       T[K]       T[C]     U[m/s]     V[m/s]  WIND[m/s]\n')

    for i in range(0, len(u)):
        wt_output.write('%8.2f %13.2f %10.2f %10.2f %10.2f %10.2f %10.2f\n' % (
        hgt[i], p[i], tmp_k[i], tmp_c[i], u[i], v[i], wind[i]))
    wt_output.close()
    # Elaborate data and save relevant weather parameter
    # weather_parameters(year, month, day, validity, prof_file) This call will be done by FOXI for each plume height value


def extract_data_erain(year, month, day, validity, wtfile_prof_step):
    from calc_wt_par import weather_parameters
    file = open(wtfile_prof_step, "r",encoding="utf-8", errors="surrogateescape")
    records1 = []
    records2 = []
    values = []
    nrecords = 0
    for line in file:
        nrecords += 1
        records1.append(line.split(':'))
        records2.append(line.split('val='))
    level = []
    u_tmp = []
    v_tmp = []
    hgt_tmp = []
    tmp_k_tmp = []
    mb_tmp = []
    u = []
    v = []
    wind = []
    hgt = []
    tmp_k = []
    tmp_c = []
    mb = []
    p = []
    i = 0
    while i < nrecords:
        if records1[i][3] == 'UGRD':
            u_tmp.append(records2[i][1])
            mb_tmp.append(records1[i][4].split(' '))
        elif records1[i][3] == 'VGRD':
            v_tmp.append(records2[i][1])
        elif records1[i][3] == 'GP':
            hgt_tmp.append(records2[i][1])
        elif records1[i][3] == 'TMP':
            tmp_k_tmp.append(records2[i][1])
        i += 1
    for i in range(0, len(u_tmp)):
        u.append(float(u_tmp[i]))
        v.append(float(v_tmp[i]))
        wind.append((u[i] ** 2 + v[i] ** 2) ** 0.5)
        hgt.append(float(hgt_tmp[i]) / 9.8066)
        tmp_k.append(float(tmp_k_tmp[i]))
        tmp_c.append(tmp_k[i] - 273.15)
        mb.append(float(mb_tmp[i][0]))
        p.append(mb[i] * 100)
    prof_file = 'profile_data_' + validity + '.txt'
    wt_output = open(prof_file, 'w',encoding="utf-8", errors="surrogateescape")
    wt_output.write('  HGT[m]         P[Pa]       T[K]       T[C]     U[m/s]     V[m/s]  WIND[m/s]\n')
    for i in range(0, len(u)):
        wt_output.write('%8.2f %13.2f %10.2f %10.2f %10.2f %10.2f %10.2f\n' % (
        hgt[i], p[i], tmp_k[i], tmp_c[i], u[i], v[i], wind[i]))
    wt_output.close()
    wind_trp = 0
    hgt_trp = 0
    # Elaborate data and save relevant weather parameter
     #weather_parameters(year, month, day, validity, prof_file)
