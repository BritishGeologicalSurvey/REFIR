"""
*** FIX v18.1 ***   
- component of REFIR 19.0 -
-control software and GUI for operating REFIR -
 
Copyright (C) 2018 Tobias Dürig, Fabio Dioguardi
================================

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

If you wish to contribute to the development of REFIR or to reports bugs or other problems with
the software, please write an email to me.

Contact: tobias.durig@otago.ac.nz, fabiod@bgs.ac.uk

RNZ22323I

"""
# tested on 27/01/2018
# Compatible for FOXI 18

from __future__ import division
from __future__ import with_statement
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
import time
import math
from copy import deepcopy
from mpl_toolkits.basemap import Basemap
import os

import sys

if sys.version_info[0] < 3:
    from Tkinter import *

else:
    from tkinter import *

runtype_weather = Tk()
weather = 1  # Default is automatic weather data retrieval
run_type = 1  # Default is real_time mode
quit_refir = IntVar()
#quit_refir.set(0) # FOXI continues until exit_param = 0
exit_param = 0

def calculate_position(self,x, y):
# Function that control the position of the widget in the screen
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    pos_x = x * screen_width
    pos_y = y * screen_height
    return (pos_x, pos_y)

def first_widget():
    global run_type_in, weather_in

    run_type_in = IntVar()
    weather_in = IntVar()
    run_type_in.set(1)
    weather_in.set(1)
    runtype_weather.title("REFIR Operation Mode")

    Label(runtype_weather, text="REFIR Operation Mode", font=("Verdana", 14, "bold"), fg="navy").grid(row=1, column=1,
                                                                                                      columnspan=4,
                                                                                                      sticky=W)
    Label(runtype_weather, text="Mode Selection", font=("Verdana", 10, "bold"), fg="navy").grid(row=2, column=1,
                                                                                                columnspan=2, sticky=W)

    Radiobutton(runtype_weather, text="Real Time", variable=run_type_in, value=1).grid(row=4, column=1, columnspan=2,
                                                                                       sticky=W)
    Radiobutton(runtype_weather, text="Reanalysis", variable=run_type_in, value=2).grid(row=5, column=1, columnspan=2,
                                                                                        sticky=W)

    Label(runtype_weather, text="Weather data", font=("Verdana", 10, "bold"), fg="navy").grid(row=2, column=4,
                                                                                              columnspan=2, sticky=W)

    Radiobutton(runtype_weather, text="Automatic Retrieve", variable=weather_in, value=1).grid(row=4, column=4,
                                                                                               columnspan=2, sticky=W)
    Radiobutton(runtype_weather, text="Manual entry", variable=weather_in, value=2).grid(row=5, column=4, columnspan=2,
                                                                                         sticky=W)

    x_screen_fr = 0.2
    y_screen_fr = 0.2
    size_x = 300
    size_y = 100
    pos_x, pos_y = calculate_position(runtype_weather,x_screen_fr, y_screen_fr)
    runtype_weather.geometry('%dx%d+%d+%d' % (size_x, size_y, pos_x, pos_y))
    runtype_weather.mainloop()


first_widget()
run_type = run_type_in.get()
weather = weather_in.get()

if run_type == 2:
    past_eruption = Tk()
    out = StringVar()

    def second_widget():
        past_eruption.title("Reanalysis mode control")
        Label(past_eruption, text="Specify start and end of eruption", \
              font="Helvetica 12", fg="blue").grid(row=0, column=0, columnspan=6)
        Label(past_eruption, text="Start of eruption: ", \
              font="Helvetica 11", fg="green").grid(row=5, column=0, columnspan=2, sticky=W)
        Label(past_eruption, text="Year: ", font="Helvetica 10").grid(row=5, column=2)
        Label(past_eruption, text="Month: ", font="Helvetica 10").grid(row=6, column=2)
        Label(past_eruption, text="Day: ", font="Helvetica 10").grid(row=6, column=0)
        Label(past_eruption, text="Hour: ", font="Helvetica 10").grid(row=7, column=0)
        Label(past_eruption, text="Minute: ", font="Helvetica 10").grid(row=7, column=2)
        Label(past_eruption, text="End of eruption: ", \
              font="Helvetica 11", fg="green").grid(row=9, column=0, columnspan=2, sticky=W)
        Label(past_eruption, text="Year: ", font="Helvetica 10").grid(row=9, column=2)
        Label(past_eruption, text="Month: ", font="Helvetica 10").grid(row=10, column=2)
        Label(past_eruption, text="Day: ", font="Helvetica 10").grid(row=10, column=0)
        Label(past_eruption, text="Hour: ", font="Helvetica 10").grid(row=11, column=0)
        Label(past_eruption, text="Minute: ", font="Helvetica 10").grid(row=11, column=2)

        time_ERU_start_y = Entry(past_eruption, width=4)
        time_ERU_start_y.grid(row=5, column=3, sticky=W)
        time_ERU_start_mo = Entry(past_eruption, width=2)
        time_ERU_start_mo.grid(row=6, column=3, sticky=W)
        time_ERU_start_d = Entry(past_eruption, width=2)
        time_ERU_start_d.grid(row=6, column=1, sticky=W)
        time_ERU_start_h = Entry(past_eruption, width=2)
        time_ERU_start_h.grid(row=7, column=1, sticky=W)
        time_ERU_start_m = Entry(past_eruption, width=2)
        time_ERU_start_m.grid(row=7, column=3, sticky=W)
        time_ERU_stop_y = Entry(past_eruption, width=4)
        time_ERU_stop_y.grid(row=9, column=3, sticky=W)
        time_ERU_stop_mo = Entry(past_eruption, width=2)
        time_ERU_stop_mo.grid(row=10, column=3, sticky=W)
        time_ERU_stop_d = Entry(past_eruption, width=2)
        time_ERU_stop_d.grid(row=10, column=1, sticky=W)
        time_ERU_stop_h = Entry(past_eruption, width=2)
        time_ERU_stop_h.grid(row=11, column=1, sticky=W)
        time_ERU_stop_m = Entry(past_eruption, width=2)
        time_ERU_stop_m.grid(row=11, column=3, sticky=W)

        def on_button():
            global time_start, time_stop, eruption_start, eruption_stop
            global Y_eru_start_s, MO_eru_start_s, D_eru_start_s
            global Y_eru_start, MO_eru_start, D_eru_start, H_eru_start
            global Y_eru_stop, MO_eru_stop, D_eru_stop, H_eru_stop
            Y_eru_start = int(time_ERU_start_y.get())
            MO_eru_start = int(time_ERU_start_mo.get())
            D_eru_start = int(time_ERU_start_d.get())
            H_eru_start = int(time_ERU_start_h.get())
            M_eru_start = int(time_ERU_start_m.get())
            Y_eru_stop = int(time_ERU_stop_y.get())
            MO_eru_stop = int(time_ERU_stop_mo.get())
            D_eru_stop = int(time_ERU_stop_d.get())
            H_eru_stop = int(time_ERU_stop_h.get())
            M_eru_stop = int(time_ERU_stop_m.get())
            Y_eru_start_s = str(Y_eru_start)
            if MO_eru_start < 10:
                MO_eru_start_s = '0' + str(MO_eru_start)
            else:
                MO_eru_start_s = str(MO_eru_start)
            print(D_eru_start)
            if D_eru_start < 10:
                D_eru_start_s = '0' + str(D_eru_start)
            else:
                D_eru_start_s = str(D_eru_start)
            if H_eru_start < 10:
                H_eru_start_s = '0' + str(H_eru_start)
            else:
                H_eru_start_s = str(H_eru_start)
            Y_eru_stop_s = str(Y_eru_stop)
            if MO_eru_stop < 10:
                MO_eru_stop_s = '0' + str(MO_eru_stop)
            else:
                MO_eru_stop_s = str(MO_eru_stop)
            if D_eru_stop < 10:
                D_eru_stop_s = '0' + str(D_eru_stop)
            else:
                D_eru_stop_s = str(D_eru_stop)
            if H_eru_stop < 10:
                H_eru_stop_s = '0' + str(H_eru_stop)
            else:
                H_eru_stop_s = str(H_eru_stop)
            eruption_start = Y_eru_start_s + MO_eru_start_s + D_eru_start_s + H_eru_start_s
            eruption_stop = Y_eru_stop_s + MO_eru_stop_s + D_eru_stop_s + H_eru_stop_s
            time_start = datetime.datetime(Y_eru_start, MO_eru_start, D_eru_start, H_eru_start, M_eru_start)
            time_stop = datetime.datetime(Y_eru_stop, MO_eru_stop, D_eru_stop, H_eru_stop, M_eru_stop)

        Button(past_eruption, text="Confirm times", font="Helvetica 11", fg="yellow", bg="red", \
               width=24, height=2, command=on_button).grid(row=14, column=0, columnspan=5)

        past_eruption.mainloop()

    second_widget()
else:
    time_start = '00-00-00 00:00:00'
    time_stop = '00-00-00 00:00:00'

#dir1 = os.path.dirname(__file__)
dir1 = os.path.dirname(os.path.abspath(__file__))
PlumeRiseFile = "PlumeRise_Foxi"
root = Tk()
x_screen_fr = 0.2
y_screen_fr = 0.2
size_x = 210
size_y = 350
pos_x, pos_y = calculate_position(root,x_screen_fr, y_screen_fr)
root.geometry('%dx%d+%d+%d' % (size_x, size_y, pos_x, pos_y))
root.title("select the volcano")
vulkan = 0
vulk = IntVar()
vulk.set(0)  # initializing the choice

try:
    label = ['n.a.', 'n.a.', 'n.a.', 'n.a.', 'n.a.', 'n.a.', 'n.a.', 'n.a.', 'n.a.', 'n.a.']
    volc_lat = []
    volc_lon = []
    kurzvulk = []
    defsetup = []
    fn = os.path.join(dir1 + '/refir_config', 'volcano_list.ini')
    with open(fn,encoding="utf-8", errors="surrogateescape") as f:
        lines = f.readlines()
        Cse = []
        for l in lines:
            Cse.append(l.strip().split("\t"))
    f.close()
    N_env = len(Cse) - 1  # number of entries
    if N_env < 1:
        print("\nNo volcano assigned!\n")
    else:
        for y in range(0, N_env):
            label.append(0)
            volc_lat.append(0)
            volc_lon.append(0)
            defsetup.append(0)
            kurzvulk.append("")
        for x in range(0, N_env):
            label[x] = str(Cse[x + 1][5])
            volc_lat[x] = float(Cse[x + 1][1])
            volc_lon[x] = float(Cse[x + 1][2])
            defsetup[x] = int(Cse[x + 1][4])
            kurzvulk[x] = str(Cse[x + 1][0])
    # file exists
except  EnvironmentError:
    # file does not exist yet
    print("Error -file volcano_list.ini not found!")

volcanoes = [(label[0], 0), (label[1], 1),
             (label[2], 2),
             (label[3], 3),
             (label[4], 4),
             (label[5], 5), (label[6], 6), (label[7], 7), (label[8], 8), (label[9], 9)]


def ShowChoiceVulk():
    print (vulk.get())
    global vulkan
    vulkan = vulk.get()


Label(root,
      text="""Select eruption site:""", font="Verdana 12 bold",
      justify=LEFT,
      padx=20).pack()

for txt, val in volcanoes:
    Radiobutton(root,
                text=txt, font="Helvetica 12",
                indicatoron=0,
                width=20,
                padx=20,
                variable=vulk,
                command=ShowChoiceVulk,
                value=val).pack(anchor=W)

mainloop()

time_update = datetime.datetime.utcnow()
print("**** REFIR FIX system is booting ****")
print("Selected volcano: ")
print(vulk.get())

ISKEF, ISEGS, ISX1, ISX2, GFZ1, GFZ2, GFZ3 = 0, 0, 0, 0, 0, 0, 0

fndb = os.path.join(dir1 + '/refir_config', 'volc_database.ini')
vent_h, dist_ISKEF, dist_ISEGS, dist_Cband3, dist_Cband4, dist_Cband5, dist_Cband6, \
dist_ISX1, dist_ISX2, dist_Xband3, dist_Xband4, dist_Xband5, dist_Xband6, dist_GFZ1, \
dist_GFZ2, dist_GFZ3, dist_Cam4, dist_Cam5, dist_Cam6 = \
    np.loadtxt(fndb, skiprows=2, usecols=(3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21),
               unpack=True, delimiter='\t')

try:
    defsetup = defsetup[vulkan]
    vent_h = vent_h[vulkan]
    dist_ISKEF = dist_ISKEF[vulkan]
    dist_ISEGS = dist_ISEGS[vulkan]
    dist_Cband3, dist_Cband4, dist_Cband5, dist_Cband6, dist_ISX1, dist_ISX2, \
    dist_Xband3, dist_Xband4, dist_Xband5, dist_Xband6, dist_GFZ1, \
    dist_GFZ2, dist_GFZ3, dist_Cam4, dist_Cam5, dist_Cam6 = \
        dist_Cband3[vulkan], dist_Cband4[vulkan], dist_Cband5[vulkan], dist_Cband6[vulkan], dist_ISX1[vulkan], \
        dist_ISX2[vulkan], \
        dist_Xband3[vulkan], dist_Xband4[vulkan], dist_Xband5[vulkan], dist_Xband6[vulkan], dist_GFZ1[vulkan], \
        dist_GFZ2[vulkan], dist_GFZ3[vulkan], dist_Cam4[vulkan], dist_Cam5[vulkan], dist_Cam6[vulkan]
except  IndexError:
    # only one entry
    huj = 0

# Note: if the automatic weather data option is chosen, some of these data will be overwritten at runtime (when using
# Degruyter&Bonadonna or Woodhouse model. The automatic weather data retrieval package will be called from these
# functions
P0 = 101325
P_0_in_default = P0 * math.exp(-vent_h / 7990)
P_0 = P_0_in_default
theta0_default = 1323
alpha_default = 0.1
beta_default = 0.5
theta_a0_default = 278
H1_default = 12000
H2_default = 20000
tempGrad_1_default = -0.0065
tempGrad_2_default = 0
tempGrad_3_default = 0.002
wfac_mod4_default = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
rho_dre_default = 2600
Vmax_default = 10
ki_default = 1.6

def safe_exit():
    global exit_param
    exit_param = 1
    save_default_file()
    print("Aborting FIX")
    print("FOXI will stop at next iteration")
    sys.exit()
    return(exit_param)

def automatic_weather():
    sys.path.insert(0, './weather')
    from weather import retrieve_data
    from retrieve_data import era_interim_retrieve
    from retrieve_data import gfs_forecast_retrieve
    from retrieve_data import gfs_past_forecast_retrieve
    import os
    from datetime import datetime, date, timedelta
    from shutil import move
    if run_type == 1:
        now = str(datetime.utcnow())
        year = now[0:4]
        month = now[5:7]
        day = now[8:10]
        gfs_forecast_retrieve(volc_lon[vulkan], volc_lat[vulkan])
        folder = 'raw_forecast_weather_data_' + year + month + day
    elif run_type == 2:
        print('Retrieving past GFS forecasts for the eruption interval')
        eruption_start_datetime = datetime(Y_eru_start, MO_eru_start, D_eru_start, H_eru_start)
        eruption_stop_datetime = datetime(Y_eru_stop, MO_eru_stop, D_eru_stop, H_eru_stop)
        response = gfs_past_forecast_retrieve(volc_lon[vulkan], volc_lat[vulkan], eruption_start_datetime,
                                   eruption_stop_datetime)
        if response == True:
            folder = 'raw_reanalysis_weather_data_' + Y_eru_start_s + MO_eru_start_s + D_eru_start_s
        else:
            print('GFS data not available.')
            print('Retrieving ERA Interim data')
            era_interim_retrieve(volc_lon[vulkan], volc_lat[vulkan], eruption_start, eruption_stop)
            folder = 'raw_reanalysis_weather_data_' + Y_eru_start_s + MO_eru_start_s + D_eru_start_s
    if not os.path.isdir(folder):
        os.makedirs(folder)
    current = os.getcwd()
    files = os.listdir(current)
    for file in files:
        if file.startswith('weather_') or file.startswith('profile_') or file.startswith('pressure_level'):
            print(file,folder)
            move(os.path.join(current,file),os.path.join(folder,file))

if weather == 1:
    automatic_weather()

qf_OBS = 4

timebase = -1

ID = ["n.a.", "n.a.", "n.a.", "n.a.", "n.a.", "n.a.", "n.a.", "n.a.", "n.a.", "n.a.", "n.a.", "n.a.", "n.a.", "n.a.",
      "n.a.", "n.a.", "n.a.", "n.a."]
sens_file = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
sens_IP = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
sens_dir = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
sens_url = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
N_en, N_en1, N_en2 = 0, 0, 0

loc_ISKEF = 0
loc_ISEGS = 0
loc_Cband4 = 0
loc_Cband5 = 0
loc_Cband6 = 0
loc_ISX1 = 0
loc_ISX2 = 0
loc_Xband3 = 0
loc_Xband4 = 0
loc_Xband5 = 0
loc_Xband6 = 0
loc_GFZ1 = 0
loc_GFZ2 = 0
loc_GFZ3 = 0
loc_Cam4 = 0
loc_Cam5 = 0
loc_Cam6 = 0


def read_sensors():
    """reads IDs and GPS coordinates from *.ini files"""
    global ID, sens_file, N_en, N_en1, N_en2, sens_url, sens_IP, sens_dir, Ase, sens_bwidth

    sens_bwidth = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    try:
        # C-band
        fnCb = os.path.join(dir1 + '/refir_config', 'Cband.ini')
        with open(fnCb, encoding="utf-8", errors="surrogateescape") as f:
            lines = f.readlines()
            Cse = []
            for l in lines:
                Cse.append(l.strip().split("\t"))
        f.close()
        N_en = len(Cse) - 1  # number of entries
        if N_en < 1:
            print("\nNo C-band radar sensors assigned!\n")
        else:
            for x in range(0, N_en):
                ID[x] = str(Cse[x + 1][0])
                sens_bwidth[x] = str(Cse[x + 1][5])
                sens_file[x] = str(Cse[x + 1][6])
                sens_url[x] = str(Cse[x + 1][7])
                if sens_url[x] == "":
                    sens_IP[x] = str(Cse[x + 1][8])
                    sens_dir[x] = str(Cse[x + 1][9])
                else:
                    sens_IP[x] = ""
                    sens_dir[x] = ""
    except  EnvironmentError:
        print("Error - \".ini\" sensor file not found!\n")

    try:
        # X-band
        fnXb = os.path.join(dir1 + '/refir_config', 'Xband.ini')
        with open(fnXb,encoding="utf-8", errors="surrogateescape") as f:
            lines = f.readlines()
            Dse = []
            for l in lines:
                Dse.append(l.strip().split("\t"))
        f.close()
        N_en2 = len(Dse) - 1  # number of entries
        if N_en2 < 1:
            print("\nNo X-band radar sensors assigned!\n")
        else:
            for x in range(0, N_en2):
                ID[x + 6] = str(Dse[x + 1][0])
                sens_bwidth[x + 6] = str(Dse[x + 1][5])
                sens_file[x + 6] = str(Dse[x + 1][6])
                sens_url[x + 6] = str(Dse[x + 1][7])
                if sens_url[x + 6] == "":
                    sens_IP[x + 6] = str(Dse[x + 1][8])
                    sens_dir[x + 6] = str(Dse[x + 1][9])
                else:
                    sens_IP[x + 6] = ""
                    sens_dir[x + 6] = ""
    except  EnvironmentError:
        print("Error - \".ini\" sensor file not found!\n")
    try:
        # Cams
        fnCam = os.path.join(dir1 + '/refir_config', 'Cam.ini')
        with open(fnCam,encoding="utf-8", errors="surrogateescape") as f:
            lines = f.readlines()
            Ase = []
            for l in lines:
                Ase.append(l.strip().split("\t"))
        f.close()
        N_en1 = len(Ase) - 1  # number of entries
        if N_en1 < 1:
            print("\nNo webcams assigned!\n")
        else:
            for x in range(0, N_en1):
                ID[x + 12] = str(Ase[x + 1][0])
                sens_file[x + 12] = str(Ase[x + 1][6])
                sens_url[x + 12] = str(Ase[x + 1][7])
                if sens_url[x + 12] == "":
                    sens_IP[x + 12] = str(Ase[x + 1][8])
                    sens_dir[x + 12] = str(Ase[x + 1][9])
                else:
                    sens_IP[x + 12] = ""
                    sens_dir[x + 12] = ""

    except  EnvironmentError:
        print("Error - \".ini\" sensor file not found!\n")


read_sensors()  # ID: array with sensor IDs [0-5]:Cband, [6-11]:Xband, [12-17]Cam


def get_last_time():
    global time_OBS
    try:

        config2file = open("fix_config.txt", "r",encoding="utf-8", errors="surrogateescape")
        config2lines = config2file.readlines()
        config2file.close()
        time_OBS_str0 = config2lines[2]
        time_OBS_str = time_OBS_str0[0:19]
        time_OBS = datetime.datetime.strptime(time_OBS_str, "%Y-%m-%d %H:%M:%S")
        checkfile = 11


    except EnvironmentError:
        checkfile = 10
        time_OBS = datetime.datetime(1979, 4, 30)


Hmin_obs_in = 0
Hmax_obs_in = 0


def defaultvalues(venth):
    """attributes default values to input parameters"""

    global P_0_in_default
    global theta_0
    global alpha
    global beta
    global theta_a0
    global H1
    global H2
    global tempGrad_1
    global tempGrad_2
    global tempGrad_3
    global wfac_mod4_default
    global wtf_wil
    global wtf_spa
    global wtf_mas
    global wtf_mtg
    global wtf_deg
    global wtf_wood0d

    global rho_dre
    global Vmax
    global ki
    global Hmin_obs
    global Hmax_obs
    global qf_OBS
    global time_OBS
    global analysis
    global timebase
    global ISKEF_on
    global ISEGS_on
    global ISX1_on
    global ISX2_on
    global ISKEFm_on
    global ISEGSm_on
    global ISX1m_on
    global ISX2m_on
    global GFZ1_on
    global GFZ2_on
    global GFZ3_on
    global OBS_on
    global oo_exp
    global oo_con
    global wtf_exp
    global wtf_con
    global oo_manual
    global wtf_manual
    global min_manMER
    global max_manMER
    global oo_wood
    global oo_RMER
    global wtf_wood
    global wtf_RMER
    global oo_isound
    global wtf_isound
    global oo_esens
    global wtf_esens
    global oo_pulsan
    global wtf_pulsan
    global oo_scatter
    global wtf_scatter
    global cal_ISKEF_a
    global cal_ISKEF_b
    global cal_ISEGS_a
    global cal_ISEGS_b
    global cal_ISX1_a
    global cal_ISX1_b
    global cal_ISX2_a
    global cal_ISX2_b
    global Hmin_obs_in
    global Hmax_obs_in
    global qf_obs
    global OBS1
    global P_0

    global PM_Nplot, PM_PHplot, PM_MERplot, PM_TME, PM_FMERplot, PM_FTME, StatusR_oo

    global Min_DiaOBS, Max_DiaOBS, pl_width_min, pl_width_max

    global Cband3_on, Cband4_on, Cband5_on, Cband6_on, Xband3_on, Xband4_on, \
        Xband5_on, Xband6_on, Cam4_on, Cam5_on, Cam6_on
    global Cband3m_on, Cband4m_on, Cband5m_on, Cband6m_on, Xband3m_on, Xband4m_on, \
        Xband5m_on, Xband6m_on, Cam4m_on, Cam5m_on, Cam6m_on
    global cal_Cband3a, cal_Cband3b, cal_Cband4a, cal_Cband4b, cal_Cband5a, cal_Cband5b, \
        cal_Cband6a, cal_Cband6b, cal_Xband3a, cal_Xband3b, cal_Xband4a, cal_Xband4b, \
        cal_Xband5a, cal_Xband5b, cal_Xband6a, cal_Xband6b

    P0 = 101325  # default ambient pressure at sea level
    P_0_in_default = P0 * math.exp(-venth / 7990)  # def. ambient pressure at vent
    P_0 = P_0_in_default
    theta_0 = 1323  # default magmatic temperature (K)
    alpha = 0.1  # def. radial entrainment coeff
    beta = 0.5  # def. wind entrainment coeff
    theta_a0 = 278  # default ambient temperature (K)
    H1 = 12000  # def. height tropopause a.s.l. (m)
    H2 = 20000  # def. height stratosphere a.s.l. (m)
    tempGrad_1 = -0.0065  # def. temp. grad. troposphere (K/m)
    tempGrad_2 = 0  # def. temp. grad. between tropo & stratosphere (K/m)
    tempGrad_3 = 0.002  # def. temp. grad. stratosphere (K/m)
    wfac_mod4_default = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]  # def. model weight factors
    wtf_wil = wfac_mod4_default[0]
    wtf_spa = wfac_mod4_default[1]
    wtf_mas = wfac_mod4_default[2]
    wtf_mtg = wfac_mod4_default[3]
    wtf_deg = wfac_mod4_default[4]
    wtf_wood0d = wfac_mod4_default[5]
    ki = 1.6  # default scale factor

    rho_dre = 2600  # default rock density
    Vmax = 10  # default max windspeed at tropopause (m/s)

    Hmin_obs = 0
    Hmax_obs = 0

    Min_DiaOBS = 0
    Max_DiaOBS = 0

    time_OBS = datetime.datetime(1979, 4, 30)
    analysis = 0
    timebase = -1

    ISKEF_on = 1
    ISEGS_on = 1
    ISX1_on = 1
    ISX2_on = 1
    ISKEFm_on = 1
    ISEGSm_on = 1
    ISX1m_on = 1
    ISX2m_on = 1
    GFZ1_on = 0
    GFZ2_on = 0
    GFZ3_on = 0
    OBS_on = 1

    oo_exp = 0
    oo_con = 1
    wtf_exp = 0
    wtf_con = 1

    oo_manual = 0
    wtf_manual = 0
    min_manMER = 0
    max_manMER = 0

    oo_wood = 0
    oo_RMER = 1
    wtf_wood = 0
    wtf_RMER = 1

    oo_isound = 0
    wtf_isound = 0
    oo_esens = 0
    wtf_esens = 0
    oo_pulsan = 0
    wtf_pulsan = 0
    oo_scatter = 0
    wtf_scatter = 0

    cal_ISKEF_a = 0
    cal_ISKEF_b = 1
    cal_ISEGS_a = 0
    cal_ISEGS_b = 1
    cal_ISX1_a = 0
    cal_ISX1_b = 1
    cal_ISX2_a = 0
    cal_ISX2_b = 1

    Hmin_obs_in = 0
    Hmax_obs_in = 0
    qf_obs = 0
    OBS1 = 1

    PM_Nplot = 1
    PM_PHplot = 1
    PM_MERplot = 1
    PM_TME = 1
    PM_FMERplot = 1
    PM_FTME = 1
    StatusR_oo = 1

    Cband3_on, Cband4_on, Cband5_on, Cband6_on, Xband3_on, Xband4_on, \
    Xband5_on, Xband6_on, Cam4_on, Cam5_on, Cam6_on, Cband3m_on, Cband4m_on, Cband5m_on, \
    Cband6m_on, Xband3m_on, Xband4m_on, Xband5m_on, Xband6m_on, Cam4m_on, Cam5m_on, Cam6m_on \
        = -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1

    cal_Cband3a, cal_Cband3b, cal_Cband4a, cal_Cband4b, cal_Cband5a, cal_Cband5b, \
    cal_Cband6a, cal_Cband6b, cal_Xband3a, cal_Xband3b, cal_Xband4a, cal_Xband4b, \
    cal_Xband5a, cal_Xband5b, cal_Xband6a, cal_Xband6b = 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1


V = vulkan + 1

IDC = []
LatC = []
LonC = []
try:
    fnCb = os.path.join(dir1 + '/refir_config', 'Cband.ini')
    with open(fnCb,encoding="utf-8", errors="surrogateescape") as f:
        lines = f.readlines()
        Cse = []
        for l in lines:
            Cse.append(l.strip().split("\t"))
    f.close()
    N_enc = len(Cse) - 1  # number of entries
    if N_enc < 1:
        print("\nNo C-band radar sensors assigned!\n")
    else:

        for y in range(0, N_enc):
            IDC.append(0)
            LatC.append(0)
            LonC.append(0)

        for x in range(0, N_enc):
            IDC[x] = str(Cse[x + 1][0])
            LatC[x] = float(Cse[x + 1][1])
            LonC[x] = float(Cse[x + 1][2])
    # file exists
except  EnvironmentError:
    # file does not exist yet
    print("\nCband.ini file not found!\n")

IDX = []
LatX = []
LonX = []

try:
    fnXb = os.path.join(dir1 + '/refir_config', 'Xband.ini')
    with open(fnXb,encoding="utf-8", errors="surrogateescape") as f:
        lines = f.readlines()
        Cse = []
        for l in lines:
            Cse.append(l.strip().split("\t"))
    f.close()
    N_enx = len(Cse) - 1  # number of entries
    if N_enx < 1:
        print("\nNo X-band radar sensors assigned!\n")
    else:
        for y in range(0, N_enx):
            IDX.append(0)
            LatX.append(0)
            LonX.append(0)
        for x in range(0, N_enx):
            IDX[x] = str(Cse[x + 1][0])
            LatX[x] = float(Cse[x + 1][1])
            LonX[x] = float(Cse[x + 1][2])
    # file exists
except  EnvironmentError:
    # file does not exist yet
    print("\nXband.ini file not found!\n")

IDCam = []
LatCam = []
LonCam = []

try:
    fnCam = os.path.join(dir1 + '/refir_config', 'Cam.ini')
    with open(fnCam,encoding="utf-8", errors="surrogateescape") as f:
        lines = f.readlines()
        Cse = []
        for l in lines:
            Cse.append(l.strip().split("\t"))
    f.close()
    N_enca = len(Cse) - 1  # number of entries
    if N_enca < 1:
        print("\nNo webcams assigned!\n")
    else:
        for y in range(0, N_enca):
            IDCam.append(0)
            LatCam.append(0)
            LonCam.append(0)
        for x in range(0, N_enca):
            IDCam[x] = str(Cse[x + 1][0])
            LatCam[x] = float(Cse[x + 1][1])
            LonCam[x] = float(Cse[x + 1][2])
    # file exists
except  EnvironmentError:
    # file does not exist yet
    print("\nCam.ini file not found!\n")

minlat = min(min(LatC or volc_lat), min(LatX or volc_lat), min(LatCam or volc_lat), min(volc_lat)) - 0.5
maxlat = max(max(LatC or volc_lat), max(LatX or volc_lat), max(LatCam or volc_lat), max(volc_lat)) + 0.5
minlon = min(min(LonC or volc_lon), min(LonX or volc_lon), min(LonCam or volc_lon), min(volc_lon)) - 0.5
maxlon = max(max(LonC or volc_lon), max(LonX or volc_lon), max(LonCam or volc_lon), max(volc_lon)) + 0.5


def checkbox_oo(oo_var):
    """returns True or False when called by an on/off switch"""
    if oo_var == 1:
        return True
    else:
        return False


def get_last_data():
    """reads default values from fix_config file if existing"""
    global P_0
    global theta_0
    global alpha
    global beta
    global theta_a0
    global H1
    global H2
    global tempGrad_1
    global tempGrad_2
    global tempGrad_3
    global wfac_mod4_default
    global rho_dre
    global Vmax, Vmax_default
    global ki
    global wtf_wil
    global wtf_spa
    global wtf_mas
    global wtf_mtg
    global wtf_deg
    global qf_OBS
    global time_OBS
    global analysis
    global timebase
    global ISKEF_on
    global ISEGS_on
    global ISX1_on
    global ISX2_on
    global ISKEFm_on
    global ISEGSm_on
    global ISX1m_on
    global ISX2m_on
    global GFZ1_on
    global GFZ2_on
    global GFZ3_on
    global OBS_on
    global oo_exp
    global oo_con
    global wtf_exp
    global wtf_con
    global oo_manual
    global wtf_manual
    global min_manMER
    global max_manMER
    global oo_wood
    global oo_RMER
    global wtf_wood
    global wtf_RMER
    global oo_isound
    global wtf_isound
    global oo_esens
    global wtf_esens
    global oo_pulsan
    global wtf_pulsan
    global oo_scatter
    global wtf_scatter
    global cal_ISKEF_a
    global cal_ISKEF_b
    global cal_ISEGS_a
    global cal_ISEGS_b
    global cal_ISX1_a
    global cal_ISX1_b
    global cal_ISX2_a
    global cal_ISX2_b
    global qf_obs
    global OBS1
    global PM_Nplot, PM_PHplot, PM_MERplot, PM_TME, PM_FMERplot, PM_FTME, StatusR_oo
    global pl_minw_default, pl_maxw_default
    global qfak_Cband3
    global qfak_Cband4, qfak_Cband5, qfak_Cband6, qfak_Xband3, qfak_Xband4, \
        qfak_Xband5, qfak_Xband6, qfak_Cam4, qfak_Cam5, qfak_Cam6, unc_Cband3, \
        unc_Cband4, unc_Cband5, unc_Cband6, unc_Xband3, unc_Xband4, unc_Xband5, unc_Xband6
    global Cband3_on, Cband4_on, Cband5_on, Cband6_on, Xband3_on, Xband4_on, \
        Xband5_on, Xband6_on, Cam4_on, Cam5_on, Cam6_on
    global Cband3m_on, Cband4m_on, Cband5m_on, Cband6m_on, Xband3m_on, Xband4m_on, \
        Xband5m_on, Xband6m_on, Cam4m_on, Cam5m_on, Cam6m_on
    global cal_Cband3a, cal_Cband3b, cal_Cband4a, cal_Cband4b, cal_Cband5a, cal_Cband5b, \
        cal_Cband6a, cal_Cband6b, cal_Xband3a, cal_Xband3b, cal_Xband4a, cal_Xband4b, \
        cal_Xband5a, cal_Xband5b, cal_Xband6a, cal_Xband6b
    global wtf_wood0d
    global time_start, time_stop

    try:

        configfile = open("fix_config.txt", "r",encoding="utf-8", errors="surrogateescape")
        configlines3 = configfile.readlines()
        configfile.close()
        checkfile = 1
        P_0 = float(configlines3[8])
        theta_0 = float(configlines3[9])
        alpha = float(configlines3[11])
        beta = float(configlines3[12])
        theta_a0 = float(configlines3[7])
        H1 = float(configlines3[18])
        H2 = float(configlines3[19])
        tempGrad_1 = float(configlines3[20])
        tempGrad_2 = float(configlines3[21])
        tempGrad_3 = float(configlines3[22])

        wfac_mod4_default[0] = float(configlines3[13])
        wfac_mod4_default[1] = float(configlines3[14])
        wfac_mod4_default[2] = float(configlines3[15])
        wfac_mod4_default[3] = float(configlines3[16])
        wfac_mod4_default[4] = float(configlines3[17])
        wfac_mod4_default[5] = float(configlines3[165])

        wtf_wil = wfac_mod4_default[0]
        wtf_spa = wfac_mod4_default[1]
        wtf_mas = wfac_mod4_default[2]
        wtf_mtg = wfac_mod4_default[3]
        wtf_deg = wfac_mod4_default[4]
        wtf_wood0d = wfac_mod4_default[5]

        rho_dre = float(configlines3[10])
        Vmax = float(configlines3[23])
        Vmax_default = Vmax
        ki = float(configlines3[24])

        qf_OBS = int(configlines3[6])
        ISKEF_on = int(configlines3[37])
        ISEGS_on = int(configlines3[38])
        ISX1_on = int(configlines3[39])
        ISX2_on = int(configlines3[40])
        GFZ1_on = int(configlines3[41])
        GFZ2_on = int(configlines3[42])
        GFZ3_on = int(configlines3[43])
        analysis = int(configlines3[44])
        timebase = int(configlines3[45])
        cal_ISKEF_a = float(configlines3[66])
        cal_ISKEF_b = float(configlines3[67])
        cal_ISEGS_a = float(configlines3[68])
        cal_ISEGS_b = float(configlines3[69])
        cal_ISX1_a = float(configlines3[70])
        cal_ISX1_b = float(configlines3[71])
        cal_ISX2_a = float(configlines3[72])
        cal_ISX2_b = float(configlines3[73])
        ISKEFm_on = int(configlines3[74])
        ISEGSm_on = int(configlines3[75])
        ISX1m_on = int(configlines3[76])
        ISX2m_on = int(configlines3[77])
        OBS_on = int(configlines3[5])
        oo_exp = int(configlines3[46])
        oo_con = int(configlines3[47])
        wtf_exp = float(configlines3[48])
        wtf_con = float(configlines3[49])
        oo_manual = int(configlines3[50])
        wtf_manual = float(configlines3[51])
        min_manMER = float(configlines3[52])
        max_manMER = float(configlines3[53])
        oo_wood = int(configlines3[54])
        oo_RMER = int(configlines3[55])
        wtf_wood = float(configlines3[56])
        wtf_RMER = float(configlines3[57])
        oo_isound = int(configlines3[58])
        wtf_isound = float(configlines3[59])
        oo_esens = int(configlines3[60])
        wtf_esens = float(configlines3[61])
        oo_pulsan = int(configlines3[62])
        wtf_pulsan = float(configlines3[63])
        oo_scatter = int(configlines3[64])
        wtf_scatter = float(configlines3[65])

        PM_Nplot = int(configlines3[78])
        PM_PHplot = int(configlines3[79])
        PM_MERplot = int(configlines3[80])
        PM_TME = int(configlines3[81])
        PM_FMERplot = int(configlines3[82])
        PM_FTME = int(configlines3[83])
        StatusR_oo = int(configlines3[84])
        pl_minw_default = float(configlines3[85])
        pl_maxw_default = float(configlines3[86])

        qfak_Cband3 = float(configlines3[87])
        qfak_Cband4 = float(configlines3[88])
        qfak_Cband5 = float(configlines3[89])
        qfak_Cband6 = float(configlines3[90])
        qfak_Xband3 = float(configlines3[91])
        qfak_Xband4 = float(configlines3[92])
        qfak_Xband5 = float(configlines3[93])
        qfak_Xband6 = float(configlines3[94])
        qfak_Cam4 = float(configlines3[95])
        qfak_Cam5 = float(configlines3[96])
        qfak_Cam6 = float(configlines3[97])
        unc_Cband3 = float(configlines3[98])
        unc_Cband4 = float(configlines3[99])
        unc_Cband5 = float(configlines3[100])
        unc_Cband6 = float(configlines3[101])
        unc_Xband3 = float(configlines3[102])
        unc_Xband4 = float(configlines3[103])
        unc_Xband5 = float(configlines3[104])
        unc_Xband6 = float(configlines3[105])
        Cband3_on = float(configlines3[106])
        Cband4_on = float(configlines3[107])
        Cband5_on = float(configlines3[108])
        Cband6_on = float(configlines3[109])
        Xband3_on = float(configlines3[110])
        Xband4_on = float(configlines3[111])
        Xband5_on = float(configlines3[112])
        Xband6_on = float(configlines3[113])
        Cam4_on = float(configlines3[114])
        Cam5_on = float(configlines3[115])
        Cam6_on = float(configlines3[116])
        Cband3m_on = float(configlines3[117])
        Cband4m_on = float(configlines3[118])
        Cband5m_on = float(configlines3[119])
        Cband6m_on = float(configlines3[120])
        Xband3m_on = float(configlines3[121])
        Xband4m_on = float(configlines3[122])
        Xband5m_on = float(configlines3[123])
        Xband6m_on = float(configlines3[124])
        Cam4m_on = float(configlines3[125])  # not used
        Cam5m_on = float(configlines3[126])  # not used
        Cam6m_on = float(configlines3[127])  # not used
        cal_Cband3a = float(configlines3[128])
        cal_Cband3b = float(configlines3[129])
        cal_Cband4a = float(configlines3[130])
        cal_Cband4b = float(configlines3[131])
        cal_Cband5a = float(configlines3[132])
        cal_Cband5b = float(configlines3[133])
        cal_Cband6a = float(configlines3[134])
        cal_Cband6b = float(configlines3[135])
        cal_Xband3a = float(configlines3[136])
        cal_Xband3b = float(configlines3[137])
        cal_Xband4a = float(configlines3[138])
        cal_Xband4b = float(configlines3[139])
        cal_Xband5a = float(configlines3[140])
        cal_Xband5b = float(configlines3[141])
        cal_Xband6a = float(configlines3[142])
        cal_Xband6b = float(configlines3[143])
        get_last_time()

    except EnvironmentError:
        checkfile = 0
        time_OBS = datetime.datetime(1979, 4, 30)
        defaultvalues(vent_h)


masterklick = Tk()


def save_default_file():
    time_update = datetime.datetime.utcnow()
    default_FILE = open("fix_config.txt", 'w',encoding="utf-8", errors="surrogateescape")
    default_FILE.write(str(vulkan) + " \n" + str(time_update) + " \n" + \
                       str(time_OBS) + "\n" + str(Hmin_obs) + " \n" + str(Hmax_obs) + \
                       " \n" + str(OBS_on) + " \n" + str(qf_OBS) + " \n" + str(theta_a0) + \
                       " \n" + str(P_0) + " \n" + str(theta_0) + " \n" + str(rho_dre) + " \n" + str(alpha) + \
                       " \n" + str(beta) + " \n" + str(wtf_wil) + " \n" + str(wtf_spa) + " \n" + str(wtf_mas) + \
                       " \n" + str(wtf_mtg) + " \n" + str(wtf_deg) + " \n" + str(H1) + " \n" + str(H2) + \
                       " \n" + str(tempGrad_1) + " \n" + str(tempGrad_2) + " \n" + str(tempGrad_3) + " \n" + \
                       str(Vmax) + " \n" + str(ki) + " \n" + str(qfak_ISKEF) + " \n" + str(qfak_ISEGS) + " \n" + \
                       str(qfak_ISX1) + " \n" + str(qfak_ISX2) + " \n" + str(qfak_GFZ1) + " \n" + str(qfak_GFZ2) + \
                       " \n" + str(qfak_GFZ3) + " \n" + str(unc_ISKEF) + " \n" + str(unc_ISEGS) + " \n" + \
                       str(unc_ISX1) + " \n" + str(unc_ISX2) + " \n" + str(vent_h) + " \n" + str(ISKEF_on) + " \n" \
                       + str(ISEGS_on) + " \n" + str(ISX1_on) + " \n" + str(ISX2_on) + " \n" + str(GFZ1_on) + \
                       " \n" + str(GFZ2_on) + " \n" + str(GFZ3_on) + " \n" + str(analysis) + " \n" + str(timebase) \
                       + " \n" + str(oo_exp) + " \n" + str(oo_con) + " \n" + str(wtf_exp) + " \n" + str(wtf_con) \
                       + " \n" + str(oo_manual) + " \n" + str(wtf_manual) + " \n" + str(min_manMER) + " \n" \
                       + str(max_manMER) + " \n" + str(oo_wood) + " \n" + str(oo_RMER) + " \n" + str(wtf_wood) + " \n" \
                       + str(wtf_RMER) + " \n" + str(oo_isound) + " \n" + str(wtf_isound) + " \n" + str(oo_esens) \
                       + " \n" + str(wtf_esens) + " \n" + str(oo_pulsan) + " \n" + str(wtf_pulsan) + " \n" \
                       + str(oo_scatter) + " \n" + str(wtf_scatter) + " \n" + str(cal_ISKEF_a) + \
                       " \n" + str(cal_ISKEF_b) + " \n" + str(cal_ISEGS_a) + " \n" + str(cal_ISEGS_b) \
                       + " \n" + str(cal_ISX1_a) + " \n" + str(cal_ISX1_b) + " \n" + str(cal_ISX2_a) + " \n" \
                       + str(cal_ISX2_b) + " \n" + str(ISKEFm_on) + " \n" + str(ISEGSm_on) + " \n" \
                       + str(ISX1m_on) + " \n" + str(ISX2m_on) + "\n" + str(PM_Nplot) + "\n" + str(PM_PHplot) + \
                       "\n" + str(PM_MERplot) + "\n" + str(PM_TME) + "\n" + str(PM_FMERplot) + "\n" + str(PM_FTME) \
                       + "\n" + str(StatusR_oo) + "\n" + str(Min_DiaOBS) + "\n" + str(Max_DiaOBS) \
                       + "\n" + str(qfak_Cband3) + "\n" + str(qfak_Cband4) + "\n" + str(qfak_Cband5) + "\n" + str(
        qfak_Cband6) \
                       + "\n" + str(qfak_Xband3) + "\n" + str(qfak_Xband4) + "\n" + str(qfak_Xband5) + "\n" + str(
        qfak_Xband6) \
                       + "\n" + str(qfak_Cam4) + "\n" + str(qfak_Cam5) + "\n" + str(qfak_Cam6) + "\n" + str(unc_Cband3) \
                       + "\n" + str(unc_Cband4) + "\n" + str(unc_Cband5) + "\n" + str(unc_Cband6) + "\n" + str(
        unc_Xband3) \
                       + "\n" + str(unc_Xband4) + "\n" + str(unc_Xband5) + "\n" + str(unc_Xband6) + "\n" + str(
        Cband3_on) \
                       + "\n" + str(Cband4_on) + "\n" + str(Cband5_on) + "\n" + str(Cband6_on) + "\n" + str(Xband3_on) \
                       + "\n" + str(Xband4_on) + "\n" + str(Xband5_on) + "\n" + str(Xband6_on) + "\n" + str(Cam4_on) \
                       + "\n" + str(Cam5_on) + "\n" + str(Cam6_on) + "\n" + str(Cband3m_on) + "\n" + str(Cband4m_on) \
                       + "\n" + str(Cband5m_on) + "\n" + str(Cband6m_on) + "\n" + str(Xband3m_on) + "\n" + str(
        Xband4m_on) \
                       + "\n" + str(Xband5m_on) + "\n" + str(Xband6m_on) + "\n" + str(Cam4m_on) + "\n" + str(Cam5m_on) \
                       + "\n" + str(Cam6m_on) + "\n" + str(cal_Cband3a) + "\n" + str(cal_Cband3b) + "\n" + str(
        cal_Cband4a) \
                       + "\n" + str(cal_Cband4b) + "\n" + str(cal_Cband5a) + "\n" + str(cal_Cband5b) + "\n" + str(
        cal_Cband6a) \
                       + "\n" + str(cal_Cband6b) + "\n" + str(cal_Xband3a) + "\n" + str(cal_Xband3b) + "\n" + str(
        cal_Xband4a) \
                       + "\n" + str(cal_Xband4b) + "\n" + str(cal_Xband5a) + "\n" + str(cal_Xband5b) \
                       + "\n" + str(cal_Xband6a) + "\n" + str(cal_Xband6b) \
                       + "\n" + str(loc_ISKEF) + "\n" + str(loc_ISEGS) \
                       + "\n" + str(loc_Cband3) + "\n" + str(loc_Cband4) + "\n" + str(loc_Cband5) + "\n" + str(
        loc_Cband6) \
                       + "\n" + str(loc_ISX1) + "\n" + str(loc_ISX2) \
                       + "\n" + str(loc_Xband3) + "\n" + str(loc_Xband4) + "\n" + str(loc_Xband5) + "\n" + str(
        loc_Xband6) \
                       + "\n" + str(loc_GFZ1) + "\n" + str(loc_GFZ2) + "\n" + str(loc_GFZ3) \
                       + "\n" + str(loc_Cam4) + "\n" + str(loc_Cam5) + "\n" + str(loc_Cam6) + "\n" + str(defsetup) \
                       + "\n" + str(run_type) + "\n" + str(weather) + "\n" + str(wtf_wood0d) + "\n" + str(time_start) \
                       + "\n" + str(time_stop)  + "\n" + str(exit_param))  # New variables in the config files for the run type and weather
    default_FILE.close()

defaultvalues(vent_h)


def GFZquality(distance):
    """assigns quality and uncertainties to data from GFZ camera sources"""
    if distance < 0:
        loc = -1
    else:
        loc = 1
    if distance == -999:
        qfak = 0
        qf = "OUT OF RANGE"
        qf_fg = "red"
        loc = 0
    elif distance == 9999:
        qfak = 0
        qf = "-- n.a. --"
        qf_fg = "rosybrown"
        loc = 0
    else:
        qfak = 1
        qf = "WITHIN RANGE"
        qf_fg = "lime green"
    return (qfak, qf, qf_fg, loc)


def Xradarquality(distance, beamwidth):
    """assigns quality and uncertainties to data from X-band radar sources"""
    if distance < 0:
        loc = -1
    else:
        loc = 1
    distance = abs(distance)
    fbeamwidth = float(beamwidth)
    unc = 0.5 * distance * np.tan(fbeamwidth * math.pi / 180)

    if distance < 60:
        qfak = 3
        qf = "WITHIN OPTIMAL RANGE"
        qf_fg = "lime green"

    elif distance < 120:
        qfak = 2
        qf = "WITHIN FAIR RANGE"
        qf_fg = "dark green"

    elif distance < 180:
        qfak = 1
        qf = "WITHIN LIMITED RANGE"
        qf_fg = "dark orange"

    elif distance == 9999:
        qfak = 0
        qf = "-- n.a. --"
        qf_fg = "rosybrown"
        unc = 99
        loc = 0
    else:
        qfak = 0
        qf = "OUT OF RANGE"
        qf_fg = "red"
        unc = 99
    return (qfak, qf, qf_fg, unc, loc)


def Cradarquality(distance, beamwidth):
    """assigns quality and uncertainties to data from C-band radar sources"""
    if distance < 0:
        loc = -1
    else:
        loc = 1
    distance = abs(distance)
    fbeamwidth = float(beamwidth)
    unc = 0.5 * distance * np.tan(fbeamwidth * math.pi / 180)

    if distance < 120:
        qfak = 3
        qf = "WITHIN OPTIMAL RANGE"
        qf_fg = "lime green"

    elif distance < 200:
        qfak = 2
        qf = "WITHIN FAIR RANGE"
        qf_fg = "dark green"

    elif distance < 255:
        qfak = 1
        qf = "WITHIN LIMITED RANGE"
        qf_fg = "dark orange"

    elif distance == 9999:
        qfak = 0
        qf = "-- n.a. --"
        qf_fg = "rosybrown"
        unc = 99
        loc = 0
    else:
        qfak = 0
        qf = "OUT OF RANGE"
        qf_fg = "red"
    return (qfak, qf, qf_fg, unc, loc)


def Cradarerror(distance, beamwidth):
    """assigns plume height uncertainties to data from C-band radar sources"""
    global err_plh
    """
    if distance <120:
        err_plh = 1000
    elif distance < 200:
        err_plh = 1500
    elif distance < 240:
        err_plh = 2000
    else:
        err_plh = 99999
    """
    distance = abs(distance)
    fbeamwidth = float(beamwidth)
    # err_plh = 0.5*distance*np.tan(fbeamwidth*math.pi/180)
    err_plh = 0.5 * distance * np.tan(fbeamwidth * math.pi / 180) * 1000  # Corrected to meters

    return (err_plh)


def Xradarerror(distance, beamwidth):
    """assigns plume height uncertainties to data from X-band radar sources"""
    global err_plh
    """
    if distance <65:
        err_plh = 1000
    elif distance < 120:
        err_plh = 1500
    elif distance < 180:
        err_plh = 2000
    else:
        err_plh = 99999
    """
    distance = abs(distance)
    fbeamwidth = float(beamwidth)
    # err_plh = 0.5*distance*np.tan(fbeamwidth*math.pi/180)
    err_plh = 0.5 * distance * np.tan(fbeamwidth * math.pi / 180) * 1000  # Corrected to meters
    print("distance is: " + str(distance))
    print("beamwidth is: " + str(beamwidth))
    print("UNCERTAINTY iS: " + str(err_plh))
    return (err_plh)


qfak_ISKEF = Cradarquality(dist_ISKEF, sens_bwidth[0])[0]
qf_ISKEF = Cradarquality(dist_ISKEF, sens_bwidth[0])[1]
qf_fg_ISKEF = Cradarquality(dist_ISKEF, sens_bwidth[0])[2]
unc_ISKEF = Cradarquality(dist_ISKEF, sens_bwidth[0])[3]
loc_ISKEF = Cradarquality(dist_ISKEF, sens_bwidth[0])[4]

qfak_ISEGS = Cradarquality(dist_ISEGS, sens_bwidth[1])[0]
qf_ISEGS = Cradarquality(dist_ISEGS, sens_bwidth[1])[1]
qf_fg_ISEGS = Cradarquality(dist_ISEGS, sens_bwidth[1])[2]
unc_ISEGS = Cradarquality(dist_ISEGS, sens_bwidth[1])[3]
loc_ISEGS = Cradarquality(dist_ISEGS, sens_bwidth[1])[4]

qfak_Cband3 = Cradarquality(dist_Cband3, sens_bwidth[2])[0]
qf_Cband3 = Cradarquality(dist_Cband3, sens_bwidth[2])[1]
qf_fg_Cband3 = Cradarquality(dist_Cband3, sens_bwidth[2])[2]
unc_Cband3 = Cradarquality(dist_Cband3, sens_bwidth[2])[3]
loc_Cband3 = Cradarquality(dist_Cband3, sens_bwidth[2])[4]

qfak_Cband4 = Cradarquality(dist_Cband4, sens_bwidth[3])[0]
qf_Cband4 = Cradarquality(dist_Cband4, sens_bwidth[3])[1]
qf_fg_Cband4 = Cradarquality(dist_Cband4, sens_bwidth[3])[2]
unc_Cband4 = Cradarquality(dist_Cband4, sens_bwidth[3])[3]
loc_Cband4 = Cradarquality(dist_Cband4, sens_bwidth[3])[4]

qfak_Cband5 = Cradarquality(dist_Cband5, sens_bwidth[4])[0]
qf_Cband5 = Cradarquality(dist_Cband5, sens_bwidth[4])[1]
qf_fg_Cband5 = Cradarquality(dist_Cband5, sens_bwidth[4])[2]
unc_Cband5 = Cradarquality(dist_Cband5, sens_bwidth[4])[3]
loc_Cband5 = Cradarquality(dist_Cband5, sens_bwidth[4])[4]

qfak_Cband6 = Cradarquality(dist_Cband6, sens_bwidth[5])[0]
qf_Cband6 = Cradarquality(dist_Cband6, sens_bwidth[5])[1]
qf_fg_Cband6 = Cradarquality(dist_Cband6, sens_bwidth[5])[2]
unc_Cband6 = Cradarquality(dist_Cband6, sens_bwidth[5])[3]
loc_Cband6 = Cradarquality(dist_Cband6, sens_bwidth[5])[4]

qfak_ISX1 = Xradarquality(dist_ISX1, sens_bwidth[6])[0]
qf_ISX1 = Xradarquality(dist_ISX1, sens_bwidth[6])[1]
qf_fg_ISX1 = Xradarquality(dist_ISX1, sens_bwidth[6])[2]
unc_ISX1 = Xradarquality(dist_ISX1, sens_bwidth[6])[3]
loc_ISX1 = Xradarquality(dist_ISX1, sens_bwidth[6])[4]

qfak_ISX2 = Xradarquality(dist_ISX2, sens_bwidth[7])[0]
qf_ISX2 = Xradarquality(dist_ISX2, sens_bwidth[7])[1]
qf_fg_ISX2 = Xradarquality(dist_ISX2, sens_bwidth[7])[2]
unc_ISX2 = Xradarquality(dist_ISX2, sens_bwidth[7])[3]
loc_ISX2 = Xradarquality(dist_ISX2, sens_bwidth[7])[4]

qfak_Xband3 = Xradarquality(dist_Xband3, sens_bwidth[8])[0]
qf_Xband3 = Xradarquality(dist_Xband3, sens_bwidth[8])[1]
qf_fg_Xband3 = Xradarquality(dist_Xband3, sens_bwidth[8])[2]
unc_Xband3 = Xradarquality(dist_Xband3, sens_bwidth[8])[3]
loc_Xband3 = Xradarquality(dist_Xband3, sens_bwidth[8])[4]

qfak_Xband4 = Xradarquality(dist_Xband4, sens_bwidth[9])[0]
qf_Xband4 = Xradarquality(dist_Xband4, sens_bwidth[9])[1]
qf_fg_Xband4 = Xradarquality(dist_Xband4, sens_bwidth[9])[2]
unc_Xband4 = Xradarquality(dist_Xband4, sens_bwidth[9])[3]
loc_Xband4 = Xradarquality(dist_Xband4, sens_bwidth[9])[4]

qfak_Xband5 = Xradarquality(dist_Xband5, sens_bwidth[10])[0]
qf_Xband5 = Xradarquality(dist_Xband5, sens_bwidth[10])[1]
qf_fg_Xband5 = Xradarquality(dist_Xband5, sens_bwidth[10])[2]
unc_Xband5 = Xradarquality(dist_Xband5, sens_bwidth[10])[3]
loc_Xband5 = Xradarquality(dist_Xband5, sens_bwidth[10])[4]

qfak_Xband6 = Xradarquality(dist_Xband6, sens_bwidth[11])[0]
qf_Xband6 = Xradarquality(dist_Xband6, sens_bwidth[11])[1]
qf_fg_Xband6 = Xradarquality(dist_Xband6, sens_bwidth[11])[2]
unc_Xband6 = Xradarquality(dist_Xband6, sens_bwidth[11])[3]
loc_Xband6 = Xradarquality(dist_Xband6, sens_bwidth[11])[4]

qfak_GFZ1 = GFZquality(dist_GFZ1)[0]
qf_GFZ1 = GFZquality(dist_GFZ1)[1]
qf_fg_GFZ1 = GFZquality(dist_GFZ1)[2]
loc_GFZ1 = GFZquality(dist_GFZ1)[3]

qfak_GFZ2 = GFZquality(dist_GFZ2)[0]
qf_GFZ2 = GFZquality(dist_GFZ2)[1]
qf_fg_GFZ2 = GFZquality(dist_GFZ2)[2]
loc_GFZ2 = GFZquality(dist_GFZ2)[3]

qfak_GFZ3 = GFZquality(dist_GFZ3)[0]
qf_GFZ3 = GFZquality(dist_GFZ3)[1]
qf_fg_GFZ3 = GFZquality(dist_GFZ3)[2]
loc_GFZ3 = GFZquality(dist_GFZ3)[3]

qfak_Cam4 = GFZquality(dist_Cam4)[0]
qf_Cam4 = GFZquality(dist_Cam4)[1]
qf_fg_Cam4 = GFZquality(dist_Cam4)[2]
loc_Cam4 = GFZquality(dist_Cam4)[3]

qfak_Cam5 = GFZquality(dist_Cam5)[0]
qf_Cam5 = GFZquality(dist_Cam5)[1]
qf_fg_Cam5 = GFZquality(dist_Cam5)[2]
loc_Cam5 = GFZquality(dist_Cam5)[3]

qfak_Cam6 = GFZquality(dist_Cam6)[0]
qf_Cam6 = GFZquality(dist_Cam6)[1]
qf_fg_Cam6 = GFZquality(dist_Cam6)[2]
loc_Cam6 = GFZquality(dist_Cam6)[3]

save_default_file()


def gfz_vistable(gfz_v):
    """serves as legend for visibility of GFZ camera"""
    if gfz_v == -2:
        gfz_vis_str = "---"
        gfz_vis_fg = "rosybrown"
    elif gfz_v == 0:
        gfz_vis_str = "NO VISIBILITY"
        gfz_vis_fg = "red"
    elif gfz_v == 1:
        gfz_vis_str = "VERY LOW VISIBILITY"
        gfz_vis_fg = "dark orange"
    elif gfz_v == 2:
        gfz_vis_str = "RESTRICTED VISIBILITY"
        gfz_vis_fg = "gold"
    elif gfz_v == 3:
        gfz_vis_str = "FAIR VISIBILITY"
        gfz_vis_fg = "dark green"
    elif gfz_v == 4:
        gfz_vis_str = "CLEAR VIEW"
        gfz_vis_fg = "lime green"
    else:
        gfz_vis_str = "OFFLINE"
        gfz_vis_fg = "red"
    return (gfz_vis_str, gfz_vis_fg)


def entfernung(dist):
    """returns distance and sector indicator"""
    entfernung = ["", "", "black"]
    if dist == 9999:
        entfernung[0] = "---"
        entfernung[1] = "--"
        entfernung[2] = "black"
    elif dist == -999:
        entfernung[0] = "---"
        entfernung[1] = "--"
        entfernung[2] = "black"
    elif dist > 0:
        entfernung[0] = str(dist)
        entfernung[1] = "E"
        entfernung[2] = "red"
    else:
        entfernung[0] = str(abs(dist))
        entfernung[1] = "W"
        entfernung[2] = "blue"
    return (entfernung)


def SourceStatOview():
    global gfz3_images, gfz3_vis, gfz3_havg, gfz3_hstd, gfz1_images, gfz1_vis, gfz1_havg, gfz1_hstd, \
        gfz2_images, gfz2_vis, gfz2_havg, gfz2_hstd, gfz1_con, gfz2_con, gfz3_con, iskef_status, iskef_status, \
        iskef_con, iskef_status_fg, isegs_con, isegs_status, isegs_status_fg, isx1_con, isx1_status, isx1_status_fg, isx2_con, isx2_status, isx2_status_fg
    global cam4_con, cam4_images, cam4_vis, cam4_havg, cam4_hstd, cam5_con, cam5_images, cam5_vis, cam5_havg, cam5_hstd, \
        cam6_con, cam6_images, cam6_vis, cam6_havg, cam6_hstd, cband3_con, cband3_images, cband3_vis, cband3_havg, cband3_hstd, \
        cband4_con, cband4_images, cband4_vis, cband4_havg, cband4_hstd, cband5_con, cband5_images, cband5_vis, cband5_havg, cband5_hstd, \
        cband6_con, cband6_images, cband6_vis, cband6_havg, cband6_hstd, xband3_con, xband3_images, xband3_vis, xband3_havg, xband3_hstd, \
        xband4_con, xband4_images, xband4_vis, xband4_havg, xband4_hstd, xband5_con, xband5_images, xband5_vis, xband5_havg, xband5_hstd, \
        xband6_con, xband6_images, xband6_vis, xband6_havg, xband6_hstd
    global ID, sens_file, file_gfz1, file_gfz2, file_gfz3, file_cam4, file_cam5, file_cam6, file_iskef, file_isegs, file_cband3, \
        file_cband4, file_cband5, file_cband6, file_xband3, file_xband4, file_xband5, file_xband6, file_isx1, file_isx2
    global cam4_images, cam4_vis, cam4_havg, cam4_hstd, cam5_images, cam5_vis, cam5_havg, cam5_hstd, \
        cam6_images, cam6_vis, cam6_havg, cam6_hstd, cam5_con, cam6_con, cam4_con, cband3_status, cband3_status, \
        cband3_con, cband3_status_fg, cband4_con, cband4_status, cband4_status_fg, cband5_con, cband5_status, cband5_status_fg, cband6_con, cband6_status, cband6_status_fg
    global xband3_status, xband3_status, xband3_con, xband3_status_fg, xband4_con, \
        xband4_status, xband4_status_fg, xband5_con, xband5_status, xband5_status_fg, xband6_con, xband6_status, xband6_status_fg

    if sens_file[12] == "":
        gfz1_con = 0
        gfz1_images = -1
        gfz1_vis = -2
        gfz1_havg = 0
        gfz1_hstd = 0
    else:
        file_gfz1 = sens_file[12] + ".txt"
        try:
            with open(file_gfz1,encoding="utf-8", errors="surrogateescape") as f:
                rlines = []
                for line in f:
                    rlines.append(line)
                f.close()
                if len(rlines) == 1:
                    gfz1_images, gfz1_vis, gfz1_havg, gfz1_hstd = np.loadtxt(file_gfz1, usecols=(2, 3, 4, 5),
                                                                             unpack=True, delimiter='\t')
                    gfz1_con = 1

                else:
                    gfz1_images, gfz1_vis, gfz1_havg, gfz1_hstd = np.loadtxt(file_gfz1, usecols=(2, 3, 4, 5),
                                                                             unpack=True, delimiter='\t')
                    gfz1_con = 1
                    gfz1_images = gfz1_images[-1]
                    gfz1_vis = gfz1_vis[-1]
                    gfz1_havg = gfz1_havg[-1]
                    gfz1_hstd = gfz1_hstd[-1]

        except EnvironmentError:
            gfz1_con = 0
            gfz1_images = -1
            gfz1_vis = -1
            gfz1_havg = 0
            gfz1_hstd = 0

    if sens_file[13] == "":
        gfz2_con = 0
        gfz2_images = -1
        gfz2_vis = -2
        gfz2_havg = 0
        gfz2_hstd = 0
    else:
        file_gfz2 = sens_file[13] + ".txt"
        try:
            with open(file_gfz2,encoding="utf-8", errors="surrogateescape") as f:
                rlines = []
                for line in f:
                    rlines.append(line)
                f.close()
                if len(rlines) == 1:
                    gfz2_images, gfz2_vis, gfz2_havg, gfz2_hstd = np.loadtxt(file_gfz2, usecols=(2, 3, 4, 5),
                                                                             unpack=True, delimiter='\t')
                    gfz2_con = 1

                else:
                    gfz2_images, gfz2_vis, gfz2_havg, gfz2_hstd = np.loadtxt(file_gfz2, usecols=(2, 3, 4, 5),
                                                                             unpack=True, delimiter='\t')
                    gfz2_con = 1
                    gfz2_images = gfz2_images[-1]
                    gfz2_vis = gfz2_vis[-1]
                    gfz2_havg = gfz2_havg[-1]
                    gfz2_hstd = gfz2_hstd[-1]

        except EnvironmentError:
            gfz2_con = 0
            gfz2_images = -1
            gfz2_vis = -1
            gfz2_havg = 0
            gfz2_hstd = 0

    if sens_file[14] == "":
        gfz3_con = 0
        gfz3_images = -1
        gfz3_vis = -2
        gfz3_havg = 0
        gfz3_hstd = 0
    else:
        file_gfz3 = sens_file[14] + ".txt"
        try:
            with open(file_gfz3,encoding="utf-8", errors="surrogateescape") as f:
                rlines = []
                for line in f:
                    rlines.append(line)
                f.close()
                if len(rlines) == 1:
                    gfz3_images, gfz3_vis, gfz3_havg, gfz3_hstd = np.loadtxt(file_gfz3, usecols=(2, 3, 4, 5),
                                                                             unpack=True, delimiter='\t')
                    gfz3_con = 1
                else:
                    gfz3_images, gfz3_vis, gfz3_havg, gfz3_hstd = np.loadtxt(file_gfz3, usecols=(2, 3, 4, 5),
                                                                             unpack=True, delimiter='\t')
                    gfz3_con = 1
                    gfz3_images = gfz3_images[-1]
                    gfz3_vis = gfz3_vis[-1]
                    gfz3_havg = gfz3_havg[-1]
                    gfz3_hstd = gfz3_hstd[-1]
        except EnvironmentError:
            gfz3_con = 0
            gfz3_images = -1
            gfz3_vis = -1
            gfz3_havg = 0
            gfz3_hstd = 0

    if sens_file[15] == "":
        cam4_con = 0
        cam4_images = -1
        cam4_vis = -2
        cam4_havg = 0
        cam4_hstd = 0
    else:
        file_cam4 = sens_file[15] + ".txt"
        try:
            with open(file_cam4,encoding="utf-8", errors="surrogateescape") as f:
                rlines = []
                for line in f:
                    rlines.append(line)
                f.close()
                if len(rlines) == 1:
                    cam4_images, cam4_vis, cam4_havg, cam4_hstd = np.loadtxt(file_cam4, usecols=(2, 3, 4, 5),
                                                                             unpack=True, delimiter='\t')
                    cam4_con = 1
                else:
                    cam4_images, cam4_vis, cam4_havg, cam4_hstd = np.loadtxt(file_cam4, usecols=(2, 3, 4, 5),
                                                                             unpack=True, delimiter='\t')
                    cam4_con = 1
                    cam4_images = cam4_images[-1]
                    cam4_vis = cam4_vis[-1]
                    cam4_havg = cam4_havg[-1]
                    cam4_hstd = cam4_hstd[-1]
        except EnvironmentError:
            cam4_con = 0
            cam4_images = -1
            cam4_vis = -1
            cam4_havg = 0
            cam4_hstd = 0

    if sens_file[16] == "":
        cam5_con = 0
        cam5_images = -1
        cam5_vis = -2
        cam5_havg = 0
        cam5_hstd = 0
    else:
        file_cam5 = sens_file[16] + ".txt"
        try:
            with open(file_cam5,encoding="utf-8", errors="surrogateescape") as f:
                rlines = []
                for line in f:
                    rlines.append(line)
                f.close()
                if len(rlines) == 1:
                    cam5_images, cam5_vis, cam5_havg, cam5_hstd = np.loadtxt(file_cam5, usecols=(2, 3, 4, 5),
                                                                             unpack=True, delimiter='\t')
                    cam5_con = 1
                else:
                    cam5_images, cam5_vis, cam5_havg, cam5_hstd = np.loadtxt(file_cam5, usecols=(2, 3, 4, 5),
                                                                             unpack=True, delimiter='\t')
                    cam5_con = 1
                    cam5_images = cam5_images[-1]
                    cam5_vis = cam5_vis[-1]
                    cam5_havg = cam5_havg[-1]
                    cam5_hstd = cam5_hstd[-1]
        except EnvironmentError:
            cam5_con = 0
            cam5_images = -1
            cam5_vis = -1
            cam5_havg = 0
            cam5_hstd = 0

    if sens_file[17] == "":
        cam6_con = 0
        cam6_images = -1
        cam6_vis = -2
        cam6_havg = 0
        cam6_hstd = 0
    else:
        file_cam6 = sens_file[17] + ".txt"
        try:
            with open(file_cam6,encoding="utf-8", errors="surrogateescape") as f:
                rlines = []
                for line in f:
                    rlines.append(line)
                f.close()
                if len(rlines) == 1:
                    cam6_images, cam6_vis, cam6_havg, cam6_hstd = np.loadtxt(file_cam6, usecols=(2, 3, 4, 5),
                                                                             unpack=True, delimiter='\t')
                    cam6_con = 1
                else:
                    cam6_images, cam6_vis, cam6_havg, cam6_hstd = np.loadtxt(file_cam6, usecols=(2, 3, 4, 5),
                                                                             unpack=True, delimiter='\t')
                    cam6_con = 1
                    cam6_images = cam6_images[-1]
                    cam6_vis = cam6_vis[-1]
                    cam6_havg = cam6_havg[-1]
                    cam6_hstd = cam6_hstd[-1]
        except EnvironmentError:
            cam6_con = 0
            cam6_images = -1
            cam6_vis = -1
            cam6_havg = 0
            cam6_hstd = 0

    if sens_file[0] == "":
        iskef_con = 0
        iskef_status = "- n.a. -"
        iskef_status_fg = "rosybrown"
    else:
        file_iskef = sens_file[0] + ".txt"
        try:
            with open(file_iskef,encoding="utf-8", errors="surrogateescape") as f:
                iskef_con = 1
                iskef_status = "ONLINE"
                iskef_status_fg = "lime green"
        except EnvironmentError:
            iskef_con = 0
            iskef_status = "OFFLINE"
            iskef_status_fg = "red"

    if sens_file[1] == "":
        isegs_con = 0
        isegs_status = "- n.a. -"
        isegs_status_fg = "rosybrown"
    else:
        file_isegs = sens_file[1] + ".txt"
        try:
            with open(file_isegs,encoding="utf-8", errors="surrogateescape") as f:
                isegs_con = 1
                isegs_status = "ONLINE"
                isegs_status_fg = "lime green"
        except EnvironmentError:
            isegs_con = 0
            isegs_status = "OFFLINE"
            isegs_status_fg = "red"

    if sens_file[2] == "":
        cband3_con = 0
        cband3_status = "- n.a. -"
        cband3_status_fg = "rosybrown"
    else:
        file_cband3 = sens_file[2] + ".txt"
        try:
            with open(file_cband3,encoding="utf-8", errors="surrogateescape") as f:
                cband3_con = 1
                cband3_status = "ONLINE"
                cband3_status_fg = "lime green"
        except EnvironmentError:
            cband3_con = 0
            cband3_status = "OFFLINE"
            cband3_status_fg = "red"

    if sens_file[3] == "":
        cband4_con = 0
        cband4_status = "- n.a. -"
        cband4_status_fg = "rosybrown"
    else:
        file_cband4 = sens_file[3] + ".txt"
        try:
            with open(file_cband4,encoding="utf-8", errors="surrogateescape") as f:
                cband4_con = 1
                cband4_status = "ONLINE"
                cband4_status_fg = "lime green"
        except EnvironmentError:
            cband4_con = 0
            cband4_status = "OFFLINE"
            cband4_status_fg = "red"

    if sens_file[4] == "":
        cband5_con = 0
        cband5_status = "- n.a. -"
        cband5_status_fg = "rosybrown"
    else:
        file_cband5 = sens_file[4] + ".txt"
        try:
            with open(file_cband5,encoding="utf-8", errors="surrogateescape") as f:
                cband5_con = 1
                cband5_status = "ONLINE"
                cband5_status_fg = "lime green"
        except EnvironmentError:
            cband5_con = 0
            cband5_status = "OFFLINE"
            cband5_status_fg = "red"

    if sens_file[5] == "":
        cband6_con = 0
        cband6_status = "- n.a. -"
        cband6_status_fg = "rosybrown"
    else:
        file_cband6 = sens_file[5] + ".txt"
        try:
            with open(file_cband6,encoding="utf-8", errors="surrogateescape") as f:
                cband6_con = 1
                cband6_status = "ONLINE"
                cband6_status_fg = "lime green"
        except EnvironmentError:
            cband6_con = 0
            cband6_status = "OFFLINE"
            cband6_status_fg = "red"

    if sens_file[6] == "":
        isx1_con = 0
        isx1_status = "- n.a. -"
        isx1_status_fg = "rosybrown"
    else:
        file_isx1 = sens_file[6] + ".txt"
        try:
            with open(file_isx1,encoding="utf-8", errors="surrogateescape") as f:
                isx1_con = 1
                isx1_status = "ONLINE"
                isx1_status_fg = "lime green"
        except EnvironmentError:
            isx1_con = 0
            isx1_status = "OFFLINE"
            isx1_status_fg = "red"

    if sens_file[7] == "":
        isx2_con = 0
        isx2_status = "- n.a. -"
        isx2_status_fg = "rosybrown"
    else:
        file_isx2 = sens_file[7] + ".txt"
        try:
            with open(file_isx2,encoding="utf-8", errors="surrogateescape") as f:
                isx2_con = 1
                isx2_status = "ONLINE"
                isx2_status_fg = "lime green"
        except EnvironmentError:
            isx2_con = 0
            isx2_status = "OFFLINE"
            isx2_status_fg = "red"

    if sens_file[8] == "":
        xband3_con = 0
        xband3_status = "- n.a. -"
        xband3_status_fg = "rosybrown"
    else:
        file_xband3 = sens_file[8] + ".txt"
        try:
            with open(file_xband3,encoding="utf-8", errors="surrogateescape") as f:
                xband3_con = 1
                xband3_status = "ONLINE"
                xband3_status_fg = "lime green"
        except EnvironmentError:
            xband3_con = 0
            xband3_status = "OFFLINE"
            xband3_status_fg = "red"

    if sens_file[9] == "":
        xband4_con = 0
        xband4_status = "- n.a. -"
        xband4_status_fg = "rosybrown"
    else:
        file_xband4 = sens_file[9] + ".txt"
        try:
            with open(file_xband4,encoding="utf-8", errors="surrogateescape") as f:
                xband4_con = 1
                xband4_status = "ONLINE"
                xband4_status_fg = "lime green"
        except EnvironmentError:
            xband4_con = 0
            xband4_status = "OFFLINE"
            xband4_status_fg = "red"

    if sens_file[10] == "":
        xband5_con = 0
        xband5_status = "- n.a. -"
        xband5_status_fg = "rosybrown"
    else:
        file_xband5 = sens_file[10] + ".txt"
        try:
            with open(file_xband5,encoding="utf-8", errors="surrogateescape") as f:
                xband5_con = 1
                xband5_status = "ONLINE"
                xband5_status_fg = "lime green"
        except EnvironmentError:
            xband5_con = 0
            xband5_status = "OFFLINE"
            xband5_status_fg = "red"

    if sens_file[11] == "":
        xband6_con = 0
        xband6_status = "- n.a. -"
        xband6_status_fg = "rosybrown"
    else:
        file_xband6 = sens_file[11] + ".txt"
        try:
            with open(file_xband6,encoding="utf-8", errors="surrogateescape") as f:
                xband6_con = 1
                xband6_status = "ONLINE"
                xband6_status_fg = "lime green"
        except EnvironmentError:
            xband6_con = 0
            xband6_status = "OFFLINE"
            xband6_status_fg = "red"


SourceStatOview()


def PHSonoff():
    global ISKEF_on
    global ISEGS_on
    global ISX1_on
    global ISX2_on
    global ISKEFm_on
    global ISEGSm_on
    global ISX1m_on
    global ISX2m_on
    global GFZ1_on
    global GFZ2_on
    global GFZ3_on
    global OBS_on
    global Cband3_on, Cband4_on, Cband5_on, Cband6_on
    global Xband3_on, Xband4_on, Xband5_on, Xband6_on
    global Cam4_on, Cam5_on, Cam6_on
    global Cband3m_on, Cband4m_on, Cband5m_on, Cband6m_on
    global Xband3m_on, Xband4m_on, Xband5m_on, Xband6m_on

    ISKEF_on = int(ISKEF.get())
    ISEGS_on = int(ISEGS.get())
    ISX1_on = int(ISX1.get())
    ISX2_on = int(ISX2.get())
    ISKEFm_on = int(ISKEFm.get())
    ISEGSm_on = int(ISEGSm.get())
    ISX1m_on = int(ISX1m.get())
    ISX2m_on = int(ISX2m.get())
    GFZ1_on = int(GFZ1.get())
    GFZ2_on = int(GFZ2.get())
    GFZ3_on = int(GFZ3.get())
    OBS_on = int(OBSon.get())
    Cband3_on = int(Cband3.get())
    Cband4_on = int(Cband4.get())
    Cband5_on = int(Cband5.get())
    Cband6_on = int(Cband6.get())
    Cband3m_on = int(Cband3m.get())
    Cband4m_on = int(Cband4m.get())
    Cband5m_on = int(Cband5m.get())
    Cband6m_on = int(Cband6m.get())
    Xband3_on = int(Xband3.get())
    Xband4_on = int(Xband4.get())
    Xband5_on = int(Xband5.get())
    Xband6_on = int(Xband6.get())
    Xband3m_on = int(Xband3m.get())
    Xband4m_on = int(Xband4m.get())
    Xband5m_on = int(Xband5m.get())
    Xband6m_on = int(Xband6m.get())
    Cam4_on = int(Cam4.get())
    Cam5_on = int(Cam5.get())
    Cam6_on = int(Cam6.get())

    if sens_file[0] == "":
        ISKEF_on, ISKEFm_on = -1, -1
    else:
        nix = 0

    if sens_file[1] == "":
        ISEGS_on, ISEGSm_on = -1, -1
    else:
        nix = 0
    if sens_file[2] == "":
        Cband3_on, Cband3m_on = -1, -1
    else:
        nix = 0
    if sens_file[3] == "":
        Cband4_on, Cband4m_on = -1, -1
    else:
        nix = 0
    if sens_file[4] == "":
        Cband5_on, Cband5m_on = -1, -1
    else:
        nix = 0
    if sens_file[5] == "":
        Cband6_on, Cband6m_on = -1, -1
    else:
        nix = 0
    if sens_file[6] == "":
        ISX1_on, ISX1m_on = -1, -1
    else:
        nix = 0
    if sens_file[7] == "":
        ISX2_on, ISX2m_on = -1, -1
    else:
        nix = 0
    if sens_file[8] == "":
        Xband3_on, Xband3m_on = -1, -1
    else:
        nix = 0
    if sens_file[9] == "":
        Xband4_on, Xband4m_on = -1, -1
    else:
        nix = 0
    if sens_file[10] == "":
        Xband5_on, Xband5m_on = -1, -1
    else:
        nix = 0
    if sens_file[11] == "":
        Xband6_on, Xband6m_on = -1, -1
    else:
        nix = 0
    if sens_file[12] == "":
        GFZ1_on = -1
    else:
        nix = 0
    if sens_file[13] == "":
        GFZ2_on = -1
    else:
        nix = 0
    if sens_file[14] == "":
        GFZ3_on = -1
    else:
        nix = 0
    if sens_file[15] == "":
        Cam4_on = -1
    else:
        nix = 0
    if sens_file[16] == "":
        Cam5_on = -1
    else:
        nix = 0
    if sens_file[17] == "":
        Cam6_on = -1
    else:
        nix = 0

    print("*** settings updated! ***")
    save_default_file()
    check_configfile()


# MAP GENERATOR
def showmap():
    """shows and updates map"""

    global CS_oo, XS_oo, Cam_oo
    CS_oo = [-1, -1, -1, -1, -1, -1]  # -1: no sensor assigned, 0: off 1: on
    XS_oo = [-1, -1, -1, -1, -1, -1]  # -1: no sensor assigned, 0: off 1: on
    Cam_oo = [-1, -1, -1, -1, -1, -1]  # -1: no sensor assigned, 0: off 1: on
    CS_oo = [ISKEF_on, ISEGS_on, Cband3_on, Cband4_on, Cband5_on, Cband6_on]
    XS_oo = [ISX1_on, ISX2_on, Xband3_on, Xband4_on, Xband5_on, Xband6_on]
    Cam_oo = [GFZ1_on, GFZ2_on, GFZ3_on, Cam4_on, Cam5_on, Cam6_on]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    m = Basemap(resolution='h', projection='merc', llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=minlon,
                urcrnrlon=maxlon, lat_ts=20, epsg=3857)
    # resolution "f" for full

    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=2000, verbose=True)
    # m.drawcoastlines(color='blue')

    lat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    lon = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #for i in range(0, 10):
    for i in range(0, len(volc_lon)):
        lon[i], lat[i] = m(volc_lon[i], volc_lat[i])

    def volc_active(A, B, V):
        plt.plot(A, B, "r^", markersize=12)
        plt.annotate(label[V - 1],
                     xy=(A, B), xytext=(40, -30),
                     textcoords='offset points', ha='right', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                     arrowprops=dict(arrowstyle='->', lw="1", color="red", connectionstyle='arc3,rad=0'))

    def volc_inactive(A, B, V):
        plt.plot(A, B, "darkviolet", marker="^", markersize=10)

    idC = [0, 0, 0, 0, 0, 0]
    latC = [0, 0, 0, 0, 0, 0]
    lonC = [0, 0, 0, 0, 0, 0]

    idX = [0, 0, 0, 0, 0, 0]
    latX = [0, 0, 0, 0, 0, 0]
    lonX = [0, 0, 0, 0, 0, 0]

    idCam = [0, 0, 0, 0, 0, 0]
    latCam = [0, 0, 0, 0, 0, 0]
    lonCam = [0, 0, 0, 0, 0, 0]

    def CSens_active(A, B, S):
        plt.plot(A, B, "lime", marker="s", markersize=10)
        plt.annotate(S,
                     xy=(A, B), xytext=(-20, 20),
                     textcoords='offset points', ha='right', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', fc='lime', alpha=0.5),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    def CSens_inactive(A, B, S):
        plt.plot(A, B, "orange", marker="s", markersize=10)
        plt.annotate(S,
                     xy=(A, B), xytext=(-20, 20),
                     textcoords='offset points', ha='right', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', fc='orange', alpha=0.5),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    def XSens_active(A, B, S):
        plt.plot(A, B, "lime", marker="o", markersize=10)
        plt.annotate(S,
                     xy=(A, B), xytext=(-20, 20),
                     textcoords='offset points', ha='right', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', fc='lime', alpha=0.5),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    def XSens_inactive(A, B, S):
        plt.plot(A, B, "orange", marker="o", markersize=10)
        plt.annotate(S,
                     xy=(A, B), xytext=(-20, 20),
                     textcoords='offset points', ha='right', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', fc='orange', alpha=0.5),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    def CamSens_active(A, B, S):
        plt.plot(A, B, "lime", marker="*", markersize=10)
        plt.annotate(S,
                     xy=(A, B), xytext=(-20, 20),
                     textcoords='offset points', ha='right', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', fc='lime', alpha=0.5),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    def CamSens_inactive(A, B, S):
        plt.plot(A, B, "orange", marker="*", markersize=10)
        plt.annotate(S,
                     xy=(A, B), xytext=(-20, 20),
                     textcoords='offset points', ha='right', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', fc='orange', alpha=0.5),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    def volc_plot(V):
        global A1, B1
        #for q in range(0, 10):
        for q in range(0, len(lon)):
            if V == q + 1:
                volc_active(lon[q], lat[q], V)

            else:
                if lon[q] == 0:
                    print()
                else:
                    volc_inactive(lon[q], lat[q], V)

    def Cband_plot(cs_oo):
        #for h in range(0, 6):
        for h in range(0, len(LonC)):
            if cs_oo[h] == 1:
                lonC[h], latC[h] = m(LonC[h], LatC[h])
                CSens_active(lonC[h], latC[h], IDC[h])
            elif cs_oo[h] == 0:
                lonC[h], latC[h] = m(LonC[h], LatC[h])
                CSens_inactive(lonC[h], latC[h], IDC[h])
            else:
                None

    def Xband_plot(xs_oo):
        #for h in range(0, 6):
        for h in range(0, len(LonX)):
            if xs_oo[h] == 1:
                lonX[h], latX[h] = m(LonX[h], LatX[h])
                XSens_active(lonX[h], latX[h], IDX[h])
            elif xs_oo[h] == 0:
                lonX[h], latX[h] = m(LonX[h], LatX[h])
                XSens_inactive(lonX[h], latX[h], IDX[h])
            else:
                None

    def Cam_plot(cam_oo):
        #for h in range(0, 6):
        for h in range(0, len(LonCam)):
            if cam_oo[h] == 1:
                lonCam[h], latCam[h] = m(LonCam[h], LatCam[h])
                CamSens_active(lonCam[h], latCam[h], IDCam[h])
            if cam_oo[h] == 0:
                lonCam[h], latCam[h] = m(LonCam[h], LatCam[h])
                CamSens_inactive(lonCam[h], latCam[h], IDCam[h])
            else:
                None

    get_last_data()

    volc_plot(V)
    Cband_plot(CS_oo)
    Xband_plot(XS_oo)
    Cam_plot(Cam_oo)

    ax.annotate('sensors:', xy=(1, 0), xycoords='axes fraction', xytext=(-90, 44), textcoords='offset pixels',
                color='cyan', fontsize=14, horizontalalignment='left', verticalalignment='bottom')
    ax.annotate('switched on', xy=(1, 0), xycoords='axes fraction', xytext=(-90, 30), textcoords='offset pixels',
                color='lime', fontsize=14, horizontalalignment='left', verticalalignment='bottom')
    ax.annotate('switched off', xy=(1, 0), xycoords='axes fraction', xytext=(-90, 16), textcoords='offset pixels',
                color='orange', fontsize=14, horizontalalignment='left', verticalalignment='bottom')

    plt.gcf().set_size_inches(12, 12)
    plt.savefig('map1.png', bbox_inches='tight')
    plt.savefig('map1.svg', format='svg', dpi=300)
    # 1    plt.show()

    ma = Basemap(resolution='h', projection='merc', llcrnrlat=volc_lat[V - 1] - 0.4, urcrnrlat=volc_lat[V - 1] + 0.4,
                 llcrnrlon=volc_lon[V - 1] - 1, urcrnrlon=volc_lon[V - 1] + 1, lat_ts=20, epsg=3857)
    ma.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=2000, verbose=True)

    # ma.drawcoastlines(color='blue')

    def volc_plot2(V):
        #for q in range(0, 10):
        for q in range(0, len(lon2)):
            if V == q + 1:
                volc_active(lon2[q], lat2[q], V)
            else:
                if lon[q] == 0:
                    print()
                else:
                    volc_inactive(lon2[q], lat2[q], V)

    def Cband_plot2(cs_oo):
        #for h in range(0, 6):
        for h in range(0, len(LonC)):
            if cs_oo[h] == 1:
                lonC[h], latC[h] = ma(LonC[h], LatC[h])
                CSens_active(lonC[h], latC[h], IDC[h])
            elif cs_oo[h] == 0:
                lonC[h], latC[h] = ma(LonC[h], LatC[h])
                CSens_inactive(lonC[h], latC[h], IDC[h])
            else:
                None

    def Xband_plot2(xs_oo):
        #for h in range(0, 6):
        for h in range(0, len(LonX)):
            if xs_oo[h] == 1:
                lonX[h], latX[h] = ma(LonX[h], LatX[h])
                XSens_active(lonX[h], latX[h], IDX[h])
            elif xs_oo[h] == 0:
                lonX[h], latX[h] = ma(LonX[h], LatX[h])
                XSens_inactive(lonX[h], latX[h], IDX[h])
            else:
                None

    def Cam_plot2(cam_oo):
        #for h in range(0, 6):
        for h in range(0, len(LonCam)):
            if cam_oo[h] == 1:
                lonCam[h], latCam[h] = ma(LonCam[h], LatCam[h])
                CamSens_active(lonCam[h], latCam[h], IDCam[h])
            if cam_oo[h] == 0:
                lonCam[h], latCam[h] = ma(LonCam[h], LatCam[h])
                CamSens_inactive(lonCam[h], latCam[h], IDCam[h])
            else:
                None

    lat2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    lon2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 10):
        lon2[i], lat2[i] = ma(volc_lon[i], volc_lat[i])

    volc_plot2(V)

    Cband_plot2(CS_oo)
    Xband_plot2(XS_oo)
    Cam_plot2(Cam_oo)
    plt.gcf().set_size_inches(12, 10)
    plt.tight_layout()
    plt.savefig('map2.png', bbox_inches='tight')
    plt.savefig('map2.svg', format='svg', dpi=300)


# 1    plt.show()

# OUTPUT CONTROL PANEL
def plot_mode():
    global timebase
    get_last_data()

    def plot_modeset(kzl):
        if kzl == 0:
            menu_txt = "off"
        elif kzl == 1:
            menu_txt = "total"
        elif kzl == 2:
            menu_txt = "last 12h"
        elif kzl == 3:
            menu_txt = "last 6h"
        elif kzl == 4:
            menu_txt = "last 1h"
        else:
            menu_txt = "last 15min"
        return (menu_txt)

    plotmode = Toplevel()
    plotmode.title("Output control panel")

    Label(plotmode, text="Output settings", \
          font=("Verdana", 12, "bold"), fg="navy").grid(row=1, column=0, columnspan=5)

    Label(plotmode, text=" ", \
          font="Helvetica 11").grid(row=2, column=0, columnspan=5)

    Label(plotmode, text="- - - Plume height estimates - - -", \
          font="Helvetica 11", fg="green").grid(row=4, column=0, columnspan=5)

    Label(plotmode, text="- - - Model based estimates (CMER) - - -", \
          font="Helvetica 11", fg="blue").grid(row=8, column=0, columnspan=5)

    Label(plotmode, text="- - - Overall estimates (FMER) - - -", \
          font="Helvetica 11", fg="red4").grid(row=12, column=0, columnspan=5)

    Label(plotmode, text="   ", \
          font="Helvetica 11", fg="red4").grid(row=15, column=0)

    Label(plotmode, text="- - - Provide status report - - -", \
          font="Helvetica 11").grid(row=16, column=0, columnspan=5)

    statusR_o = IntVar()
    statusR_o.set(StatusR_oo)
    Radiobutton(plotmode, text="on", variable=statusR_o, value=1). \
        grid(row=17, column=3, sticky=E)
    Radiobutton(plotmode, text="off", variable=statusR_o, value=0). \
        grid(row=17, column=4, sticky=W)
    Label(plotmode, text=" ", \
          font="Helvetica 11").grid(row=18, column=0, columnspan=6)

    Label(plotmode, text="N-plot", font=("Verdana", 8, "bold"), fg="green"). \
        grid(row=5, column=0)

    PMvari_N = StringVar(plotmode)
    PMvari_N.set(plot_modeset(PM_Nplot))
    wn = OptionMenu(plotmode, PMvari_N, "off", "total", "last 12h", "last 6h", "last 1h", "last 15min")
    wn.grid(row=6, column=0)
    wn.config(width=12)
    Label(plotmode, text=" ", \
          font="Helvetica 11").grid(row=5, column=3)

    Label(plotmode, text="Plume height plot", font=("Verdana", 8, "bold"), fg="green"). \
        grid(row=5, column=4)

    PMvari_PH = StringVar(plotmode)
    PMvari_PH.set(plot_modeset(PM_PHplot))
    wPH = OptionMenu(plotmode, PMvari_PH, "off", "total", "last 12h", "last 6h", "last 1h", "last 15min")
    wPH.grid(row=6, column=4)
    wPH.config(width=12)
    Label(plotmode, text=" ", \
          font="Helvetica 11").grid(row=7, column=0, columnspan=6)

    Label(plotmode, text="CMER plot", font=("Verdana", 8, "bold"), fg="blue"). \
        grid(row=9, column=0)

    PMvari_MER = StringVar(plotmode)
    PMvari_MER.set(plot_modeset(PM_MERplot))
    wq = OptionMenu(plotmode, PMvari_MER, "off", "total", "last 12h", "last 6h", "last 1h", "last 15min")
    wq.grid(row=10, column=0)
    wq.config(width=12)
    Label(plotmode, text="Total mass erupted", font=("Verdana", 8, "bold"), fg="blue"). \
        grid(row=9, column=4)

    PMvari_TME = StringVar(plotmode)
    PMvari_TME.set(plot_modeset(PM_TME))
    wTME = OptionMenu(plotmode, PMvari_TME, "off", "total", "last 12h", "last 6h", "last 1h", "last 15min")
    wTME.grid(row=10, column=4)
    wTME.config(width=12)

    Label(plotmode, text=" ", \
          font="Helvetica 11").grid(row=11, column=0, columnspan=6)
    Label(plotmode, text="FMER plot", font=("Verdana", 8, "bold"), fg="red4"). \
        grid(row=13, column=0)

    PMvari_FMER = StringVar(plotmode)
    PMvari_FMER.set(plot_modeset(PM_FMERplot))
    wqF = OptionMenu(plotmode, PMvari_FMER, "off", "total", "last 12h", "last 6h", "last 1h", "last 15min")
    wqF.grid(row=14, column=0)
    wqF.config(width=12)
    Label(plotmode, text="Total mass erupted", font=("Verdana", 8, "bold"), fg="red4"). \
        grid(row=13, column=4)

    PMvari_FTME = StringVar(plotmode)
    PMvari_FTME.set(plot_modeset(PM_FTME))
    wFM = OptionMenu(plotmode, PMvari_FTME, "off", "total", "last 12h", "last 6h", "last 1h", "last 15min")
    wFM.grid(row=14, column=4)
    wFM.config(width=12)

    def plotmode_update():
        global PM_Nplot, PM_PHplot, PM_MERplot, PM_TME, PM_FMERplot, PM_FTME, StatusR_oo
        menu_N = str(PMvari_N.get())
        if menu_N == "off":
            PM_Nplot = 0
        elif menu_N == "total":
            PM_Nplot = 1
        elif menu_N == "last 12h":
            PM_Nplot = 2
        elif menu_N == "last 6h":
            PM_Nplot = 3
        elif menu_N == "last 1h":
            PM_Nplot = 4
        else:
            PM_Nplot = -1

        menu_PH = str(PMvari_PH.get())
        if menu_PH == "off":
            PM_PHplot = 0
        elif menu_PH == "total":
            PM_PHplot = 1
        elif menu_PH == "last 12h":
            PM_PHplot = 2
        elif menu_PH == "last 6h":
            PM_PHplot = 3
        elif menu_PH == "last 1h":
            PM_PHplot = 4
        else:
            PM_PHplot = -1

        menu_MER = str(PMvari_MER.get())
        if menu_MER == "off":
            PM_MERplot = 0
        elif menu_MER == "total":
            PM_MERplot = 1
        elif menu_MER == "last 12h":
            PM_MERplot = 2
        elif menu_MER == "last 6h":
            PM_MERplot = 3
        elif menu_MER == "last 1h":
            PM_MERplot = 4
        else:
            PM_MERplot = -1

        menu_TME = str(PMvari_TME.get())
        if menu_TME == "off":
            PM_TME = 0
        elif menu_TME == "total":
            PM_TME = 1
        elif menu_TME == "last 12h":
            PM_TME = 2
        elif menu_TME == "last 6h":
            PM_TME = 3
        elif menu_TME == "last 1h":
            PM_TME = 4
        else:
            PM_TME = -1

        menu_FMER = str(PMvari_FMER.get())
        if menu_FMER == "off":
            PM_FMERplot = 0
        elif menu_FMER == "total":
            PM_FMERplot = 1
        elif menu_FMER == "last 12h":
            PM_FMERplot = 2
        elif menu_FMER == "last 6h":
            PM_FMERplot = 3
        elif menu_FMER == "last 1h":
            PM_FMERplot = 4
        else:
            PM_FMERplot = -1

        menu_FTME = str(PMvari_FTME.get())
        if menu_FTME == "off":
            PM_FTME = 0
        elif menu_FTME == "total":
            PM_FTME = 1
        elif menu_FTME == "last 12h":
            PM_FTME = 2
        elif menu_FTME == "last 6h":
            PM_FTME = 3
        elif menu_FTME == "last 1h":
            PM_FTME = 4
        else:
            PM_FTME = -1

        StatusR_oo = int(statusR_o.get())

        save_default_file()
        print("*** settings updated! ***")
        check_configfile()

    Button(plotmode, text="Confirm", font=("Verdana", 9), fg="green yellow", bg="forest green", width=18, height=2, \
           command=plotmode_update).grid(row=20, column=0, columnspan=5)

    Label(plotmode, text="   ", font="Helvetica 11", fg="red4").grid(row=21, column=0)

    Button(plotmode, text="Show Map", font=("Verdana", 9), fg="blue2", bg="light steel blue", width=18, height=2, \
           command=showmap).grid(row=22, column=0, columnspan=5)

    Label(plotmode, text="   ", font="Helvetica 11", fg="red4").grid(row=23, column=0)

    plotmode.mainloop()

# OVERVIEW AND CONTROL PANEL
def sourcecontrol():
    global ISKEF
    global ISEGS
    global ISX1
    global ISX2
    global GFZ1
    global GFZ2
    global GFZ3
    global ISKEFm
    global ISEGSm
    global ISX1m
    global ISX2m
    global OBSon

    global Cband3
    global Cband4
    global Cband5
    global Cband6
    global Xband3
    global Xband4
    global Xband5
    global Xband6
    global Cam4
    global Cam5
    global Cam6
    global ISKEFm
    global ISEGSm
    global Cband3m
    global Cband4m
    global Cband5m
    global Cband6m
    global ISX1m
    global ISX2m
    global Xband3m
    global Xband4m
    global Xband5m
    global Xband6m

    SourceStatOview()
    overviewPHS = Toplevel()

    overviewPHS.title("Overview and Control Panel - Plume height sensors:")

    Label(overviewPHS, text='Volcano: ' + label[vulkan] + '    Smithsonian ID: ' + kurzvulk[vulkan], font="Verdana 12", fg="red", bg="yellow").grid(row=0, column=0)
    Label(overviewPHS, text="Select plume height channels", font="Verdana 9", fg="purple").grid(row=1, column=0,
                                                                                                columnspan=3)
    Label(overviewPHS, text="C-band radar:", font="Verdana 11").grid(row=2, column=0)
    Label(overviewPHS, text=ID[0] + ":").grid(row=3, column=0)
    Label(overviewPHS, text=ID[1] + ":").grid(row=4, column=0)
    Label(overviewPHS, text=ID[2] + ":").grid(row=5, column=0)
    Label(overviewPHS, text=ID[3] + ":").grid(row=6, column=0)
    Label(overviewPHS, text=ID[4] + ":").grid(row=7, column=0)
    Label(overviewPHS, text=ID[5] + ":").grid(row=8, column=0)
    Label(overviewPHS, text="X-band radar:", font="Verdana 11").grid(row=9, column=0)
    Label(overviewPHS, text=ID[6] + ":").grid(row=10, column=0)
    Label(overviewPHS, text=ID[7] + ":").grid(row=11, column=0)
    Label(overviewPHS, text=ID[8] + ":").grid(row=12, column=0)
    Label(overviewPHS, text=ID[9] + ":").grid(row=13, column=0)
    Label(overviewPHS, text=ID[10] + ":").grid(row=14, column=0)
    Label(overviewPHS, text=ID[11] + ":").grid(row=15, column=0)
    Label(overviewPHS, text="Web cameras:", font="Verdana 11").grid(row=16, column=0)
    Label(overviewPHS, text=ID[12] + ":").grid(row=17, column=0)
    Label(overviewPHS, text=ID[13] + ":").grid(row=18, column=0)
    Label(overviewPHS, text=ID[14] + ":").grid(row=19, column=0)
    Label(overviewPHS, text=ID[15] + ":").grid(row=20, column=0)
    Label(overviewPHS, text=ID[16] + ":").grid(row=21, column=0)
    Label(overviewPHS, text=ID[17] + ":").grid(row=22, column=0)

    Label(overviewPHS, text="auto").grid(row=2, column=1)
    Label(overviewPHS, text="Non-autostream sources:", font="Verdana 11", fg="navy").grid(row=23, column=0,
                                                                                          columnspan=4, sticky=W)
    Label(overviewPHS, text="ALL MANUAL INPUT:", fg="navy").grid(row=24, column=0, columnspan=2, sticky=E)
    Label(overviewPHS, text=" ").grid(row=25, column=0, columnspan=4, sticky=W)

    OBSon = IntVar()
    OBSon.set(checkbox_oo(OBS_on))
    Checkbutton(overviewPHS, variable=OBSon).grid(row=24, column=2)

    ISKEF = IntVar()
    ISKEF.set(checkbox_oo(ISKEF_on))
    Checkbutton(overviewPHS, variable=ISKEF).grid(row=3, column=1)
    ISEGS = IntVar()
    ISEGS.set(checkbox_oo(ISEGS_on))
    Checkbutton(overviewPHS, variable=ISEGS).grid(row=4, column=1)
    Cband3 = IntVar()
    Cband3.set(checkbox_oo(Cband3_on))
    Checkbutton(overviewPHS, variable=Cband3).grid(row=5, column=1)
    Cband4 = IntVar()
    Cband4.set(checkbox_oo(Cband4_on))
    Checkbutton(overviewPHS, variable=Cband4).grid(row=6, column=1)
    Cband5 = IntVar()
    Cband5.set(checkbox_oo(Cband5_on))
    Checkbutton(overviewPHS, variable=Cband5).grid(row=7, column=1)
    Cband6 = IntVar()
    Cband6.set(checkbox_oo(Cband6_on))
    Checkbutton(overviewPHS, variable=Cband6).grid(row=8, column=1)

    ISX1 = IntVar()
    ISX1.set(checkbox_oo(ISX1_on))
    Checkbutton(overviewPHS, variable=ISX1).grid(row=10, column=1)
    ISX2 = IntVar()
    ISX2.set(checkbox_oo(ISX2_on))
    Checkbutton(overviewPHS, variable=ISX2).grid(row=11, column=1)
    Xband3 = IntVar()
    Xband3.set(checkbox_oo(Xband3_on))
    Checkbutton(overviewPHS, variable=Xband3).grid(row=12, column=1)
    Xband4 = IntVar()
    Xband4.set(checkbox_oo(Xband4_on))
    Checkbutton(overviewPHS, variable=Xband4).grid(row=13, column=1)
    Xband5 = IntVar()
    Xband5.set(checkbox_oo(Xband5_on))
    Checkbutton(overviewPHS, variable=Xband5).grid(row=14, column=1)
    Xband6 = IntVar()
    Xband6.set(checkbox_oo(Xband6_on))
    Checkbutton(overviewPHS, variable=Xband6).grid(row=15, column=1)

    GFZ1 = IntVar()
    GFZ1.set(checkbox_oo(GFZ1_on))
    Checkbutton(overviewPHS, variable=GFZ1).grid(row=17, column=1)
    GFZ2 = IntVar()
    GFZ2.set(checkbox_oo(GFZ2_on))
    Checkbutton(overviewPHS, variable=GFZ2).grid(row=18, column=1)
    GFZ3 = IntVar()
    GFZ3.set(checkbox_oo(GFZ3_on))
    Checkbutton(overviewPHS, variable=GFZ3).grid(row=19, column=1)
    Cam4 = IntVar()
    Cam4.set(checkbox_oo(Cam4_on))
    Checkbutton(overviewPHS, variable=Cam4).grid(row=20, column=1)
    Cam5 = IntVar()
    Cam5.set(checkbox_oo(Cam5_on))
    Checkbutton(overviewPHS, variable=Cam5).grid(row=21, column=1)
    Cam6 = IntVar()
    Cam6.set(checkbox_oo(Cam6_on))
    Checkbutton(overviewPHS, variable=Cam6).grid(row=22, column=1)

    Label(overviewPHS, text="man.").grid(row=2, column=2)
    ISKEFm = IntVar()
    ISKEFm.set(checkbox_oo(ISKEFm_on))
    Checkbutton(overviewPHS, variable=ISKEFm).grid(row=3, column=2)
    ISEGSm = IntVar()
    ISEGSm.set(checkbox_oo(ISEGSm_on))
    Checkbutton(overviewPHS, variable=ISEGSm).grid(row=4, column=2)
    Cband3m = IntVar()
    Cband3m.set(checkbox_oo(Cband3m_on))
    Checkbutton(overviewPHS, variable=Cband3m).grid(row=5, column=2)
    Cband4m = IntVar()
    Cband4m.set(checkbox_oo(Cband4m_on))
    Checkbutton(overviewPHS, variable=Cband4m).grid(row=6, column=2)
    Cband5m = IntVar()
    Cband5m.set(checkbox_oo(Cband5m_on))
    Checkbutton(overviewPHS, variable=Cband5m).grid(row=7, column=2)
    Cband6m = IntVar()
    Cband6m.set(checkbox_oo(Cband6m_on))
    Checkbutton(overviewPHS, variable=Cband6m).grid(row=8, column=2)

    ISX1m = IntVar()
    ISX1m.set(checkbox_oo(ISX1m_on))
    Checkbutton(overviewPHS, variable=ISX1m).grid(row=10, column=2)
    ISX2m = IntVar()
    ISX2m.set(checkbox_oo(ISX2m_on))
    Checkbutton(overviewPHS, variable=ISX2m).grid(row=11, column=2)
    Xband3m = IntVar()
    Xband3m.set(checkbox_oo(Xband3m_on))
    Checkbutton(overviewPHS, variable=Xband3m).grid(row=12, column=2)
    Xband4m = IntVar()
    Xband4m.set(checkbox_oo(Xband4m_on))
    Checkbutton(overviewPHS, variable=Xband4m).grid(row=13, column=2)
    Xband5m = IntVar()
    Xband5m.set(checkbox_oo(Xband5m_on))
    Checkbutton(overviewPHS, variable=Xband5m).grid(row=14, column=2)
    Xband6m = IntVar()
    Xband6m.set(checkbox_oo(Xband6m_on))
    Checkbutton(overviewPHS, variable=Xband6m).grid(row=15, column=2)

    Label(overviewPHS, text="eruption column").grid(row=2, column=8)
    Label(overviewPHS, text=qf_ISKEF, fg=qf_fg_ISKEF).grid(row=3, column=8)
    Label(overviewPHS, text=qf_ISEGS, fg=qf_fg_ISEGS).grid(row=4, column=8)
    Label(overviewPHS, text=qf_Cband3, fg=qf_fg_Cband3).grid(row=5, column=8)
    Label(overviewPHS, text=qf_Cband4, fg=qf_fg_Cband4).grid(row=6, column=8)
    Label(overviewPHS, text=qf_Cband5, fg=qf_fg_Cband5).grid(row=7, column=8)
    Label(overviewPHS, text=qf_Cband6, fg=qf_fg_Cband6).grid(row=8, column=8)

    Label(overviewPHS, text=qf_ISX1, fg=qf_fg_ISX1).grid(row=10, column=8)
    Label(overviewPHS, text=qf_ISX2, fg=qf_fg_ISX2).grid(row=11, column=8)
    Label(overviewPHS, text=qf_Xband3, fg=qf_fg_Xband3).grid(row=12, column=8)
    Label(overviewPHS, text=qf_Xband4, fg=qf_fg_Xband4).grid(row=13, column=8)
    Label(overviewPHS, text=qf_Xband5, fg=qf_fg_Xband5).grid(row=14, column=8)
    Label(overviewPHS, text=qf_Xband6, fg=qf_fg_Xband6).grid(row=15, column=8)

    Label(overviewPHS, text=qf_GFZ1, fg=qf_fg_GFZ1).grid(row=17, column=8)
    Label(overviewPHS, text=qf_GFZ2, fg=qf_fg_GFZ2).grid(row=18, column=8)
    Label(overviewPHS, text=qf_GFZ3, fg=qf_fg_GFZ3).grid(row=19, column=8)
    Label(overviewPHS, text=qf_Cam4, fg=qf_fg_Cam4).grid(row=20, column=8)
    Label(overviewPHS, text=qf_Cam5, fg=qf_fg_Cam5).grid(row=21, column=8)
    Label(overviewPHS, text=qf_Cam6, fg=qf_fg_Cam6).grid(row=22, column=8)

    Label(overviewPHS, text="->").grid(row=3, column=4)
    Label(overviewPHS, text="->").grid(row=4, column=4)
    Label(overviewPHS, text="->").grid(row=5, column=4)
    Label(overviewPHS, text="->").grid(row=6, column=4)
    Label(overviewPHS, text="->").grid(row=7, column=4)
    Label(overviewPHS, text="->").grid(row=8, column=4)
    Label(overviewPHS, text="->").grid(row=10, column=4)
    Label(overviewPHS, text="->").grid(row=11, column=4)
    Label(overviewPHS, text="->").grid(row=12, column=4)
    Label(overviewPHS, text="->").grid(row=13, column=4)
    Label(overviewPHS, text="->").grid(row=14, column=4)
    Label(overviewPHS, text="->").grid(row=15, column=4)
    Label(overviewPHS, text="->").grid(row=17, column=4)
    Label(overviewPHS, text="->").grid(row=18, column=4)
    Label(overviewPHS, text="->").grid(row=19, column=4)
    Label(overviewPHS, text="->").grid(row=20, column=4)
    Label(overviewPHS, text="->").grid(row=21, column=4)
    Label(overviewPHS, text="->").grid(row=22, column=4)

    def distGFZdarst(distance):
        if distance == -1:
            distdarst = "---"
        else:
            distdarst = str(distance)
        return (distdarst)

    distdarstGFZ1 = entfernung(dist_GFZ1)[0]
    distdarstGFZ2 = entfernung(dist_GFZ2)[0]
    distdarstGFZ3 = entfernung(dist_GFZ3)[0]
    distdarstCam4 = entfernung(dist_Cam4)[0]
    distdarstCam5 = entfernung(dist_Cam5)[0]
    distdarstCam6 = entfernung(dist_Cam6)[0]

    Label(overviewPHS, text="distance to").grid(row=2, column=4, columnspan=2)
    Label(overviewPHS, text="vent").grid(row=2, column=6)
    Label(overviewPHS, text=entfernung(dist_ISKEF)[0], fg=entfernung(dist_ISKEF)[2]).grid(row=3, column=5)
    Label(overviewPHS, text=entfernung(dist_ISEGS)[0], fg=entfernung(dist_ISEGS)[2]).grid(row=4, column=5)
    Label(overviewPHS, text=entfernung(dist_Cband3)[0], fg=entfernung(dist_Cband3)[2]).grid(row=5, column=5)
    Label(overviewPHS, text=entfernung(dist_Cband4)[0], fg=entfernung(dist_Cband4)[2]).grid(row=6, column=5)
    Label(overviewPHS, text=entfernung(dist_Cband5)[0], fg=entfernung(dist_Cband5)[2]).grid(row=7, column=5)
    Label(overviewPHS, text=entfernung(dist_Cband6)[0], fg=entfernung(dist_Cband6)[2]).grid(row=8, column=5)

    Label(overviewPHS, text=entfernung(dist_ISX1)[0], fg=entfernung(dist_ISX1)[2]).grid(row=10, column=5)
    Label(overviewPHS, text=entfernung(dist_ISX2)[0], fg=entfernung(dist_ISX2)[2]).grid(row=11, column=5)
    Label(overviewPHS, text=entfernung(dist_Xband3)[0], fg=entfernung(dist_Xband3)[2]).grid(row=12, column=5)
    Label(overviewPHS, text=entfernung(dist_Xband4)[0], fg=entfernung(dist_Xband4)[2]).grid(row=13, column=5)
    Label(overviewPHS, text=entfernung(dist_Xband5)[0], fg=entfernung(dist_Xband5)[2]).grid(row=14, column=5)
    Label(overviewPHS, text=entfernung(dist_Xband6)[0], fg=entfernung(dist_Xband6)[2]).grid(row=15, column=5)

    Label(overviewPHS, text=distdarstGFZ1, fg=entfernung(dist_GFZ1)[2]).grid(row=17, column=5)
    Label(overviewPHS, text=distdarstGFZ2, fg=entfernung(dist_GFZ2)[2]).grid(row=18, column=5)
    Label(overviewPHS, text=distdarstGFZ3, fg=entfernung(dist_GFZ3)[2]).grid(row=19, column=5)
    Label(overviewPHS, text=distdarstCam4, fg=entfernung(dist_Cam4)[2]).grid(row=20, column=5)
    Label(overviewPHS, text=distdarstCam5, fg=entfernung(dist_Cam5)[2]).grid(row=21, column=5)
    Label(overviewPHS, text=distdarstCam6, fg=entfernung(dist_Cam6)[2]).grid(row=22, column=5)

    Label(overviewPHS, text="km").grid(row=3, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=4, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=5, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=6, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=7, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=8, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=10, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=11, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=12, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=13, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=14, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=15, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=17, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=18, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=19, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=20, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=21, column=6, sticky=W)
    Label(overviewPHS, text="km").grid(row=22, column=6, sticky=W)

    Label(overviewPHS, text="sensor located").grid(row=2, column=7)
    Label(overviewPHS, text=entfernung(dist_ISKEF)[1], fg=entfernung(dist_ISKEF)[2]).grid(row=3, column=7)
    Label(overviewPHS, text=entfernung(dist_ISEGS)[1], fg=entfernung(dist_ISEGS)[2]).grid(row=4, column=7)
    Label(overviewPHS, text=entfernung(dist_Cband3)[1], fg=entfernung(dist_Cband3)[2]).grid(row=5, column=7)
    Label(overviewPHS, text=entfernung(dist_Cband4)[1], fg=entfernung(dist_Cband4)[2]).grid(row=6, column=7)
    Label(overviewPHS, text=entfernung(dist_Cband5)[1], fg=entfernung(dist_Cband5)[2]).grid(row=7, column=7)
    Label(overviewPHS, text=entfernung(dist_Cband6)[1], fg=entfernung(dist_Cband6)[2]).grid(row=8, column=7)

    Label(overviewPHS, text=entfernung(dist_ISX1)[1], fg=entfernung(dist_ISX1)[2]).grid(row=10, column=7)
    Label(overviewPHS, text=entfernung(dist_ISX2)[1], fg=entfernung(dist_ISX2)[2]).grid(row=11, column=7)
    Label(overviewPHS, text=entfernung(dist_Xband3)[1], fg=entfernung(dist_Xband3)[2]).grid(row=12, column=7)
    Label(overviewPHS, text=entfernung(dist_Xband4)[1], fg=entfernung(dist_Xband4)[2]).grid(row=13, column=7)
    Label(overviewPHS, text=entfernung(dist_Xband5)[1], fg=entfernung(dist_Xband5)[2]).grid(row=14, column=7)
    Label(overviewPHS, text=entfernung(dist_Xband6)[1], fg=entfernung(dist_Xband6)[2]).grid(row=15, column=7)

    Label(overviewPHS, text=entfernung(dist_GFZ1)[1], fg=entfernung(dist_GFZ1)[2]).grid(row=17, column=7)
    Label(overviewPHS, text=entfernung(dist_GFZ2)[1], fg=entfernung(dist_GFZ2)[2]).grid(row=18, column=7)
    Label(overviewPHS, text=entfernung(dist_GFZ3)[1], fg=entfernung(dist_GFZ3)[2]).grid(row=19, column=7)
    Label(overviewPHS, text=entfernung(dist_Cam4)[1], fg=entfernung(dist_Cam4)[2]).grid(row=20, column=7)
    Label(overviewPHS, text=entfernung(dist_Cam5)[1], fg=entfernung(dist_Cam5)[2]).grid(row=21, column=7)
    Label(overviewPHS, text=entfernung(dist_Cam6)[1], fg=entfernung(dist_Cam6)[2]).grid(row=22, column=7)

    Label(overviewPHS, text="status").grid(row=2, column=3)
    Label(overviewPHS, text=iskef_status, fg=iskef_status_fg).grid(row=3, column=3)
    Label(overviewPHS, text=isegs_status, fg=isegs_status_fg).grid(row=4, column=3)
    Label(overviewPHS, text=cband3_status, fg=cband3_status_fg).grid(row=5, column=3)
    Label(overviewPHS, text=cband4_status, fg=cband4_status_fg).grid(row=6, column=3)
    Label(overviewPHS, text=cband5_status, fg=cband5_status_fg).grid(row=7, column=3)
    Label(overviewPHS, text=cband6_status, fg=cband6_status_fg).grid(row=8, column=3)

    Label(overviewPHS, text=isx1_status, fg=isx1_status_fg).grid(row=10, column=3)
    Label(overviewPHS, text=isx2_status, fg=isx2_status_fg).grid(row=11, column=3)
    Label(overviewPHS, text=xband3_status, fg=xband3_status_fg).grid(row=12, column=3)
    Label(overviewPHS, text=xband4_status, fg=xband4_status_fg).grid(row=13, column=3)
    Label(overviewPHS, text=xband5_status, fg=xband5_status_fg).grid(row=14, column=3)
    Label(overviewPHS, text=xband6_status, fg=xband6_status_fg).grid(row=15, column=3)

    Label(overviewPHS, text="visibility").grid(row=16, column=3)
    Label(overviewPHS, text=gfz_vistable(gfz1_vis)[0], fg=gfz_vistable(gfz1_vis)[1]).grid(row=17, column=3)
    Label(overviewPHS, text=gfz_vistable(gfz2_vis)[0], fg=gfz_vistable(gfz2_vis)[1]).grid(row=18, column=3)
    Label(overviewPHS, text=gfz_vistable(gfz3_vis)[0], fg=gfz_vistable(gfz3_vis)[1]).grid(row=19, column=3)
    Label(overviewPHS, text=gfz_vistable(cam4_vis)[0], fg=gfz_vistable(cam4_vis)[1]).grid(row=20, column=3)
    Label(overviewPHS, text=gfz_vistable(cam5_vis)[0], fg=gfz_vistable(cam4_vis)[1]).grid(row=21, column=3)
    Label(overviewPHS, text=gfz_vistable(cam6_vis)[0], fg=gfz_vistable(cam6_vis)[1]).grid(row=22, column=3)
    Button(overviewPHS, text="Update settings", \
           font=("Verdana", 8, "bold"), bg="dim gray", fg="yellow", command=PHSonoff).grid(row=26, column=0)

    overviewPHS.mainloop()


def default_parameter_panel():
    get_last_data()
    master1 = Toplevel()
    master1.title("Set model parameters")
    Label(master1, text="Check: http://weather.uwyo.edu/upperair/sounding.html", fg="light gray").grid(row=10, column=5,
                                                                                                       columnspan=5)
    Label(master1, text="vent conditions", font=("Verdana", 10, "bold"), fg="blue").grid(row=1, column=0, columnspan=3)
    Label(master1, text="atmos. temperature:").grid(row=2, column=0, sticky=E)
    Label(master1, text="K").grid(row=2, column=2, sticky=W)
    Label(master1, text="atmos. pressure:").grid(row=3, column=0, sticky=E)
    Label(master1, text="Pa").grid(row=3, column=2, sticky=W)

    Label(master1, text="magma conditions", font=("Verdana", 10, "bold"), fg="brown").grid(row=4, column=0,
                                                                                           columnspan=3)
    Label(master1, text="magmatic temperature:").grid(row=5, column=0, sticky=E)
    Label(master1, text="K").grid(row=5, column=2, sticky=W)
    Label(master1, text="Rock density").grid(row=6, column=0, sticky=E)

    Label(master1, text="kg/m^3").grid(row=6, column=2, sticky=W)

    Label(master1, text="plume conditions", font=("Verdana", 10, "bold"), fg="steel blue").grid(row=1, column=3,
                                                                                                columnspan=3)
    Label(master1, text="Radial entrainment coeff.:").grid(row=2, column=3, sticky=E)
    Label(master1, text="").grid(row=2, column=5, sticky=W)
    Label(master1, text="Wind entrainment coeff.:").grid(row=3, column=3, sticky=E)
    Label(master1, text="").grid(row=3, column=5, sticky=W)

    Label(master1, text="model wt. factors", font=("Verdana", 10, "bold"), fg="sea green").grid(row=4, column=3,
                                                                                                columnspan=3)

    Label(master1, text="Wilson Walker:").grid(row=5, column=3, sticky=E)
    Label(master1, text="").grid(row=5, column=5, sticky=W)
    Label(master1, text="Sparks:").grid(row=6, column=3, sticky=E)
    Label(master1, text="").grid(row=6, column=5, sticky=W)
    Label(master1, text="Mastin:").grid(row=7, column=3, sticky=E)
    Label(master1, text="").grid(row=7, column=5, sticky=W)
    Label(master1, text="Gudmundsson:").grid(row=8, column=3, sticky=E)
    Label(master1, text="").grid(row=8, column=5, sticky=W)
    Label(master1, text="Degruyter Bonadonna:").grid(row=9, column=3, sticky=E)
    Label(master1, text="").grid(row=9, column=5, sticky=W)
    Label(master1, text="Woodhouse 0D:").grid(row=10, column=3, sticky=E)
    Label(master1, text="").grid(row=10, column=5, sticky=W)

    Label(master1, text="scale f.", fg="red").grid(row=8, column=6, sticky=W)

    Label(master1, text="atmospheric conditions", font=("Verdana", 10, "bold"), fg="dark violet").grid(row=1, column=6,
                                                                                                       columnspan=3)

    Label(master1, text="Height tropopause a.s.l.:").grid(row=2, column=6, sticky=E)
    Label(master1, text="m").grid(row=2, column=8, sticky=W)
    Label(master1, text="Height stratosphere a.s.l.:").grid(row=3, column=6, sticky=E)
    Label(master1, text="m").grid(row=3, column=8, sticky=W)

    Label(master1, text="Temp. grad. troposphere:").grid(row=4, column=6, sticky=E)
    Label(master1, text="K/m").grid(row=4, column=8, sticky=W)
    Label(master1, text="Temp. grad. trs <-> str:").grid(row=5, column=6, sticky=E)
    Label(master1, text="K/m").grid(row=5, column=8, sticky=W)
    Label(master1, text="Temp. grad. stratosphere:").grid(row=6, column=6, sticky=E)
    Label(master1, text="K/m").grid(row=6, column=8, sticky=W)
    Label(master1, text="Wind speed tropopause:").grid(row=7, column=6, sticky=E)
    Label(master1, text="m/s").grid(row=7, column=8, sticky=W)

    theta_a0_in = Entry(master1, width=7)
    theta_a0_in.insert(10, theta_a0)
    theta_a0_in.grid(row=2, column=1)
    P_0_in = Entry(master1, width=7)
    P_0_in.insert(10, P_0)
    P_0_in.grid(row=3, column=1)

    theta_0_in = Entry(master1, width=7)
    theta_0_in.insert(10, theta_0)
    theta_0_in.grid(row=5, column=1)
    rho_dre_in = Entry(master1, width=7)
    rho_dre_in.insert(10, rho_dre)
    rho_dre_in.grid(row=6, column=1)

    alpha_in = Entry(master1, width=10)
    alpha_in.insert(10, alpha)
    alpha_in.grid(row=2, column=4)
    beta_in = Entry(master1, width=10)
    beta_in.insert(10, beta)
    beta_in.grid(row=3, column=4)

    wf_wil = Entry(master1, width=10)
    wf_spa = Entry(master1, width=10)
    wf_mas = Entry(master1, width=10)
    wf_mtg = Entry(master1, width=10)
    wf_deg = Entry(master1, width=10)
    wf_wood0d = Entry(master1, width=10)

    wf_wil.insert(10, wfac_mod4_default[0])
    wf_spa.insert(10, wfac_mod4_default[1])
    wf_mas.insert(10, wfac_mod4_default[2])
    wf_mtg.insert(10, wfac_mod4_default[3])
    wf_deg.insert(10, wfac_mod4_default[4])
    wf_wood0d.insert(10, wfac_mod4_default[5])

    wf_wil.grid(row=5, column=4)
    wf_spa.grid(row=6, column=4)
    wf_mas.grid(row=7, column=4)
    wf_mtg.grid(row=8, column=4)
    wf_deg.grid(row=9, column=4)
    wf_wood0d.grid(row=10, column=4)

    H1_in = Entry(master1, width=10)
    H2_in = Entry(master1, width=10)
    tempGrad_1_in = Entry(master1, width=10)
    tempGrad_2_in = Entry(master1, width=10)
    tempGrad_3_in = Entry(master1, width=10)
    Vmax_in = Entry(master1, width=10)
    ki_in = Entry(master1, width=4, fg="red")

    H1_in.insert(10, H1)
    H2_in.insert(10, H2)
    tempGrad_1_in.insert(10, tempGrad_1)
    tempGrad_2_in.insert(10, tempGrad_2)
    tempGrad_3_in.insert(10, tempGrad_3)
    Vmax_in.insert(10, Vmax_default)
    ki_in.insert(10, ki)

    H1_in.grid(row=2, column=7)
    H2_in.grid(row=3, column=7)
    tempGrad_1_in.grid(row=4, column=7)
    tempGrad_2_in.grid(row=5, column=7)
    tempGrad_3_in.grid(row=6, column=7)
    Vmax_in.grid(row=7, column=7)
    ki_in.grid(row=8, column=5)

    def default_update():
        global theta_a0
        global P_0
        global theta_0
        global rho_dre
        global alpha
        global beta
        global wtf_wil
        global wtf_spa
        global wtf_mas
        global wtf_mtg
        global wtf_deg
        global wtf_wood0d
        global H1, H1asl
        global H2, H2asl
        global tempGrad_1
        global tempGrad_2
        global tempGrad_3
        global Vmax
        global ki
        theta_a0 = float(theta_a0_in.get())
        P_0 = float(P_0_in.get())
        theta_0 = float(theta_0_in.get())
        rho_dre = float(rho_dre_in.get())
        alpha = float(alpha_in.get())
        beta = float(beta_in.get())
        wtf_wil = float(wf_wil.get())
        wtf_spa = float(wf_spa.get())
        wtf_mas = float(wf_mas.get())
        wtf_mtg = float(wf_mtg.get())
        wtf_deg = float(wf_deg.get())
        wtf_wood0d = float(wf_wood0d.get())
        H1asl = float(H1_in.get())
        H2asl = float(H2_in.get())
        tempGrad_1 = float(tempGrad_1_in.get())
        tempGrad_2 = float(tempGrad_2_in.get())
        tempGrad_3 = float(tempGrad_3_in.get())
        Vmax = float(Vmax_in.get())
        ki = float(ki_in.get())

        H1 = H1asl
        H2 = H2asl
        save_default_file()
        print("*** settings updated! ***")
        check_configfile()

    Button(master1, text="Update model parameters", font=("Verdana", 8, "bold"), bg="dim gray", fg="yellow",
           command=default_update).grid(row=9, column=0, columnspan=3)

    master1.mainloop()


# observed plume height input

TimeNUNA = datetime.datetime.utcnow()
TimeNUNAs = str(TimeNUNA)
YearNUNAs = TimeNUNAs[:4]
MonthNUNAs = TimeNUNAs[5:7]
DayNUNAs = TimeNUNAs[8:10]
HourNUNAs = TimeNUNAs[11:13]
MinuteNUNAs = TimeNUNAs[14:16]


def save_OBSfile(inputEoZ):
    """stores input data into fix_OBSin file"""
    FILE_OBS = open("fix_OBSin.txt", "a",encoding="utf-8", errors="surrogateescape")
    FILE_OBS.write(str(time_OBSdata) + "\t" + str(OBSd_on) + "\t" \
                   + str(sourceOBSdata) + "\t" + str(Hmin_obs) + "\t" + str(Havg_obs) + "\t" + str(
        Hmax_obs) + "\t" + str(unc_OBS) + "\t" + str(qf_OBS) + "\t" + str(inputEoZ) + "\t" + "9" + "\t" + str(
        Min_DiaOBS) + "\t" + str(Max_DiaOBS) + "\t" + str(time_OBSlog) + "\t" + str(comment_obs) + "\n")
    FILE_OBS.close()
    print("***observed data stored!***")


def sensorliste():
    """generates list of sensors available for manual pl.h. input"""
    global N_en, N_en2
    liSens = []
    for a in range(0, N_en):
        liSens.append(ID[a])
    for b in range(0, N_en2):
        liSens.append(ID[b + 6])
    liSens.append("aircraft")
    liSens.append("ground")
    liSens.append("satellite")
    liSens.append("other")
    return (liSens)


def entfliste():
    """generates list of sensors available for manual pl.h. input"""
    global N_en, N_en2
    liEntf = []
    if dist_ISKEF != 9999:
        liEntf.append(dist_ISKEF)
    else:
        None
    if dist_ISEGS != 9999:
        liEntf.append(dist_ISEGS)
    else:
        None
    if dist_Cband3 != 9999:
        liEntf.append(dist_Cband3)
    else:
        None
    if dist_Cband4 != 9999:
        liEntf.append(dist_Cband4)
    else:
        None
    if dist_Cband5 != 9999:
        liEntf.append(dist_Cband5)
    else:
        None
    if dist_Cband6 != 9999:
        liEntf.append(dist_Cband6)
    else:
        None
    if dist_ISX1 != 9999:
        liEntf.append(dist_ISX1)
    else:
        None
    if dist_ISX2 != 9999:
        liEntf.append(dist_ISX2)
    else:
        None
    if dist_Xband3 != 9999:
        liEntf.append(dist_Xband3)
    else:
        None
    if dist_Xband4 != 9999:
        liEntf.append(dist_Xband4)
    else:
        None
    if dist_Xband5 != 9999:
        liEntf.append(dist_Xband5)
    else:
        None
    if dist_Xband6 != 9999:
        liEntf.append(dist_Xband6)
    else:
        None
    return (liEntf)


def add_plhobs():
    global Hmin_obs_in
    global Hmax_obs_in
    global qf_obs
    global OBSdata_on, pl_minw_default, pl_maxw_default

    TimeNUNA = datetime.datetime.utcnow()
    TimeNUNAs = str(TimeNUNA)
    YearNUNAs = TimeNUNAs[:4]
    MonthNUNAs = TimeNUNAs[5:7]
    DayNUNAs = TimeNUNAs[8:10]
    HourNUNAs = TimeNUNAs[11:13]
    MinuteNUNAs = TimeNUNAs[14:16]
    plhobs = Toplevel()
    plhobs.title("Observed plume heights")

    def plhobs_quality(source):
        """attributes quality factor according to source"""
        global qf_OBS
        if source == 101:
            qf_OBS = Cradarquality(dist_ISKEF, sens_bwidth[0])[0]
        elif source == 102:
            qf_OBS = Cradarquality(dist_ISEGS, sens_bwidth[1])[0]
        elif source == 103:
            qf_OBS = Cradarquality(dist_Cband3, sens_bwidth[2])[0]
        elif source == 104:
            qf_OBS = Cradarquality(dist_Cband4, sens_bwidth[3])[0]
        elif source == 105:
            qf_OBS = Cradarquality(dist_Cband5, sens_bwidth[4])[0]
        elif source == 106:
            qf_OBS = Cradarquality(dist_Cband6, sens_bwidth[5])[0]
        elif source == 201:
            qf_OBS = Xradarquality(dist_ISX1, sens_bwidth[6])[0]
        elif source == 202:
            qf_OBS = Xradarquality(dist_ISX2, sens_bwidth[7])[0]
        elif source == 203:
            qf_OBS = Xradarquality(dist_Xband3, sens_bwidth[8])[0]
        elif source == 204:
            qf_OBS = Xradarquality(dist_Xband4, sens_bwidth[9])[0]
        elif source == 205:
            qf_OBS = Xradarquality(dist_Xband5, sens_bwidth[10])[0]
        elif source == 206:
            qf_OBS = Xradarquality(dist_Xband6, sens_bwidth[11])[0]
        else:
            qf_OBS = qf_OBS
        print("aktueller Status:")
        print (str(source))
        print (str(qf_OBS))
        print("*")
        return ()

    def plhobs_update():

        def uncOBS(Havg, Hmin):
            """computes uncertainty of manual input data"""
            global unc_OBS
            unc_OBS = abs(Havg - Hmin)
            return ()

        global Hmin_obs
        global Hmax_obs
        global Havg_obs
        global qf_OBS
        global time_OBS, time_OBSlog  # input time, input time formated for log
        global time_OBSdata  # time of data
        global OBSd_on
        global sourceOBSdata
        global comment_obs
        global Min_DiaOBS, Max_DiaOBS

        list_S = sensorliste()

        list_entf = entfliste()
        time_OBS = datetime.datetime.utcnow()
        time_OBSlog = datetime.datetime.utcnow()
        time_OBSlog = time_OBS.strftime("%m %d %Y %H:%M:%S")
        Y_OBSdata = int(time_OBS_y.get())
        MO_OBSdata = int(time_OBS_mo.get())
        D_OBSdata = int(time_OBS_d.get())
        H_OBSdata = int(time_OBS_h.get())
        M_OBSdata = int(time_OBS_m.get())
        time_OBSdata = datetime.datetime(Y_OBSdata, MO_OBSdata, D_OBSdata, H_OBSdata, M_OBSdata)
        time_OBSdata = time_OBSdata.strftime("%m %d %Y %H:%M:%S")
        menu = str(SRC_var.get())
        Hmin_obs = 0 #new
        Hmax_obs = 0 #new
        if len(pl_width_min.get()) == 0:
            Min_DiaOBS = 0
            Max_DiaOBS = 0
        else:
            Min_DiaOBS = float(pl_width_min.get())
            Max_DiaOBS = float(pl_width_max.get())
        if len(Havg_obs_in.get()) == 0:
            # mean plume height box is emtpty, min and max input expected
            Hmin_obs_km = float(Hmin_obs_in.get())
            Hmin_obs = Hmin_obs_km * 1000
            Hmax_obs_km = float(Hmax_obs_in.get())
            Hmax_obs = Hmax_obs_km * 1000
            Havg_obs = int((Hmin_obs + Hmax_obs) / 2)
            inputEoZ = 2  # indicator: one or two plh entries?
        else:
            inputEoZ = 1
            Havg_obs_km = float(Havg_obs_in.get())
            Havg_obs = Havg_obs_km * 1000
        for a in range(0, N_en):
            if menu == list_S[a]:
                OBSerr = Cradarerror(list_entf[a], sens_bwidth[a])
                if OBSerr == 99999:
                    print("WARNING! Radar out of range??")
                    OBSerr = 2000  # this will only occur if input error
                    Hmin_obs = Havg_obs - OBSerr
                    Hmax_obs = Havg_obs + OBSerr
                else:
                    Hmin_obs = Havg_obs - OBSerr
                    Hmax_obs = Havg_obs + OBSerr
            else:
                None
        ba = 0
        for b in range(N_en, N_en + N_en2):
            ba = ba + 1
            if menu == list_S[b]:
                OBSerr = Xradarerror(list_entf[b], sens_bwidth[5 + ba])
                if OBSerr == 99999:
                    print("WARNING! Radar out of range??")
                    OBSerr = 2000  # this will only occur if input error
                    Hmin_obs = Havg_obs - OBSerr
                    Hmax_obs = Havg_obs + OBSerr
                else:
                    Hmin_obs = Havg_obs - OBSerr
                    Hmax_obs = Havg_obs + OBSerr
        if menu == "aircraft":
            OBSerr = 1000  # assumed error for plh data obtained by aircraft
            #Hmin_obs = Havg_obs - OBSerr
            #Hmax_obs = Havg_obs + OBSerr
        elif menu == "ground":
            OBSerr = 1500  # assumed error for ground obs obtained plh data
            #Hmin_obs = Havg_obs - OBSerr
            #Hmax_obs = Havg_obs + OBSerr
        elif menu == "satellite":
            OBSerr = 1000 # to review
            #Hmin_obs = Havg_obs - OBSerr
            #Hmax_obs = Havg_obs + OBSerr
        elif menu == "other":
            OBSerr = 1500  # assumed error for plh data by other source
            #Hmin_obs = Havg_obs - OBSerr
            #Hmax_obs = Havg_obs + OBSerr

        if Hmin_obs == 0:
            Hmin_obs = Havg_obs - OBSerr
        if Hmax_obs == 0:
            Hmax_obs = Havg_obs + OBSerr

        comment_obs = str(comment_OBS.get())
        # ID source codes for manual input:
        # Cband radar : 101-106
        # Xband radar : 201-206
        # aircraft: 700
        # ground: 800
        # other: 900
        for a in range(0, N_en):
            if menu == list_S[a]:
                sourceOBSdata = 101 + a
            else:
                None
        for b in range(N_en, N_en + N_en2):
            if menu == list_S[b]:
                sourceOBSdata = 201 + a
            else:
                None
        if menu == "aircraft":
            sourceOBSdata = 700
        elif menu == "ground":
            sourceOBSdata = 800
        elif menu == "satellite":
            sourceOBSdata = 850
        elif menu == "other":
            sourceOBSdata = 900

        qf_OBS = int(qf_obs.get())

        OBSd_on = int(OBSdata_on.get())

        plhobs_quality(sourceOBSdata)

        uncOBS(Havg_obs, Hmin_obs)
        save_default_file()
        save_OBSfile(inputEoZ)
        check_configfile()

    get_last_data()
    if pl_minw_default == 0:
        pl_minw_default = 0.2
        pl_maxw_default = 0.5
    else:
        print()
    OBSdata_on = IntVar()
    OBSdata_on.set(True)

    Label(plhobs, text="Plume height observed", font=("Verdana", 11, "bold" \
                                                      ), fg="blue").grid(row=0, column=3, columnspan=9)

    Label(plhobs, text="Time of observation:", font=("bold")).grid(row=1, column=0, columnspan=5, sticky=S)
    Label(plhobs, text="h").grid(row=2, column=0, sticky=E)
    Label(plhobs, text=":").grid(row=2, column=1)
    Label(plhobs, text="min").grid(row=2, column=2, sticky=W)
    Label(plhobs, text="day").grid(row=2, column=3, sticky=E)
    Label(plhobs, text="month").grid(row=2, column=4)
    Label(plhobs, text="year").grid(row=2, column=5, sticky=W)
    Label(plhobs, text=":").grid(row=3, column=1)
    time_OBS_h = Entry(plhobs, width=2)
    time_OBS_h.grid(row=3, column=0, sticky=E)
    time_OBS_m = Entry(plhobs, width=2)
    time_OBS_m.grid(row=3, column=2, sticky=W)
    time_OBS_d = Entry(plhobs, width=2)
    time_OBS_d.grid(row=3, column=3, sticky=E)
    time_OBS_mo = Entry(plhobs, width=2)
    time_OBS_mo.grid(row=3, column=4)
    time_OBS_y = Entry(plhobs, width=4)
    time_OBS_y.grid(row=3, column=5, sticky=W)

    time_OBS_y.insert(10, YearNUNAs)
    time_OBS_mo.insert(10, MonthNUNAs)
    time_OBS_d.insert(10, DayNUNAs)
    time_OBS_h.insert(10, HourNUNAs)
    time_OBS_m.insert(10, MinuteNUNAs)

    Label(plhobs, text="              ").grid(row=1, column=6, sticky=W)
    Label(plhobs, text="Plume top height range (asl):", font=("bold")).grid(row=1, column=7, columnspan=3, sticky=S)
    Label(plhobs, text="Min. est. top:").grid(row=2, column=7, sticky=E)
    Label(plhobs, text="km").grid(row=2, column=9, sticky=W)
    Label(plhobs, text="Max. est. top:").grid(row=3, column=7, sticky=E)
    Label(plhobs, text="km").grid(row=3, column=9, sticky=W)
    Label(plhobs, text="Data source:").grid(row=7, column=7, sticky=E)
    Hmin_obs_in = Entry(plhobs, width=4)
    Hmax_obs_in = Entry(plhobs, width=4)
    Hmin_obs_in.grid(row=2, column=8, sticky=E)
    Hmax_obs_in.grid(row=3, column=8, sticky=E)

    Label(plhobs, text="OR").grid(row=4, column=8, sticky=W)
    Label(plhobs, text="Mean est. top:").grid(row=5, column=7, sticky=E)
    Label(plhobs, text="km").grid(row=5, column=9, sticky=W)
    Havg_obs_in = Entry(plhobs, width=4)
    Havg_obs_in.grid(row=5, column=8, sticky=E)

    Label(plhobs, text="NOTE:", font=("Verdana", 8) \
          , fg="red", bg="yellow").grid(row=5, column=0, sticky=W)

    Label(plhobs, text="Convert ground obs data to a.s.l. values!", font=("Verdana", 9) \
          , fg="red", bg="yellow").grid(row=6, column=0, columnspan=8, sticky=W)

    Label(plhobs, text="Plume diameter:", font=("bold")).grid(row=7, column=1, columnspan=5, sticky=S)
    Label(plhobs, text="Min width:").grid(row=8, column=1, columnspan=2, sticky=E)
    Label(plhobs, text="Max width:").grid(row=9, column=1, columnspan=2, sticky=E)
    Label(plhobs, text="km").grid(row=8, column=4, sticky=W)
    Label(plhobs, text="km").grid(row=9, column=4, sticky=W)
    pl_width_min = Entry(plhobs, width=4)
    pl_width_min.grid(row=8, column=3, sticky=E)
    pl_width_min.insert(10, pl_minw_default)
    pl_width_max = Entry(plhobs, width=4)
    pl_width_max.grid(row=9, column=3, sticky=E)
    pl_width_max.insert(10, pl_maxw_default)

    SRC_var = StringVar(plhobs)
    SRC_var.set("ground")
    list_S = sensorliste()
    wsrc = OptionMenu(plhobs, SRC_var, *list_S)
    wsrc.grid(row=7, column=8, columnspan=2)

    Label(plhobs, text="       ").grid(row=1, column=10, sticky=W)
    Label(plhobs, text="Quality of data:", font=("bold")). \
        grid(row=1, column=11, columnspan=2, sticky=E)
    Label(plhobs, text="       ").grid(row=8, column=10, sticky=W)
    Label(plhobs, text="       ").grid(row=10, column=10, sticky=W)
    qf_obs = IntVar()
    Radiobutton(plhobs, text="poor", variable=qf_obs, value=1).grid(row=2, column=12, columnspan=2, sticky=W)
    Radiobutton(plhobs, text="fair", variable=qf_obs, value=2).grid(row=3, column=12, columnspan=2, sticky=W)
    Radiobutton(plhobs, text="good", variable=qf_obs, value=3).grid(row=4, column=12, columnspan=2, sticky=W)
    Radiobutton(plhobs, text="brilliant", variable=qf_obs, value=4).grid(row=5, column=12, columnspan=2, sticky=W)

    qf_obs.set(qf_OBS)
    Label(plhobs, text="Comment:").grid(row=9, column=6, sticky=E)
    comment_OBS = Entry(plhobs, width=30)
    comment_OBS.grid(row=9, column=7, columnspan=2, sticky=W)

    Label(plhobs, text="Include data?", font=("Verdana", 8), fg="red").grid(row=9, column=11, columnspan=3, sticky=W)
    Checkbutton(plhobs, variable=OBSdata_on).grid(row=9, column=10, sticky=E)

    Button(plhobs, text="Update observed plume height", font=("Verdana", 8, \
                                                              "bold"), bg="dim gray", fg="yellow",
           command=plhobs_update).grid(row=11, \
                                       column=6, columnspan=4)

    plhobs.mainloop()


TimeObs1 = "--------"
TimeUpdate1 = "--------"
default_txt = "!!! NOTE: Set initial parameters and activate plume height sensors !!!"
default_bg = "yellow"


def check_configfile():
    global bgcol
    try:
        global TimeObs1
        global time_OBS
        global TimeUpdate1
        global sTimeUpdate1
        global sTimeObs1
        configfile = open("fix_config.txt", "r",encoding="utf-8", errors="surrogateescape")
        configlines4 = configfile.readlines()
        configfile.close()
        TimeUpdate = configlines4[1]
        TimeUpdate1 = TimeUpdate[:16]
        sTimeUpdate1.set(TimeUpdate1)
        TimeObs = configlines4[2]
        TimeObs1 = TimeObs[:16]
        sTimeObs1.set(TimeObs1)
        vdefault_test = 1
        bgcol.set("dark green")
        label3.configure(bg=bgcol.get())
        label3.configure(fg="green yellow")


    except EnvironmentError:
        vdefault_test = 0
        sTimeObs1.set("--:--:--")
        sTimeUpdate1.set("--:--:--")
        bgcol.set("yellow")
        label3.configure(bg=bgcol.get())
        label3.configure(fg="red")

    global default_txt
    global default_bg

    if vdefault_test == 0:
        default_txt = "!!! NOTE: Set initial parameters and activate plume height sensors !!!"
        default_bg = "yellow"
        bgcol.set("yellow")
        sdefault_txt.set(default_txt)

    else:
        default_txt = "OK - system parameters initialized."
        default_bg = "lime green"
        sdefault_txt.set(default_txt)
        bgcol.set("lime green")


sTimeUpdate1 = StringVar()
sTimeObs1 = StringVar()
sdefault_txt = StringVar()
bgcol = StringVar()
bgcol.set('orange')
label3 = Label(masterklick, textvariable=sdefault_txt, bg=bgcol.get())

check_configfile()
Analysis = IntVar()


def analysis_mode():
    global analysis
    global Analysis
    get_last_data()

    anam = Toplevel()
    anam.title("Setting of mode")

    Label(anam, text="Set Analysis Mode", font=("Verdana", 8, "bold") \
          , fg="orange").grid(row=0, column=0, columnspan=2)
    Label(anam, text="If switched ON, all individual MER values will be \
logged").grid(row=1, column=0, sticky=W, columnspan=2)
    Label(anam, text="            and additional source stats will be plotted").grid(row=2, column=0, sticky=W,
                                                                                     columnspan=2)
    Analysis = IntVar()
    Analysis.set(checkbox_oo(analysis))
    Radiobutton(anam, text="OFF", fg="dark green", variable=Analysis, value=0).grid(row=3, column=0, sticky=E)
    Radiobutton(anam, text="ON", fg="lime green", variable=Analysis, value=1).grid(row=3, column=1, sticky=W)

    Label(anam, text="").grid(row=3, column=0, sticky=W, columnspan=2)
    Label(anam, text="CAUTION: long monitoring periods might cause large files!" \
          , fg="red").grid(row=5, column=0, sticky=W, columnspan=2)
    Label(anam, text="").grid(row=6, column=0, sticky=W, columnspan=2)

    def analysis_update():
        global analysis
        global Analysis
        analysis = int(Analysis.get())
        print("ANALYSIS MODE: " + str(analysis))
        save_default_file()
        print("*** settings updated! ***")
        check_configfile()

    Button(anam, text="Confirm", font=("Verdana", 8), width=18, height=2, \
           command=analysis_update).grid(row=7, column=0, columnspan=2)

    anam.mainloop()


def tb_mode():
    global timebase
    get_last_data()

    tb = Toplevel()
    tb.title("Setting of time base")

    Label(tb, text="Set Time Base", font=("Verdana", 8, "bold") \
          , fg="purple").grid(row=0, column=0, columnspan=2)
    variable = StringVar(tb)

    if timebase == 15:
        menun = "15min"
    elif timebase == 30:
        menun = "30min"
    elif timebase == 60:
        menun = "1h"
    elif timebase == 180:
        menun = "3h"
    else:
        menun = "Auto30"

    variable.set(menun)

    w = OptionMenu(tb, variable, "15min", "30min", "1h", "3h", "Auto30")
    w.grid(row=1, column=0, columnspan=2)

    def tb_update():
        global timebase
        menu = str(variable.get())
        if menu == "15min":
            timebase = 15
        elif menu == "30min":
            timebase = 30
        elif menu == "1h":
            timebase = 60
        elif menu == "3h":
            timebase = 180
        elif menu == "Auto30":
            timebase = -1
        else:
            timebase = 30

        save_default_file()
        print("*** settings updated! ***")
        check_configfile()

    Button(tb, text="Confirm", font=("Verdana", 8), width=18, height=2, \
           command=tb_update).grid(row=2, column=0, columnspan=2)

    tb.mainloop()


def calibF():
    global cal_ISKEF_a, cal_ISKEF_b, cal_ISEGS_a, cal_ISEGS_b  # radar calib. param.
    global Cal_ISKEF_a, Cal_ISKEF_b, Cal_ISEGS_a, Cal_ISEGS_b  # radar calib. param.
    global cal_ISX1_a, cal_ISX1_b, cal_ISX2_a, cal_ISX2_b  # radar calib. param.
    global Cal_ISX1_a, Cal_ISX1_b, Cal_ISX2_a, Cal_ISX2_b  # radar calib. param.
    global cal_Cband3a, cal_Cband3b, cal_Cband4a, cal_Cband4b, cal_Cband5a, cal_Cband5b, \
        cal_Cband6a, cal_Cband6b, cal_Xband3a, cal_Xband3b, cal_Xband4a, cal_Xband4b, \
        cal_Xband5a, cal_Xband5b, cal_Xband6a, cal_Xband6b

    global Cal_Cband3a, Cal_Cband3b, Cal_Cband4a, Cal_Cband4b, Cal_Cband5a, Cal_Cband5b, \
        Cal_Cband6a, Cal_Cband6b, Cal_Xband3a, Cal_Xband3b, Cal_Xband4a, Cal_Xband4b, \
        Cal_Xband5a, Cal_Xband5b, Cal_Xband6a, Cal_Xband6b

    get_last_data()

    calibP = Toplevel()
    calibP.title("Radar calibration settings")

    Label(calibP, text="Radar calibration", font=("Verdana", 11, "bold") \
          , fg="green4").grid(row=0, column=0, columnspan=3)
    Label(calibP, text=" ").grid(row=2, column=1)
    Label(calibP, text="Calibrated height: H = A + B x h", fg="red").grid(row=1, column=0, columnspan=3)

    Label(calibP, text="offset A").grid(row=3, column=1)
    Label(calibP, text="cal.f. B").grid(row=3, column=2)
    Label(calibP, text=ID[0], font=("Verdana", 9)).grid(row=4, column=0)
    Cal_ISKEF_a = Entry(calibP, width=7)
    Cal_ISKEF_a.grid(row=4, column=1)
    Cal_ISKEF_a.insert(10, str(cal_ISKEF_a))
    Cal_ISKEF_b = Entry(calibP, width=7)
    Cal_ISKEF_b.grid(row=4, column=2)
    Cal_ISKEF_b.insert(10, str(cal_ISKEF_b))

    Label(calibP, text=ID[1], font=("Verdana", 9)).grid(row=5, column=0)
    Cal_ISEGS_a = Entry(calibP, width=7)
    Cal_ISEGS_a.grid(row=5, column=1)
    Cal_ISEGS_a.insert(10, str(cal_ISEGS_a))
    Cal_ISEGS_b = Entry(calibP, width=7)
    Cal_ISEGS_b.grid(row=5, column=2)
    Cal_ISEGS_b.insert(10, str(cal_ISEGS_b))

    Label(calibP, text=ID[2], font=("Verdana", 9)).grid(row=6, column=0)
    Cal_Cband3a = Entry(calibP, width=7)
    Cal_Cband3a.grid(row=6, column=1)
    Cal_Cband3a.insert(10, str(cal_Cband3a))
    Cal_Cband3b = Entry(calibP, width=7)
    Cal_Cband3b.grid(row=6, column=2)
    Cal_Cband3b.insert(10, str(cal_Cband3b))

    Label(calibP, text=ID[3], font=("Verdana", 9)).grid(row=7, column=0)
    Cal_Cband4a = Entry(calibP, width=7)
    Cal_Cband4a.grid(row=7, column=1)
    Cal_Cband4a.insert(10, str(cal_Cband4a))
    Cal_Cband4b = Entry(calibP, width=7)
    Cal_Cband4b.grid(row=7, column=2)
    Cal_Cband4b.insert(10, str(cal_Cband4b))

    Label(calibP, text=ID[4], font=("Verdana", 9)).grid(row=8, column=0)
    Cal_Cband5a = Entry(calibP, width=7)
    Cal_Cband5a.grid(row=8, column=1)
    Cal_Cband5a.insert(10, str(cal_Cband5a))
    Cal_Cband5b = Entry(calibP, width=7)
    Cal_Cband5b.grid(row=8, column=2)
    Cal_Cband5b.insert(10, str(cal_Cband5b))

    Label(calibP, text=ID[5], font=("Verdana", 9)).grid(row=9, column=0)
    Cal_Cband6a = Entry(calibP, width=7)
    Cal_Cband6a.grid(row=9, column=1)
    Cal_Cband6a.insert(10, str(cal_Cband6a))
    Cal_Cband6b = Entry(calibP, width=7)
    Cal_Cband6b.grid(row=9, column=2)
    Cal_Cband6b.insert(10, str(cal_Cband6b))

    Label(calibP, text="  ", font=("Verdana", 9)).grid(row=10, column=0)

    Label(calibP, text=ID[6], font=("Verdana", 9)).grid(row=11, column=0)
    Cal_ISX1_a = Entry(calibP, width=7)
    Cal_ISX1_a.grid(row=11, column=1)
    Cal_ISX1_a.insert(10, str(cal_ISX1_a))
    Cal_ISX1_b = Entry(calibP, width=7)
    Cal_ISX1_b.grid(row=11, column=2)
    Cal_ISX1_b.insert(10, str(cal_ISX1_b))

    Label(calibP, text=ID[7], font=("Verdana", 9)).grid(row=12, column=0)
    Cal_ISX2_a = Entry(calibP, width=7)
    Cal_ISX2_a.grid(row=12, column=1)
    Cal_ISX2_a.insert(10, str(cal_ISX2_a))
    Cal_ISX2_b = Entry(calibP, width=7)
    Cal_ISX2_b.grid(row=12, column=2)
    Cal_ISX2_b.insert(10, str(cal_ISX2_b))

    Label(calibP, text=ID[8], font=("Verdana", 9)).grid(row=13, column=0)
    Cal_Xband3a = Entry(calibP, width=7)
    Cal_Xband3a.grid(row=13, column=1)
    Cal_Xband3a.insert(10, str(cal_Xband3a))
    Cal_Xband3b = Entry(calibP, width=7)
    Cal_Xband3b.grid(row=13, column=2)
    Cal_Xband3b.insert(10, str(cal_Xband3b))

    Label(calibP, text=ID[9], font=("Verdana", 9)).grid(row=14, column=0)
    Cal_Xband4a = Entry(calibP, width=7)
    Cal_Xband4a.grid(row=14, column=1)
    Cal_Xband4a.insert(10, str(cal_Xband4a))
    Cal_Xband4b = Entry(calibP, width=7)
    Cal_Xband4b.grid(row=14, column=2)
    Cal_Xband4b.insert(10, str(cal_Xband4b))

    Label(calibP, text=ID[10], font=("Verdana", 9)).grid(row=15, column=0)
    Cal_Xband5a = Entry(calibP, width=7)
    Cal_Xband5a.grid(row=15, column=1)
    Cal_Xband5a.insert(10, str(cal_Xband5a))
    Cal_Xband5b = Entry(calibP, width=7)
    Cal_Xband5b.grid(row=15, column=2)
    Cal_Xband5b.insert(10, str(cal_Xband5b))

    Label(calibP, text=ID[11], font=("Verdana", 9)).grid(row=16, column=0)
    Cal_Xband6a = Entry(calibP, width=7)
    Cal_Xband6a.grid(row=16, column=1)
    Cal_Xband6a.insert(10, str(cal_Xband6a))
    Cal_Xband6b = Entry(calibP, width=7)
    Cal_Xband6b.grid(row=16, column=2)
    Cal_Xband6b.insert(10, str(cal_Xband6b))

    Label(calibP, text=" ").grid(row=17, column=1)

    def calibP_update():
        global cal_ISKEF_a, cal_ISKEF_b, cal_ISEGS_a, cal_ISEGS_b
        global Cal_ISKEF_a, Cal_ISKEF_b, Cal_ISEGS_a, Cal_ISEGS_b
        global cal_ISX1_a, cal_ISX1_b, cal_ISX2_a, cal_ISX2_b
        global Cal_ISX1_a, Cal_ISX1_b, Cal_ISX2_a, Cal_ISX2_b
        global cal_Cband3a, cal_Cband3b, cal_Cband4a, cal_Cband4b, cal_Cband5a, cal_Cband5b, \
            cal_Cband6a, cal_Cband6b, cal_Xband3a, cal_Xband3b, cal_Xband4a, cal_Xband4b, \
            cal_Xband5a, cal_Xband5b, cal_Xband6a, cal_Xband6b
        global Cal_Cband3a, Cal_Cband3b, Cal_Cband4a, Cal_Cband4b, Cal_Cband5a, Cal_Cband5b, \
            Cal_Cband6a, Cal_Cband6b, Cal_Xband3a, Cal_Xband3b, Cal_Xband4a, Cal_Xband4b, \
            Cal_Xband5a, Cal_Xband5b, Cal_Xband6a, Cal_Xband6b

        cal_ISKEF_a = float(Cal_ISKEF_a.get())
        cal_ISKEF_b = float(Cal_ISKEF_b.get())
        cal_ISEGS_a = float(Cal_ISEGS_a.get())
        cal_ISEGS_b = float(Cal_ISEGS_b.get())
        cal_Cband3a = float(Cal_Cband3a.get())
        cal_Cband3b = float(Cal_Cband3b.get())
        cal_Cband4a = float(Cal_Cband4a.get())
        cal_Cband4b = float(Cal_Cband4b.get())
        cal_Cband5a = float(Cal_Cband5a.get())
        cal_Cband5b = float(Cal_Cband5b.get())
        cal_Cband6a = float(Cal_Cband6a.get())
        cal_Cband6b = float(Cal_Cband6b.get())

        cal_ISX1_a = float(Cal_ISX1_a.get())
        cal_ISX1_b = float(Cal_ISX1_b.get())
        cal_ISX2_a = float(Cal_ISX2_a.get())
        cal_ISX2_b = float(Cal_ISX2_b.get())
        cal_Xband3a = float(Cal_Xband3a.get())
        cal_Xband3b = float(Cal_Xband3b.get())
        cal_Xband4a = float(Cal_Xband4a.get())
        cal_Xband4b = float(Cal_Xband4b.get())
        cal_Xband5a = float(Cal_Xband5a.get())
        cal_Xband5b = float(Cal_Xband5b.get())
        cal_Xband6a = float(Cal_Xband6a.get())
        cal_Xband6b = float(Cal_Xband6b.get())

        save_default_file()
        print("*** settings updated! ***")
        check_configfile()

    Button(calibP, text="Confirm", font=("Verdana", 8, "bold"), width=18, height=2, \
           command=calibP_update).grid(row=18, column=0, columnspan=3)

    calibP.mainloop()


def conv_fF():
    global Oo_wood, Oo_RMER, Wtf_wood, Wtf_RMER
    global oo_wood, oo_RMER, wtf_wood, wtf_RMER
    get_last_data()

    conv_f = Toplevel()
    Oo_wood = IntVar()
    Oo_wood.set(checkbox_oo(oo_wood))
    Oo_RMER = IntVar()
    Oo_RMER.set(checkbox_oo(oo_RMER))
    conv_f.title("Conventional model settings")

    Label(conv_f, text="Conventional model settings", font=("Verdana", 11, "bold") \
          , fg="red").grid(row=0, column=0, columnspan=5)
    Label(conv_f, text="    ").grid(row=1, column=2)
    Label(conv_f, text="5 internal models", font=("Verdana", 9), fg="navy").grid(row=2, column=0, columnspan=2)
    Label(conv_f, text="PlumeRise model", font=("Verdana", 9), fg="navy").grid(row=2, column=3, columnspan=2)
    Label(conv_f, text="ON", fg="lime green").grid(row=4, column=0, columnspan=2)

    try:
        with open(PlumeRiseFile + ".txt",encoding="utf-8", errors="surrogateescape") as f:
            wood_con = 1
            wood_status = "ONLINE"
            wood_status_fg = "lime green"
    except EnvironmentError:
        wood_con = 0
        wood_status = "OFFLINE"
        wood_status_fg = "red"
    Label(conv_f, text=wood_status, fg=wood_status_fg).grid(row=4, column=3, columnspan=2)

    Label(conv_f, text="wt factor:").grid(row=5, column=0, sticky=E)
    Wtf_wood = Entry(conv_f, width=7)
    Wtf_wood.grid(row=5, column=4, sticky=W)

    Label(conv_f, text="wt factor:").grid(row=5, column=3, sticky=E)
    Wtf_RMER = Entry(conv_f, width=7)
    Wtf_RMER.grid(row=5, column=1, sticky=W)
    if defsetup == 1:
        Checkbutton(conv_f, text="Include PlumeRise", variable=Oo_wood).grid(row=6, column=3, columnspan=2)
        # FutureVolc setting
    else:
        Checkbutton(conv_f, text="Include PlumeRise", state=DISABLED).grid(row=6, column=3, columnspan=2)
        # global setting
    Checkbutton(conv_f, text="Include 5 internal", variable=Oo_RMER).grid(row=6, column=0, columnspan=2)
    Wtf_RMER.insert(10, str(wtf_RMER))
    Wtf_wood.insert(10, str(wtf_wood))

    def conv_f_update():
        global Oo_wood, Oo_RMER, Wtf_wood, Wtf_RMER
        global oo_wood, oo_RMER, wtf_wood, wtf_RMER
        wtf_RMER = float(Wtf_RMER.get())
        oo_RMER = int(Oo_RMER.get())
        print("5MER on? " + str(oo_RMER))
        wtf_wood = float(Wtf_wood.get())
        oo_wood = int(Oo_wood.get())
        print("Woodhouse on? " + str(oo_wood))
        save_default_file()
        print("*** settings updated! ***")
        check_configfile()

    Label(conv_f, text="  ").grid(row=7, column=2, columnspan=2)

    Button(conv_f, text="Confirm", font=("Verdana", 8), width=18, height=2, \
           command=conv_f_update).grid(row=8, column=1, columnspan=3)

    conv_f.mainloop()


def expe_MERF():
    global oo_isound, Oo_isound, Wtf_isound, wtf_isound  # on/off infrasound
    global oo_esens, Oo_esens, Wtf_esens, wtf_esens  # on/off E-sensors
    global oo_pulsan, Oo_pulsan, Wtf_pulsan, wtf_pulsan  # on/off pulse analysis
    global oo_scatter, Oo_scatter, Wtf_scatter, wtf_scatter  # on/off radar scatter
    get_last_data()

    expe_MER = Toplevel()
    Oo_isound = IntVar()
    Oo_isound.set(checkbox_oo(oo_isound))
    Oo_esens = IntVar()
    Oo_esens.set(checkbox_oo(oo_esens))
    Oo_pulsan = IntVar()
    Oo_pulsan.set(checkbox_oo(oo_pulsan))
    Oo_scatter = IntVar()
    Oo_scatter.set(checkbox_oo(oo_scatter))

    expe_MER.title("Experimental MER settings")

    Label(expe_MER, text="Experimental systems", font=("Verdana", 11, "bold") \
          , fg="purple").grid(row=0, column=0, columnspan=5)
    Label(expe_MER, text="    ").grid(row=1, column=1)
    Label(expe_MER, text="Consider").grid(row=2, column=1)
    Label(expe_MER, text="wt. factor").grid(row=2, column=2)

    Label(expe_MER, text="Infrasound", font=("Verdana", 9)).grid(row=3, column=0)
    Checkbutton(expe_MER, variable=Oo_isound).grid(row=3, column=1)
    Wtf_isound = Entry(expe_MER, width=7)
    Wtf_isound.grid(row=3, column=2)
    Wtf_isound.insert(10, str(wtf_isound))

    Label(expe_MER, text="E-sensors", font=("Verdana", 9)).grid(row=4, column=0)
    Checkbutton(expe_MER, variable=Oo_esens).grid(row=4, column=1)
    Wtf_esens = Entry(expe_MER, width=7)
    Wtf_esens.grid(row=4, column=2)
    Wtf_esens.insert(10, str(wtf_esens))

    Label(expe_MER, text="Pulse analysis", font=("Verdana", 9)).grid(row=5, column=0)
    Checkbutton(expe_MER, variable=Oo_pulsan).grid(row=5, column=1)
    Wtf_pulsan = Entry(expe_MER, width=7)
    Wtf_pulsan.grid(row=5, column=2)
    Wtf_pulsan.insert(10, str(wtf_pulsan))

    Label(expe_MER, text="Radar scattering", font=("Verdana", 9)).grid(row=6, column=0)
    Checkbutton(expe_MER, variable=Oo_scatter).grid(row=6, column=1)
    Wtf_scatter = Entry(expe_MER, width=7)
    Wtf_scatter.grid(row=6, column=2)
    Wtf_scatter.insert(10, str(wtf_scatter))

    Label(expe_MER, text="  ").grid(row=7, column=1)

    def expe_MER_update():
        global oo_isound, Oo_isound, Wtf_isound, wtf_isound
        global oo_esens, Oo_esens, Wtf_esens, wtf_esens
        global oo_pulsan, Oo_pulsan, Wtf_pulsan, wtf_pulsan
        global oo_scatter, Oo_scatter, Wtf_scatter, wtf_scatter
        oo_isound = int(Oo_isound.get())
        print("Infrasound systems: " + str(oo_isound))
        oo_esens = int(Oo_esens.get())
        print("E-sensor systems: " + str(oo_esens))
        oo_pulsan = int(Oo_pulsan.get())
        print("Pulse analysis: " + str(oo_pulsan))
        oo_scatter = int(Oo_scatter.get())
        print("Radar scattering model: " + str(oo_scatter))
        wtf_isound = float(Wtf_isound.get())
        wtf_esens = float(Wtf_esens.get())
        wtf_pulsan = float(Wtf_pulsan.get())
        wtf_scatter = float(Wtf_scatter.get())
        save_default_file()
        print("*** settings updated! ***")
        check_configfile()

    Button(expe_MER, text="Confirm", font=("Verdana", 10, "bold"), fg="red", width=18, height=2, \
           command=expe_MER_update).grid(row=8, column=0, columnspan=3)

    expe_MER.mainloop()


def man_MERF():
    global oo_manual, Oo_manual, Wtf_manual, wtf_manual  # on/off manual MER input
    global Min_manMER, min_manMER, Max_manMER, max_manMER
    global Min_manMER1, Min_manMER10, Max_manMER1, Max_manMER10
    global min_manMER1, min_manMER10, max_manMER1, max_manMER10
    global time_MER_y, time_MER_mo, time_MER_d, time_MER_h, time_MER_m

    TimeNU = datetime.datetime.utcnow()
    TimeNUs = str(TimeNU)
    YearNUs = TimeNUs[:4]
    MonthNUs = TimeNUs[5:7]
    DayNUs = TimeNUs[8:10]
    HourNUs = TimeNUs[11:13]
    MinuteNUs = TimeNUs[14:16]

    man_MER = Toplevel()
    Oo_manual = IntVar()

    man_MER.title("Manual MER input")

    Label(man_MER, text="Time of estimate", font="Helvetica 11", fg="navy").grid(row=0, column=0, columnspan=5)
    Label(man_MER, text="h").grid(row=1, column=0, sticky=E)
    Label(man_MER, text=":").grid(row=2, column=1)
    Label(man_MER, text="min").grid(row=1, column=2, sticky=W)
    Label(man_MER, text="day").grid(row=1, column=3, sticky=E)
    Label(man_MER, text="month").grid(row=1, column=4)
    Label(man_MER, text="year").grid(row=1, column=5, sticky=W)

    time_MER_y = Entry(man_MER, width=4)
    time_MER_y.grid(row=2, column=5, sticky=W)

    time_MER_mo = Entry(man_MER, width=2)
    time_MER_mo.grid(row=2, column=4)

    time_MER_d = Entry(man_MER, width=2)
    time_MER_d.grid(row=2, column=3, sticky=E)

    time_MER_h = Entry(man_MER, width=2)
    time_MER_h.grid(row=2, column=0, sticky=E)
    time_MER_m = Entry(man_MER, width=2)
    time_MER_m.grid(row=2, column=2, sticky=W)

    time_MER_y.insert(10, YearNUs)
    time_MER_mo.insert(10, MonthNUs)
    time_MER_d.insert(10, DayNUs)
    time_MER_h.insert(10, HourNUs)
    time_MER_m.insert(10, MinuteNUs)

    Label(man_MER, text="          ").grid(row=3, column=6)
    Label(man_MER, text="          ").grid(row=8, column=6)

    Label(man_MER, text="Comment:").grid(row=4, column=0, columnspan=4, sticky=W)
    Com_manual = Entry(man_MER, width=25)
    Com_manual.grid(row=5, column=0, columnspan=6, sticky=W)

    Label(man_MER, text="Add MER estimate", font=("Helvetica", 11) \
          , fg="green").grid(row=0, column=7, columnspan=5)
    Label(man_MER, text="   ").grid(row=3, column=8)
    Label(man_MER, text="MIN").grid(row=1, column=7, sticky=E)
    Label(man_MER, text="MAX").grid(row=2, column=7, sticky=E)

    Min_manMER1 = Entry(man_MER, width=7)
    Min_manMER1.grid(row=1, column=8)
    Min_manMER10 = Entry(man_MER, width=3)
    Min_manMER10.grid(row=1, column=10, sticky=W)

    Max_manMER1 = Entry(man_MER, width=7)
    Max_manMER1.grid(row=2, column=8)
    Max_manMER10 = Entry(man_MER, width=3)
    Max_manMER10.grid(row=2, column=10, sticky=W)

    Label(man_MER, text="x10").grid(row=1, column=9)
    Label(man_MER, text="x10").grid(row=2, column=9)
    Label(man_MER, text="kg/s").grid(row=1, column=11, sticky=W)
    Label(man_MER, text="kg/s").grid(row=2, column=11, sticky=W)
    Label(man_MER, text="wt factor", fg="red").grid(row=4, column=8, columnspan=2, sticky=W)
    Wtf_manual = Entry(man_MER, width=8)
    Wtf_manual.grid(row=5, column=8)
    Wtf_manual.insert(10, "0")
    Oo_manual.set(1)

    #  Checkbutton(man_MER, text = "use data", variable= Oo_manual).grid(row=9, column=7,columnspan=2)

    def man_MER_update():
        global oo_manual, Oo_manual, Wtf_manual, wtf_manual  # on/off manual MER input
        global Min_manMER, min_manMER, Max_manMER, max_manMER
        global Min_manMER1, Min_manMER10, Max_manMER1, Max_manMER10
        global min_manMER1, min_manMER10, max_manMER1, max_manMER10
        global time_MER_y, time_MER_mo, time_MER_d, time_MER_h, time_MER_m

        Y_meri = int(time_MER_y.get())
        MO_meri = int(time_MER_mo.get())
        D_meri = int(time_MER_d.get())
        H_meri = int(time_MER_h.get())
        M_meri = int(time_MER_m.get())
        time_MERin = datetime.datetime(Y_meri, MO_meri, D_meri, H_meri, M_meri)
        oo_manual = int(Oo_manual.get())
        print("Considering manual input: " + str(oo_manual))
        wtf_manual = float(Wtf_manual.get())
        min_manMER1 = float(Min_manMER1.get())
        min_manMER10 = float(Min_manMER10.get())
        max_manMER1 = float(Max_manMER1.get())
        max_manMER10 = float(Max_manMER10.get())
        min_manMER = min_manMER1 * 10 ** min_manMER10
        max_manMER = max_manMER1 * 10 ** max_manMER10
        print("manual MER input:")
        print("minimum: " + str(min_manMER))
        print("maximum: " + str(max_manMER))
        comment_merin = str(Com_manual.get())
        try:
            with open("fix_MERin.txt", 'r',encoding="utf-8", errors="surrogateescape") as manMER_FILE_original:
                data = manMER_FILE_original.read()
            with open("fix_MERin.txt", 'w',encoding="utf-8", errors="surrogateescape") as manMER_FILE:
                manMER_FILE.write(str(time_MERin) + "\t" + str(oo_manual) + "\t" + \
                                  str(wtf_manual) + "\t" + str(min_manMER) + "\t" + str(max_manMER) + "\t" + str(
                    "7") + "\t" + \
                                  str("7") + "\t" + str("7") + "\t" + str("7") + "\t" + str(
                    comment_merin) + "\n" + data)
        except:
            manMER_FILE = open("fix_MERin.txt", 'a',encoding="utf-8", errors="surrogateescape")
            manMER_FILE.write(str(time_MERin) + "\t" + str(oo_manual) + "\t" + \
                              str(wtf_manual) + "\t" + str(min_manMER) + "\t" + str(max_manMER) + "\t" + str("7") + "\t" \
                              + str("7") + "\t" + str("7") + "\t" + str("7") + "\t" + str(comment_merin) + "\n")
        manMER_FILE.close()
        save_default_file()
        print("*** settings updated! ***")
        check_configfile()

    Button(man_MER, text="Confirm", font=("Verdana", 8, "bold"), width=18, height=2, \
           command=man_MER_update).grid(row=9, column=0, columnspan=7, sticky=W)

    man_MER.mainloop()


def fmer_modeF():
    global Oo_exp, Oo_con, Wtf_exp, Wtf_con
    global oo_exp, oo_con, wtf_exp, wtf_con
    get_last_data()

    fmer_mode = Toplevel()
    Oo_exp = IntVar()
    Oo_con = IntVar()
    Oo_con.set(checkbox_oo(oo_con))
    Oo_exp.set(checkbox_oo(oo_exp))
    fmer_mode.title("FMER settings")

    Label(fmer_mode, text="FMER settings", font=("Verdana", 11, "bold") \
          , fg="red").grid(row=0, column=0, columnspan=5)
    Label(fmer_mode, text="    ").grid(row=1, column=2)
    Label(fmer_mode, text="Experimental MER", font=("Verdana", 9), fg="dark orange").grid(row=2, column=0, columnspan=2)
    Label(fmer_mode, text="Conventional MER", font=("Verdana", 9), fg="navy").grid(row=2, column=3, columnspan=2)

    Label(fmer_mode, text="wt factor:").grid(row=4, column=0, sticky=E)
    Wtf_exp = Entry(fmer_mode, width=7)
    Wtf_exp.grid(row=4, column=1, sticky=W)

    Label(fmer_mode, text="wt factor:").grid(row=4, column=3, sticky=E)
    Wtf_con = Entry(fmer_mode, width=7)
    Wtf_con.grid(row=4, column=4, sticky=W)

    Checkbutton(fmer_mode, text="Include exp. MER", variable=Oo_exp).grid(row=5, column=0, columnspan=2)
    Checkbutton(fmer_mode, text="Include conv. MER", variable=Oo_con).grid(row=5, column=3, columnspan=2)
    Wtf_con.insert(10, wtf_con)
    Wtf_exp.insert(10, wtf_exp)

    def fmer_mode_update():
        global Oo_exp, Oo_con, Wtf_exp, Wtf_con
        global oo_exp, oo_con, wtf_exp, wtf_con
        oo_exp = int(Oo_exp.get())
        print("Experimental systems: " + str(oo_exp))
        oo_con = int(Oo_con.get())
        print("Conventional MER models: " + str(oo_con))
        wtf_exp = float(Wtf_exp.get())
        wtf_con = float(Wtf_con.get())
        save_default_file()
        print("*** settings updated! ***")
        check_configfile()

    Label(fmer_mode, text="  ").grid(row=6, column=2, columnspan=2)

    Button(fmer_mode, text="Confirm", font=("Verdana", 8), width=18, height=2, \
           command=fmer_mode_update).grid(row=7, column=1, columnspan=3)

    fmer_mode.mainloop()


def operation_control():
    masterklick.title("Operation Control Board - REFIR FIX")
    Label(masterklick, text="Operation Control Board", font=("Verdana", 14, \
                                                             "bold"), fg="navy").grid(row=0, column=0, columnspan=3)
    Label(masterklick, text="Last update of settings by operator:").grid(row=1, column=0)
    Label(masterklick, text="Last plume height input by operator:", fg="red").grid(row=2, column=0)

    Label(masterklick, text="FOXI Control Panels", font=("Verdana", 8, \
                                                         "bold"), fg="forest green").grid(row=4, column=1, columnspan=2)

    label1 = Label(masterklick, textvariable=sTimeUpdate1, bg="snow")

    label2 = Label(masterklick, textvariable=sTimeObs1, fg="red", bg="snow")
    label1.grid(row=1, column=1, sticky=W)
    label2.grid(row=2, column=1, sticky=W)
    Label(masterklick, text="   ", font=("Verdana", 8)).grid(row=3, column=0)
    Label(masterklick, text="Initializing Parameters", font=("Verdana", 8, \
                                                             "bold"), fg="navy").grid(row=4, column=0)

    Button(masterklick, text="QUIT REFIR", \
           font=("Verdana", 10), fg="red", bg="white", width=10, height=2, \
           command=safe_exit).grid(row=2, column=2)

    Button(masterklick, text="Plume Height Sensors", \
           font=("Verdana", 8), fg="green yellow", bg="forest green", width=18, height=2, \
           command=sourcecontrol).grid(row=5, column=1)

    Button(masterklick, text="Conv MER Models", \
           font=("Verdana", 8), fg="green yellow", bg="forest green", \
           width=18, height=2, command=conv_fF).grid(row=5, column=2)

    Button(masterklick, text="Exp. MER Systems", \
           font=("Verdana", 8), fg="green yellow", bg="forest green", \
           width=18, height=2, command=expe_MERF).grid(row=6, column=2)

    Button(masterklick, text="FMER", \
           font=("Verdana", 8), fg="green yellow", bg="forest green", \
           width=18, height=2, command=fmer_modeF).grid(row=7, column=2)

    Button(masterklick, text="Output Control", \
           font=("Verdana", 8), fg="green yellow", bg="forest green", \
           width=18, height=2, command=plot_mode).grid(row=8, column=2)

    Button(masterklick, text="Set Time Base", \
           font=("Verdana", 8), fg="green yellow", bg="forest green", \
           width=18, height=2, command=tb_mode).grid(row=8, column=1)

    Button(masterklick, text="Analysis Mode", \
           font=("Verdana", 8), fg="green yellow", bg="forest green", \
           width=18, height=2, command=analysis_mode).grid(row=7, column=1)

    Button(masterklick, text="Calibration", \
           font=("Verdana", 8), fg="green yellow", bg="forest green", \
           width=18, height=2, command=calibF).grid(row=6, column=1)

    Button(masterklick, text="Set Model Parameters", \
           font=("Verdana", 8), fg="blue2", bg="light steel blue", width=18, height=2, \
           command=default_parameter_panel).grid(row=5, column=0)

    Label(masterklick, text="Include Observations", font=("Verdana", 8, \
                                                          "bold"), fg="red").grid(row=6, column=0)

    Button(masterklick, text="Add Plume Heights", \
           font=("Verdana", 8), fg="red", bg="light steel blue", width=18, height=2, \
           command=add_plhobs).grid(row=7, column=0)

    Button(masterklick, text="Add MER Estimate", \
           font=("Verdana", 8), fg="red", bg="light steel blue", width=18, height=2, \
           command=man_MERF).grid(row=8, column=0)
    Label(masterklick, text="   ", font=("Verdana", 8)).grid(row=9, column=0)
    Label(masterklick, text="Status Overview:", font=("Verdana", 8)).grid(row=10, column=0)
    label3 = Label(masterklick, textvariable=sdefault_txt, bg=bgcol.get())
    label3.grid(row=11, column=0, columnspan=3)
    Label(masterklick, text="   ", font=("Verdana", 8)).grid(row=12, column=0)
    Label(masterklick, text="For citation contact:", font=("Verdana", 8)).grid(row=12, column=0, sticky=W, )

    Label(masterklick, text="Tobias Dürig, tobias.durig@otago.ac.nz; Fabio Dioguardi, fabiod@bgs.ac.uk", font=("Verdana", 8)).grid(row=13, column=0, sticky=W,
                                                                                  columnspan=3)
    masterklick.mainloop()


operation_control()