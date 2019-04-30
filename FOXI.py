"""
*** FOXI v19.0 ***
- component of REFIR 19.0 -
-Near-real time estimates of mass eruption rates and plume heights -
 
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


RNZ180615C 

"""

#REFIR v18 - FOXI 18.1c

from __future__ import division
from __future__ import with_statement
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import figure
import datetime
import math
from copy import deepcopy
import sys
import time
from ftplib import FTP
#import winsound
import locale
import urllib
from urllib.request import urlopen 
import logging
import os
import gc
import shutil
import csv
#import matplotlib.image as image

""" settings START """
global PI_THRESH, TimeOLD

scenario = "      +++ EXERCISE! +++ " # change into " " in real eruption
FOXIversion ="19.0"
operator = "User"
#PI_THRESH = 5.0
time_axis = 1 #0: inverted for pl.h. sector plots; 1: always same

""" settings END """

time_st = datetime.datetime.utcnow()         
time_stamp = time_st.strftime("%Y%m%d_%H%M") 

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

dir1 = os.path.dirname(os.path.abspath(__file__))
try:
    os.makedirs('foxi_log')
    filename = os.path.join(dir1+'/foxi_log', 'refir_%s.log' % time_stamp)
except EnvironmentError:
    filename = os.path.join(dir1+'/foxi_log', 'refir_%s.log' % time_stamp)

if logger == None:
    logger = logging.getLogger()
else:  
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# log to the console
console_handler = logging.StreamHandler()
level = logging.INFO
console_handler.setLevel(level)
formatter = logging.Formatter('%(name)-7s: %(levelname)-8s %(message)s')

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

logging.debug('>> logging initialized...')

logger1 = logging.getLogger('Level01')
logger2 = logging.getLogger('Level02')
logger3 = logging.getLogger('Level03')
logger4 = logging.getLogger('Level04')
logger5 = logging.getLogger('Level05')
logger6 = logging.getLogger('Level06')
logger7 = logging.getLogger('Level07')
logger8 = logging.getLogger('Level08')
logger9 = logging.getLogger('Level09')
logger10 = logging.getLogger('Level10')

out_txt ="default_fox.txt"
lead_Time=0
run=0
steptime=5 #minutes between each loop
passwort ="*****"

dt_sec = 0
timin_sec_cum = 0

woodhlink = "http://www.maths.bris.ac.uk/~mw9428/PlumeRiseQH/FutureVolcSys/PlumeRise_REFIR.txt"
timebase = 30
analysis = 0 # Analysis mode will calculate individual MER for all models and time bases

Freq = 2500 # Set Frequency To 2500 Hertz
Dur = 100 # Set Duration To 1000 ms == 1 second
Dur2 = 200 # Set Duration To 1000 ms == 1 second

ID = ["n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a."]
sens_file = ["","","","","","","","","","","","","","","","","",""]
sens_IP = ["","","","","","","","","","","","","","","","","",""]
sens_dir = ["","","","","","","","","","","","","","","","","",""]
sens_url = ["","","","","","","","","","","","","","","","","",""]

N_en,N_en1,N_en2=0,0,0

plt.ioff()
Cband1_stack = []
Cband2_stack = []
Cband3_stack = []
Cband4_stack = []
Cband5_stack = []
Cband6_stack = []

Xband1_stack = []
Xband2_stack = []
Xband3_stack = []
Xband4_stack = []
Xband5_stack = []
Xband6_stack = []

Cam1_stack = []
Cam2_stack = []
Cam3_stack = []
Cam4_stack = []
Cam5_stack = []
Cam6_stack = []

air_stack = []
ground_stack = []
other_stack = []

Cband1_t_stack = []
Cband2_t_stack = []
Cband3_t_stack = []
Cband4_t_stack = []
Cband5_t_stack = []
Cband6_t_stack = []

Xband1_t_stack = []
Xband2_t_stack = []
Xband3_t_stack = []
Xband4_t_stack = []
Xband5_t_stack = []
Xband6_t_stack = []

Cam1_t_stack = []
Cam2_t_stack = []
Cam3_t_stack = []
Cam4_t_stack = []
Cam5_t_stack = []
Cam6_t_stack = []

air_t_stack = []
ground_t_stack = []
other_t_stack = []
APHmax_y = 0

hbe_min_sum = 0
hbe_sum = 0
hbe_max_sum = 0
Qfmer_min_sum =0
Qfmer_sum = 0
Qfmer_max_sum = 0
ndata = 0
nsources = 0

def calculate_position(self,x, y):
# Function that control the position of the widget in the screen
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    pos_x = x * screen_width
    pos_y = y * screen_height
    return (pos_x, pos_y)


def read_sensors():
    """reads IDs and GPS coordinates from *.ini files"""
    global ID,sens_file,N_en,N_en1,N_en2,sens_url,sens_IP,sens_dir
    try:
        #C-band
        fnCb= os.path.join(dir1+'/refir_config','Cband.ini')
        with open (fnCb,encoding="utf-8", errors="surrogateescape") as f:
            lines =f.readlines()
            Cse = []
            for l in lines:
               Cse.append(l.strip().split("\t"))
        f.close()
        N_en = len(Cse)-1 #number of entries
        
        if N_en < 1:
            print("\nNo C-band radar sensors assigned!\n")
        else:
            for x in range(0,N_en):
                    ID[x] = str(Cse[x+1][0])
                    sens_file[x] = str(Cse[x+1][6])
                    sens_url[x] = str(Cse[x+1][7])
                    try:
                        sens_IP[x] = str(Cse[x+1][8])
                        sens_dir[x] = str(Cse[x+1][9])                    
                    except IndexError:
                        hg=0
    except  EnvironmentError:
        print("Error - \".ini\" sensor file not found!\n")

    try:
        #X-band
        fnXb= os.path.join(dir1+'/refir_config','Xband.ini')
        with open (fnXb,encoding="utf-8", errors="surrogateescape") as f:
            lines =f.readlines()
            Dse = []
            for l in lines:
               Dse.append(l.strip().split("\t"))
        f.close()
        N_en2 = len(Dse)-1 #number of entries
        if N_en2 < 1:
            print("\nNo X-band radar sensors assigned!\n")
        else:
            for x in range(0,N_en2):
                    ID[x+6] = str(Dse[x+1][0])
                    sens_file[x+6] = str(Dse[x+1][6])
                    sens_url[x+6] = str(Dse[x+1][7])
                    try:
                        sens_IP[x+6] = str(Dse[x+1][8])
                        sens_dir[x+6] = str(Dse[x+1][9])
                    except IndexError:
                        hg=2
    except  EnvironmentError:
        print("Error - \".ini\" sensor file not found!\n")
    try:
        #Cams
        fnCam= os.path.join(dir1+'/refir_config','Cam.ini')
        with open (fnCam,encoding="utf-8", errors="surrogateescape") as f:
            lines =f.readlines()
            Ase = []
            for l in lines:
               Ase.append(l.strip().split("\t"))
        f.close()
        N_en1 = len(Ase)-1 #number of entries
        if N_en1 < 1:
            print("\nNo webcams assigned!\n")
        else:
            for x in range(0,N_en1):
                    ID[x+12] = str(Ase[x+1][0])
                    sens_file[x+12] = str(Ase[x+1][6])
                    sens_url[x+12] = str(Ase[x+1][7])
                    try:
                        sens_IP[x+12] = str(Ase[x+1][8])
                        sens_dir[x+12] = str(Ase[x+1][9])
                    except IndexError:
                        hg=3
    except  EnvironmentError:
        print("Error - \".ini\" sensor file not found!\n")
    
read_sensors()

try:
    if sys.version_info[0] < 3:
        from Tkinter import *
    
    else:
        from tkinter import *

#GUI INITIALIZING
    
    TimeNUNA = datetime.datetime.utcnow()
    TimeNUNAs = str(TimeNUNA)
    YearNUNAs = TimeNUNAs[:4] 
    MonthNUNAs =TimeNUNAs[5:7]
    DayNUNAs =TimeNUNAs[8:10]
    HourNUNAs =TimeNUNAs[11:13]
    MinuteNUNAs =TimeNUNAs[14:16]
    
    masterout = Tk()
    out=StringVar()
    time_lead = IntVar()
    
    masterout.title("Initiate FOXI")
    Label(masterout, text="Specify output file and start of eruption",\
     font = "Helvetica 12", fg="blue").grid(row=0, column=0, columnspan=6)
    
    Label(masterout, text=" ", font = "Helvetica 10").grid(row=2, column=0)
    Label(masterout, text="Output file: ", font = "Helvetica 10").grid(row=3, column=0, columnspan=2,sticky=E)
    
    Label(masterout, text="Start of eruption: ", \
    font = "Helvetica 11", fg="green").grid(row=5, column=0, columnspan =2, sticky=W)
    Label(masterout, text="Year: ", font = "Helvetica 10").grid(row=5, column=2)
    Label(masterout, text="Month: ", font = "Helvetica 10").grid(row=6, column=2)
    Label(masterout, text="Day: ", font = "Helvetica 10").grid(row=6, column=0)
    Label(masterout, text="Hour: ", font = "Helvetica 10").grid(row=7, column=0)
    Label(masterout, text="Minute: ", font = "Helvetica 10").grid(row=7, column=2)

    Label(masterout, text=".txt", font = "Helvetica 10").grid(row=3,column=4, sticky=W)
    Label(masterout, text=" ", font = "Helvetica 10").grid(row=4, column=0)
    Label(masterout, text=" ", font = "Helvetica 10").grid(row=8, column=0)
    Label(masterout, text="IMPORTANT! Program starts not before window is closed!",\
    fg="red", bg="yellow").grid(row=9,column=0, sticky=W, columnspan=5)
    Label(masterout, text=" ", font = "Helvetica 10").grid(row=10, column=0)
    
    out = Entry(masterout)
    out.grid(row=3, column=2, columnspan=2, sticky=W)
    
    time_ERU_y = Entry(masterout,width=4)
    time_ERU_y.grid(row=5, column=3, sticky=W)
    time_ERU_mo = Entry(masterout,width=2)
    time_ERU_mo.grid(row=6, column=3, sticky=W)
    time_ERU_d = Entry(masterout,width=2)
    time_ERU_d.grid(row=6, column=1, sticky=W)
    time_ERU_h = Entry(masterout,width=2)
    time_ERU_h.grid(row=7, column=1, sticky=W)
    time_ERU_m = Entry(masterout,width=2)
    time_ERU_m.grid(row=7, column=3, sticky=W)
    
    time_ERU_y.insert(10,YearNUNAs)
    time_ERU_mo.insert(10,MonthNUNAs)
    time_ERU_d.insert(10,DayNUNAs)
    time_ERU_h.insert(10,HourNUNAs)
    time_ERU_m.insert(10,MinuteNUNAs)
    
    def on_button():
        global out_txt,lead_Time, time_tveir
        out_txt = str(out.get())
        Y_eru = int(time_ERU_y.get())
        MO_eru = int(time_ERU_mo.get())
        D_eru = int(time_ERU_d.get())
        H_eru = int(time_ERU_h.get())
        M_eru = int(time_ERU_m.get())
        time_tveir = datetime.datetime(Y_eru,MO_eru,D_eru,H_eru,M_eru)
        time_einn = datetime.datetime(int(YearNUNAs), int(MonthNUNAs), int(DayNUNAs), int(HourNUNAs),int(MinuteNUNAs))
        lead_Time = int((time_einn-time_tveir).total_seconds()/60)
        logging.info("Time since eruption start: " + str(lead_Time)+"min")
        logging.info("Configuration completed!")
        logging.info("Waiting for Initiation")
    
    Button(masterout, text = "Initiate!",font = "Helvetica 11", fg="yellow",bg="red",\
    width =24, height=2, command = on_button).grid(row=11, column=0, columnspan=5)
    x_screen_fr = 0.6
    y_screen_fr = 0.2
    size_x = 310
    size_y = 300
    pos_x, pos_y = calculate_position(masterout,x_screen_fr, y_screen_fr)
    masterout.geometry('%dx%d+%d+%d' % (size_x, size_y, pos_x, pos_y))
    masterout.mainloop()

#END GUI

except EnvironmentError:
    out_txt = input ("Enter name of output file (without .txt): ")
    lead_Time_d = input ("Days since start of eruption: ")
    lead_Time_h = input ("Hours since start of eruption: ")
    lead_Time_m = input ("Minutes since start of eruption: ")
    lead_Time =24*60*lead_Time_d + 60*lead_Time_h+lead_Time_m

fMER_file = open(out_txt + "_FMER.txt", "a",encoding="utf-8", errors="surrogateescape")
fMER_file.write('Time UTC'+"\t" + 'Minutes since t0' + "\t" + 'FMER min'+"\t"+'FMER avg'+"\t"+'FMER max'+"\n")
fMER_file.close()
PLH_file = open(out_txt + "_PLH.txt", "a",encoding="utf-8", errors="surrogateescape")
PLH_file.write('Time UTC'+"\t" + 'Minutes since t0' + "\t" + 'PLH min'+"\t"+'PLH avg'+"\t"+'PLH max'+"\n")
PLH_file.close()
PLH_avg_file = open(out_txt + "_tavg_PLH.txt", "a",encoding="utf-8", errors="surrogateescape")
PLH_avg_file.write('Time UTC'+"\t" + 'Minutes since t0' + "\t" + 'PLH min'+"\t"+'PLH avg'+"\t"+'PLH max'+"\n")
PLH_avg_file.close()
FMER_avg_file = open(out_txt + "_tavg_FMER.txt", "a",encoding="utf-8", errors="surrogateescape")
FMER_avg_file.write('Time UTC'+"\t" + 'Minutes since t0' + "\t" + 'FMER min'+"\t"+'FMER avg'+"\t"+'FMER max'+"\n")
FMER_avg_file.close()
NAME_file_avg = open(out_txt + "_NAME_sources_avg.txt", "a",encoding="utf-8", errors="surrogateescape")
NAME_file_writer = csv.writer(NAME_file_avg,delimiter = ',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
NAME_file_writer.writerow(['Sources:'])
NAME_file_writer.writerow(['Name','Z','dZ','Source Strength','Start Time','Stop Time'])
NAME_file_avg.close()
NAME_file_max = open(out_txt + "_NAME_sources_max.txt", "a",encoding="utf-8", errors="surrogateescape")
NAME_file_writer = csv.writer(NAME_file_max,delimiter = ',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
NAME_file_writer.writerow(['Sources:'])
NAME_file_writer.writerow(['Name','Z','dZ','Source Strength','Start Time','Stop Time'])
NAME_file_max.close()
NAME_file_min = open(out_txt + "_NAME_sources_min.txt", "a",encoding="utf-8", errors="surrogateescape")
NAME_file_writer = csv.writer(NAME_file_min,delimiter = ',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
NAME_file_writer.writerow(['Sources:'])
NAME_file_writer.writerow(['Name','Z','dZ','Source Strength','Start Time','Stop Time'])
NAME_file_min.close()

# Elaborate automatically retrieved weather data
def elaborate_weather(plume_height):
    global P_H_source
    global T_H_source
    global N_avg
    global V_avg
    global N_avg
    global V_H_top
    global Ws
    sys.path.insert(0, './weather')
    from weather import calc_wt_par, retrieve_data
    from calc_wt_par import weather_parameters
    from retrieve_data import gfs_forecast_retrieve
    from shutil import move

    cwd=os.getcwd()
    year_vals = YearNOWs
    month_vals = MonthNOWs
    day_vals = DayNOWs
    hour_vals = HourNOWs
    if run_type == 1:
        #folder_name=cwd+"\\raw_weather_data_"+YearNUNAs+MonthNUNAs+DayNUNAs
        folder_name = os.path.join(cwd,"raw_forecast_weather_data_"+YearNUNAs+MonthNUNAs+DayNUNAs)

        #abs_validity = YearNUNAs + MonthNUNAs + DayNUNAs + HourNUNAs
        #year_vals = YearNUNAs
        #month_vals = MonthNUNAs
        #day_vals = DayNUNAs
        #hour_vals = HourNUNAs
    else:
        #folder_name = cwd + "\\raw_weather_data_" + eruption_start_year + eruption_start_month + eruption_start_day
        folder_name = os.path.join(cwd,"raw_reanalysis_weather_data_"+ eruption_start_year + eruption_start_month + eruption_start_day)
        #year_vals = YearNOWs
        #month_vals = MonthNOWs
        #day_vals = DayNOWs
        #hour_vals = HourNOWs

    abs_validity = year_vals + month_vals + day_vals + hour_vals

    if os.path.exists(folder_name):
        profile_data_file = "profile_data_" + abs_validity + ".txt"
        #profile_data_file_full = folder_name+"\\"+profile_data_file
        profile_data_file_full = os.path.join(folder_name,profile_data_file)
        if os.path.exists(profile_data_file_full):
            print("Elaborating "+profile_data_file)
            [P_H_source, T_H_source, N_avg, V_avg, N_avg, V_H_top, Ws] = weather_parameters(year_vals,month_vals,day_vals,abs_validity,profile_data_file_full,plume_height,vent_h)
        else:
            print("File " + profile_data_file + " not present")
            if run_type == 1:
                print('Retrieving new GFS forecast data')
                gfs_forecast_retrieve(volcLON, volcLAT)
                current = os.getcwd()
                files = os.listdir(current)
                for file in files:
                    if file.startswith('weather_') or file.startswith('profile_'):
                        move(os.path.join(current, file), os.path.join(folder_name, file))
                print("Elaborating " + profile_data_file)
                [P_H_source, T_H_source, N_avg, V_avg, N_avg, V_H_top, Ws] = weather_parameters(year_vals, month_vals,
                                                                                                day_vals, abs_validity,
                                                                                                profile_data_file_full,
                                                                                                plume_height, vent_h)
            else:
                for itstep in range(1,6):
                    Time_updated = TimeNOW - datetime.timedelta(hours=itstep)
                    year_vals = str(Time_updated.year)
                    month_vals = str(Time_updated.month)
                    if len(month_vals) == 1:
                        month_vals = '0' + month_vals
                    day_vals = str(Time_updated.day)
                    if len(day_vals) == 1:
                        day_vals = '0' + day_vals
                    hour_vals = str(Time_updated.hour)
                    if len(hour_vals) == 1:
                        hour_vals = '0' + hour_vals
                    abs_validity = year_vals + month_vals + day_vals + hour_vals
                    profile_data_file = "profile_data_" + abs_validity + ".txt"
                    print("Searching for " + profile_data_file)
                    #profile_data_file_full = folder_name + "\\" + profile_data_file
                    profile_data_file_full = os.path.join(folder_name,profile_data_file)
                    if os.path.exists(profile_data_file_full):
                        print("Elaborating " + profile_data_file)
                        [P_H_source, T_H_source, N_avg, V_avg, N_avg, V_H_top, Ws] = weather_parameters(year_vals,
                                                                                                    month_vals,
                                                                                                    day_vals,
                                                                                                    abs_validity,
                                                                                                    profile_data_file_full,
                                                                                                    plume_height,
                                                                                                    vent_h)
                        break
                    else:
                        print("File " + profile_data_file + " not present")
                        continue
                else:
                    print("No weather data available. Please run FIX")
    else:
        print("No weather data available. Please run FIX")

Mwood = [0,0,0,0,0] 
wemer_min=0
wemer_avg=0
wemer_max=0

mwmer_max=0
mwmer_avg=0
mwmer_min=0

#default values for plot mode settings
PM_Nplot = 1
PM_PHplot = 1
PM_MERplot= 1
PM_TME= 1
PM_FMERplot = 1
PM_FTME = 1
PM_TAV = 0
NAME_out_on = 0
StatusR_oo = 1
skipFMER = 9

def init_dial():
    logger1.info(" ")
    logger1.info("*** FOXI initiated ***")
    logger1.info("name of output file: " + out_txt)
    logger1.info("lead time: " + str(lead_Time) + " minutes")
    logger1.info(" ")
    logger1.info("*** step 1 successful ***")

init_dial()

hires_tiba = 0 #if FOXI in Auto30 mode has switched to 15 this variable gets 15

EQcode = 0
MQcode = 0

Min_DiaOBSold = 0
Max_DiaOBSold = 0

TStartSim = datetime.datetime.utcnow()
#HERE BEGIN of while loop!
mins = 0

def refir_end():
    import os
    import datetime
    import shutil
    import sys
    TimeNUNA = datetime.datetime.utcnow()
    TimeNUNAs = str(TimeNUNA)
    YearNUNAs = TimeNUNAs[:4]
    MonthNUNAs = TimeNUNAs[5:7]
    DayNUNAs = TimeNUNAs[8:10]
    HourNUNAs = TimeNUNAs[11:13]
    MinuteNUNAs = TimeNUNAs[14:16]
    rundir = "run_" + YearNUNAs + MonthNUNAs + DayNUNAs + HourNUNAs + MinuteNUNAs
    os.mkdir(rundir)
    print("REFIR is going to stop")
    file_list = os.listdir(os.getcwd())
    rundir_path = os.path.join(dir1, rundir)
    for file_to_move in file_list:
        if os.path.isfile(file_to_move):
#            if (file_to_move.startswith("fix_config")):
#                shutil.copy(file_to_move, rundir_path)
            if (file_to_move.endswith(".txt") or file_to_move.endswith(".png") or file_to_move.endswith(".svg")):
                shutil.move(file_to_move, rundir_path)
        elif os.path.isdir(file_to_move):
            if (file_to_move.startswith("raw")):
                shutil.move(file_to_move, rundir_path)
    sys.exit()
    ("\n --- programm aborted")

while 1:

    run = run +1
    
    verz = 0

    # TimeNOW = datetime.datetime.utcnow()
    # if run == 1:
    #     timin = lead_Time
    # else:
    #     timin = int((TimeNOW-time_tveir).total_seconds()/60)

    try:
        
        configfile = open("fix_config.txt", "r",encoding="utf-8", errors="surrogateescape")
        configlines = configfile.readlines()
        configfile.close()
        checkfile = 1
        logger2.info("***** step 2 successful *****")
    
    
    except EnvironmentError:
        checkfile = 0
        logger2.error("!!!Error 02!!!")
        logger2.error(">>> NO CONFIGURATION FILE FOUND!")    
        logger2.error("Please look for file named fix_config.txt")
        logger2.error(" or use Refir FIX to generate it!")
        logger2.error("!! Program aborted !!")
        logger2.error("----------------------------------")

    vulkan = int(configlines[0])
    time_update = configlines[1]
    time_OBS = configlines[2]
    Hmin_obs = float(configlines[3])
    Hmax_obs = float(configlines[4])
    OBS_on = int(configlines[5])
    qf_OBS = int(configlines[6])
    theta_a0 = float(configlines[7])
    P_0 = float(configlines[8])
    theta_0 = float(configlines[9])
    rho_dre = float(configlines[10])
    alpha = float(configlines[11])
    beta = float(configlines[12])
    wtf_wil = float(configlines[13])
    wtf_spa = float(configlines[14])
    wtf_mas = float(configlines[15])
    wtf_mtg = float(configlines[16])
    wtf_deg = float(configlines[17])
    wtf_wood0d = float(configlines[165])
    H1 = float(configlines[18])
    H2 = float(configlines[19])
    tempGrad_1 = float(configlines[20])
    tempGrad_2 = float(configlines[21])
    tempGrad_3 = float(configlines[22])
    Vmax = float(configlines[23])
    ki = float(configlines[24])
    qfak_ISKEF = int(configlines[25])
    qfak_ISEGS = int(configlines[26])
    qfak_ISX1 = int(configlines[27])
    qfak_ISX2 = int(configlines[28])
    qfak_GFZ1 = int(configlines[29])
    qfak_GFZ2 = int(configlines[30])
    qfak_GFZ3 = int(configlines[31])
    unc_ISKEF = float(configlines[32])
    unc_ISEGS = float(configlines[33])
    unc_ISX1 = float(configlines[34])
    unc_ISX2 = float(configlines[35])
    vent_h = float(configlines[36])
    ISKEF_on = int(configlines[37])
    ISEGS_on = int(configlines[38])
    ISX1_on = int(configlines[39])
    ISX2_on = int(configlines[40])
    GFZ1_on = int(configlines[41])
    GFZ2_on = int(configlines[42])
    GFZ3_on = int(configlines[43])
    analysis= int(configlines[44])
    timebase= int(configlines[45])
    oo_exp= int(configlines[46])
    oo_con= int(configlines[47])
    wtf_exp= float(configlines[48])
    wtf_con= float(configlines[49])
    oo_manual= int(configlines[50])
    wtf_manual= float(configlines[51])
    min_manMER= float(configlines[52])
    max_manMER= float(configlines[53])
    oo_wood= int(configlines[54])
    oo_5MER= int(configlines[55])
    wtf_wood= float(configlines[56])
    wtf_5MER= float(configlines[57])
    oo_isound= int(configlines[58])
    wtf_isound= float(configlines[59])
    oo_esens= int(configlines[60])
    wtf_esens= float(configlines[61])
    oo_pulsan= int(configlines[62])
    wtf_pulsan= float(configlines[63])
    oo_scatter= int(configlines[64])
    wtf_scatter= float(configlines[65])
    cal_ISKEF_a= float(configlines[66])
    cal_ISKEF_b= float(configlines[67])
    cal_ISEGS_a= float(configlines[68])
    cal_ISEGS_b= float(configlines[69])
    cal_ISX1_a= float(configlines[70])
    cal_ISX1_b= float(configlines[71])
    cal_ISX2_a= float(configlines[72])
    cal_ISX2_b= float(configlines[73])
    ISKEFm_on = int(configlines[74])
    ISEGSm_on = int(configlines[75])
    ISX1m_on = int(configlines[76])
    ISX2m_on = int(configlines[77])
    PM_Nplot = int(configlines[78])
    PM_PHplot = int(configlines[79])
    PM_MERplot= int(configlines[80])
    PM_TME= int(configlines[81])
    PM_FMERplot = int(configlines[82])
    PM_FTME = int(configlines[83])
    StatusR_oo = int(configlines[84])    
    qfak_Cband3 = float(configlines[87])
    qfak_Cband4 = float(configlines[88])
    qfak_Cband5 = float(configlines[89])
    qfak_Cband6 = float(configlines[90])
    qfak_Xband3 = float(configlines[91])
    qfak_Xband4 = float(configlines[92])
    qfak_Xband5 = float(configlines[93])
    qfak_Xband6 = float(configlines[94])
    qfak_Cam4 = float(configlines[95])
    qfak_Cam5 = float(configlines[96])
    qfak_Cam6 = float(configlines[97])
    unc_Cband3 = float(configlines[98])
    unc_Cband4 = float(configlines[99])
    unc_Cband5 = float(configlines[100])
    unc_Cband6 = float(configlines[101])
    unc_Xband3 = float(configlines[102])
    unc_Xband4 = float(configlines[103])
    unc_Xband5 = float(configlines[104])
    unc_Xband6 = float(configlines[105])
    Cband3_on = float(configlines[106])
    Cband4_on = float(configlines[107])
    Cband5_on = float(configlines[108])
    Cband6_on = float(configlines[109])
    Xband3_on = float(configlines[110])
    Xband4_on = float(configlines[111])
    Xband5_on = float(configlines[112])
    Xband6_on = float(configlines[113])
    Cam4_on = float(configlines[114])
    Cam5_on = float(configlines[115])
    Cam6_on = float(configlines[116])
    Cband3m_on = float(configlines[117])
    Cband4m_on = float(configlines[118])
    Cband5m_on = float(configlines[119])
    Cband6m_on = float(configlines[120])
    Xband3m_on = float(configlines[121])
    Xband4m_on = float(configlines[122])
    Xband5m_on = float(configlines[123])
    Xband6m_on = float(configlines[124])
    Cam4m_on = float(configlines[125])#not used
    Cam5m_on = float(configlines[126])#not used
    Cam6m_on = float(configlines[127])#not used
    cal_Cband3a = float(configlines[128])
    cal_Cband3b = float(configlines[129])
    cal_Cband4a = float(configlines[130])
    cal_Cband4b = float(configlines[131])
    cal_Cband5a = float(configlines[132])
    cal_Cband5b = float(configlines[133])
    cal_Cband6a = float(configlines[134])
    cal_Cband6b = float(configlines[135])
    cal_Xband3a = float(configlines[136])
    cal_Xband3b = float(configlines[137])
    cal_Xband4a = float(configlines[138])
    cal_Xband4b = float(configlines[139])
    cal_Xband5a = float(configlines[140])
    cal_Xband5b = float(configlines[141])
    cal_Xband6a = float(configlines[142])
    cal_Xband6b = float(configlines[143])
    loc_ISKEF= float(configlines[144])
    loc_ISEGS= float(configlines[145])
    loc_Cband3= float(configlines[146])
    loc_Cband4= float(configlines[147])
    loc_Cband5= float(configlines[148])
    loc_Cband6= float(configlines[149])
    loc_ISX1= float(configlines[150])
    loc_ISX2= float(configlines[151]) 
    loc_Xband3= float(configlines[152])
    loc_Xband4= float(configlines[153])
    loc_Xband5= float(configlines[154])
    loc_Xband6= float(configlines[155]) 
    loc_GFZ1= float(configlines[156])
    loc_GFZ2= float(configlines[157])
    loc_GFZ3= float(configlines[158])
    loc_Cam4= float(configlines[159])
    loc_Cam5= float(configlines[160])
    loc_Cam6= float(configlines[161])
    defsetup= int(configlines[162])
    run_type = int(configlines[163])
    weather = int(configlines[164])
    wtf_wood0d = float(configlines[165])
    time_start = configlines[166]
    time_stop = configlines[167]
    exit_param = int(configlines[168])
    PM_TAV = int(configlines[169])
    NAME_out_on = int(configlines[170])
    PI_THRESH = float(configlines[171])

    if exit_param == 1:
        refir_end()

    mins = mins + steptime
    if run_type == 1:
        TimeNOW = datetime.datetime.utcnow()
        TimeNOWs = str(TimeNOW)
        YearNOWs = TimeNOWs[:4]
        MonthNOWs = TimeNOWs[5:7]
        DayNOWs = TimeNOWs[8:10]
        HourNOWs = TimeNOWs[11:13]
        MinuteNOWs = TimeNOWs[14:16]
        HourNOW = int(HourNOWs)
    else:
        eruption_start = datetime.datetime.strptime(time_start, "%Y-%m-%d %H:%M:%S\n")
        eruption_start_year = str(eruption_start.year)
        eruption_start_month = str(eruption_start.month)
        if len(eruption_start_month) == 1:
            eruption_start_month = '0' + eruption_start_month
        eruption_start_day = str(eruption_start.day)
        if len(eruption_start_day) == 1:
            eruption_start_day = '0' + eruption_start_day
        eruption_stop = datetime.datetime.strptime(time_stop, "%Y-%m-%d %H:%M:%S\n")
        TimeNOW = eruption_start + datetime.timedelta(minutes=mins)
        TimeNOWs = str(TimeNOW)
        YearNOWs = TimeNOWs[:4]
        MonthNOWs = TimeNOWs[5:7]
        DayNOWs = TimeNOWs[8:10]
        HourNOWs = TimeNOWs[11:13]
        MinuteNOWs = TimeNOWs[14:16]
        HourNOW = int(HourNOWs)
        if TimeNOW > eruption_stop:
            print("Eruption ended")
            refir_end()
        lead_Time = 0

    if run_type == 1:
        if run == 1:
#            timin = lead_Time
            TimeOLD = TimeNOW
        timin = int((TimeNOW-time_tveir).total_seconds()/60)
    else:
        timin = int((TimeNOW-eruption_start).total_seconds()/60)
        if run == 1:
            TimeOLD = eruption_start
    dt_sec = (TimeNOW - TimeOLD).total_seconds()

    fndb= os.path.join(dir1+'/refir_config','volc_database.ini')
    volcLAT, volcLON=\
    np.loadtxt(fndb, skiprows=2, usecols=(1,2), unpack=True, delimiter='\t')
    try:
        volcLAT = volcLAT[vulkan]
        volcLON = volcLON[vulkan]
    except  IndexError:
        #only one entry in volcdatabase
        huj=0
        
    if float(configlines[86]) == 0:
        Min_DiaOBS = Min_DiaOBSold 
        Max_DiaOBS = Max_DiaOBSold 
    else:
        Min_DiaOBS = float(configlines[85])*1000 
        Max_DiaOBS = float(configlines[86])*1000 
    if timebase == -1:
        TIMEBASE = 30 - hires_tiba
    else:
        TIMEBASE = timebase
        hires_tiba = 0
        
        
    logger2.debug("")
    logger2.debug("+++++++++++++++++++++++++++++++++")
    logger2.debug("Input parameters from config file:")
    logger2.debug("---------------------------------")
    logger2.debug("vulkan"+"\t"+str(vulkan))
    logger2.debug("vent_h"+"\t"+str(vent_h))
    logger2.debug("time_OBS"+"\t"+str(time_OBS))
    logger2.debug("Hmin_obs"+"\t"+str(Hmin_obs))
    logger2.debug("Hmax_obs"+"\t"+str(Hmax_obs))
    logger2.debug("OBS_on"+"\t"+str(OBS_on))
    logger2.debug("qf_OBS"+"\t"+str(qf_OBS))
    logger2.debug("theta_a0"+"\t"+str(theta_a0))
    logger2.debug("P_0"+"\t"+str(P_0))
    logger2.debug("theta_0"+"\t"+str(theta_0))
    logger2.debug("rho_dre"+"\t"+str(rho_dre))
    logger2.debug("alpha"+"\t"+str(alpha))
    logger2.debug("beta"+"\t"+str(beta))
    logger2.debug("H1"+"\t"+str(H1))    
    logger2.debug("H2"+"\t"+str(H2))   
    logger2.debug("tempGrad_1"+"\t"+str(tempGrad_1))
    logger2.debug("tempGrad_2"+"\t"+str(tempGrad_2))
    logger2.debug("tempGrad_3"+"\t"+str(tempGrad_3))
    logger2.debug("Vmax"+"\t"+str(Vmax))
        
    logger2.debug("--------------stream data accuracy------------")
    logger2.debug("qfak_ISKEF"+"\t"+str(qfak_ISKEF))    
    logger2.debug("qfak_ISEGS"+"\t"+str(qfak_ISEGS))  
    logger2.debug("qfak_Cband3"+"\t"+str(qfak_Cband3))
    logger2.debug("qfak_Cband4"+"\t"+str(qfak_Cband4))
    logger2.debug("qfak_Cband5"+"\t"+str(qfak_Cband5))
    logger2.debug("qfak_Cband6"+"\t"+str(qfak_Cband6))
    logger2.debug("qfak_ISX1"+"\t"+str(qfak_ISX1))
    logger2.debug("qfak_ISX2"+"\t"+str(qfak_ISX2))
    logger2.debug("qfak_Xband3"+"\t"+str(qfak_Xband3))
    logger2.debug("qfak_Xband4"+"\t"+str(qfak_Xband4))
    logger2.debug("qfak_Xband5"+"\t"+str(qfak_Xband5))
    logger2.debug("qfak_Xband6"+"\t"+str(qfak_Xband6))
    logger2.debug("qfak_GFZ1"+"\t"+str(qfak_GFZ1))
    logger2.debug("qfak_GFZ2"+"\t"+str(qfak_GFZ2))    
    logger2.debug("qfak_GFZ3"+"\t"+str(qfak_GFZ3))
    logger2.debug("qfak_Cam4"+"\t"+str(qfak_Cam4))
    logger2.debug("qfak_Cam5"+"\t"+str(qfak_Cam5))
    logger2.debug("qfak_Cam6"+"\t"+str(qfak_Cam6)) 
    logger2.debug("unc_ISKEF"+"\t"+str(unc_ISKEF))
    logger2.debug("unc_ISEGS"+"\t"+str(unc_ISEGS))
    logger2.debug("unc_Cband3"+"\t"+str(unc_Cband3))
    logger2.debug("unc_Cband4"+"\t"+str(unc_Cband4))
    logger2.debug("unc_Cband5"+"\t"+str(unc_Cband5))
    logger2.debug("unc_Cband6"+"\t"+str(unc_Cband6))   
    logger2.debug("unc_ISX1"+"\t"+str(unc_ISX1))
    logger2.debug("unc_ISX2"+"\t"+str(unc_ISX2))    
    logger2.debug("unc_Xband3"+"\t"+str(unc_Xband3))
    logger2.debug("unc_Xband4"+"\t"+str(unc_Xband4))
    logger2.debug("unc_Xband5"+"\t"+str(unc_Xband5))
    logger2.debug("unc_Xband6"+"\t"+str(unc_Xband6))

    logger2.debug("--------------sensor locations------------")
    logger2.debug("loc_ISKEF"+"\t"+str(loc_ISKEF))
    logger2.debug("loc_ISEGS"+"\t"+str(loc_ISEGS))
    logger2.debug("loc_Cband3"+"\t"+str(loc_Cband3))
    logger2.debug("loc_Cband4"+"\t"+str(loc_Cband4))
    logger2.debug("loc_Cband5"+"\t"+str(loc_Cband5))
    logger2.debug("loc_Cband6"+"\t"+str(loc_Cband6))   
    logger2.debug("loc_ISX1"+"\t"+str(loc_ISX1))
    logger2.debug("loc_ISX2"+"\t"+str(loc_ISX2))    
    logger2.debug("loc_Xband3"+"\t"+str(loc_Xband3))
    logger2.debug("loc_Xband4"+"\t"+str(loc_Xband4))
    logger2.debug("loc_Xband5"+"\t"+str(loc_Xband5))
    logger2.debug("loc_Xband6"+"\t"+str(loc_Xband6))
    
    logger2.debug("--------------sensor settings------------")
    logger2.debug("ISKEF_on"+"\t"+str(ISKEF_on))
    logger2.debug("ISEGS_on"+"\t"+str(ISEGS_on))
    logger2.debug("Cband3_on"+"\t"+str(Cband3_on))
    logger2.debug("Cband4_on"+"\t"+str(Cband4_on))
    logger2.debug("Cband5_on"+"\t"+str(Cband5_on))
    logger2.debug("Cband6_on"+"\t"+str(Cband6_on))    
    logger2.debug("ISX1_on"+"\t"+str(ISX1_on))
    logger2.debug("ISX2_on"+"\t"+str(ISX2_on))    
    logger2.debug("Xband3_on"+"\t"+str(Xband3_on))
    logger2.debug("Xband4_on"+"\t"+str(Xband4_on))
    logger2.debug("Xband5_on"+"\t"+str(Xband5_on))
    logger2.debug("Xband6_on"+"\t"+str(Xband6_on))
    logger2.debug("GFZ1_on"+"\t"+str(GFZ1_on))
    logger2.debug("GFZ2_on"+"\t"+str(GFZ2_on))
    logger2.debug("GFZ3_on"+"\t"+str(GFZ3_on))
    logger2.debug("Cam4_on"+"\t"+str(Cam4_on))
    logger2.debug("Cam5_on"+"\t"+str(Cam5_on))
    logger2.debug("Cam6_on"+"\t"+str(Cam6_on))
    logger2.debug("ISKEFm_on"+"\t"+str(ISKEFm_on))
    logger2.debug("ISEGSm_on"+"\t"+str(ISEGSm_on))
    logger2.debug("Cband3m_on"+"\t"+str(Cband3m_on))
    logger2.debug("Cband4m_on"+"\t"+str(Cband4m_on))
    logger2.debug("Cband5m_on"+"\t"+str(Cband5m_on))
    logger2.debug("Cband6m_on"+"\t"+str(Cband6m_on))
    logger2.debug("ISX1m_on"+"\t"+str(ISX1m_on))    
    logger2.debug("ISX2m_on"+"\t"+str(ISX2m_on))
    logger2.debug("Xband3m_on"+"\t"+str(Xband3m_on))
    logger2.debug("Xband4m_on"+"\t"+str(Xband4m_on))
    logger2.debug("Xband5m_on"+"\t"+str(Xband5m_on))
    logger2.debug("Xband6m_on"+"\t"+str(Xband6m_on))    

    logger2.debug("--------------radar sensor calibration------------")
    logger2.debug("cal_ISKEF_a"+"\t"+str(cal_ISKEF_a))
    logger2.debug("cal_ISKEF_b"+"\t"+str(cal_ISKEF_b))
    logger2.debug("cal_ISEGS_a"+"\t"+str(cal_ISEGS_a))    
    logger2.debug("cal_ISEGS_b"+"\t"+str(cal_ISEGS_b))   
    logger2.debug("cal_Cband3a"+"\t"+str(cal_Cband3a))
    logger2.debug("cal_Cband3b"+"\t"+str(cal_Cband3b))
    logger2.debug("cal_Cband4a"+"\t"+str(cal_Cband4a))
    logger2.debug("cal_Cband4b"+"\t"+str(cal_Cband4b))   
    logger2.debug("cal_Cband5a"+"\t"+str(cal_Cband5a))
    logger2.debug("cal_Cband5b"+"\t"+str(cal_Cband5b))
    logger2.debug("cal_Cband6a"+"\t"+str(cal_Cband6a))
    logger2.debug("cal_Cband6b"+"\t"+str(cal_Cband6b))
    logger2.debug("cal_ISX1_a"+"\t"+str(cal_ISX1_a))
    logger2.debug("cal_ISX1_b"+"\t"+str(cal_ISX1_b))
    logger2.debug("cal_ISX2_a"+"\t"+str(cal_ISX2_a))
    logger2.debug("cal_ISX2_b"+"\t"+str(cal_ISX2_b))    
    logger2.debug("cal_Xband3a"+"\t"+str(cal_Xband3a))
    logger2.debug("cal_Xband3b"+"\t"+str(cal_Xband3b))
    logger2.debug("cal_Xband4a"+"\t"+str(cal_Xband4a))
    logger2.debug("cal_Xband4b"+"\t"+str(cal_Xband4b))   
    logger2.debug("cal_Xband5a"+"\t"+str(cal_Xband5a))
    logger2.debug("cal_Xband5b"+"\t"+str(cal_Xband5b))
    logger2.debug("cal_Xband6a"+"\t"+str(cal_Xband6a))
    logger2.debug("cal_Xband6b"+"\t"+str(cal_Xband6b))
    
    logger2.debug("-------------- model settings------------")    
    logger2.debug("wtf_wil"+"\t"+str(wtf_wil))
    logger2.debug("wtf_spa"+"\t"+str(wtf_spa))
    logger2.debug("wtf_mas"+"\t"+str(wtf_mas))
    logger2.debug("wtf_mtg"+"\t"+str(wtf_mtg))    
    logger2.debug("wtf_deg"+"\t"+str(wtf_deg))
    logger2.debug("wtf_wood0d"+"\t"+str(wtf_wood0d))
    logger2.debug("ki"+"\t"+str(ki))  
    logger2.debug("timebase"+"\t"+str(timebase))    
    logger2.debug("oo_exp"+"\t"+str(oo_exp))
    logger2.debug("oo_con"+"\t"+str(oo_con))
    logger2.debug("wtf_exp"+"\t"+str(wtf_exp))
    logger2.debug("wtf_con"+"\t"+str(wtf_con))
    logger2.debug("oo_manual"+"\t"+str(oo_manual))    
    logger2.debug("wtf_manual"+"\t"+str(wtf_manual))
    logger2.debug("min_manMER"+"\t"+str(min_manMER))
    logger2.debug("max_manMER"+"\t"+str(max_manMER))
    logger2.debug("oo_wood"+"\t"+str(oo_wood))
    logger2.debug("oo_5MER"+"\t"+str(oo_5MER))    
    logger2.debug("wtf_wood"+"\t"+str(wtf_wood))       
    logger2.debug("wtf_5MER"+"\t"+str(wtf_5MER))    
    logger2.debug("oo_isound"+"\t"+str(oo_isound))   
    logger2.debug("wtf_isound"+"\t"+str(wtf_isound))    
    logger2.debug("oo_esens"+"\t"+str(oo_esens))   
    logger2.debug("wtf_esens"+"\t"+str(wtf_esens))
    logger2.debug("oo_pulsan"+"\t"+str(oo_pulsan))
    logger2.debug("wtf_pulsan"+"\t"+str(wtf_pulsan))
    logger2.debug("oo_scatter"+"\t"+str(oo_scatter))    
    logger2.debug("wtf_scatter"+"\t"+str(wtf_scatter)) 
    logger2.debug("analysis"+"\t"+str(analysis))
    
    logger2.debug("--------------output settings------------")
    logger2.debug("PM_Nplot" +"\t"+str(PM_Nplot))
    logger2.debug("PM_PHplot" +"\t"+str(PM_PHplot))
    logger2.debug("PM_MERplot"+"\t"+str(PM_MERplot))
    logger2.debug("PM_TME  "+"\t"+str(PM_TME))
    logger2.debug("PM_FMERplot" +"\t"+str(PM_FMERplot))
    logger2.debug("PM_FTME"+"\t"+str(PM_FTME))
    logger2.debug("StatusR_oo"+"\t"+str(StatusR_oo))
    logger2.debug("--------------plume diameter------------")
    logger2.debug("Min_DiaOBS"+"\t"+str(Min_DiaOBS))
    logger2.debug("Max_DiaOBS"+"\t"+str(Max_DiaOBS))
    logger2.debug("------------------------------------------")
    logger2.debug("TIMEBASE" +"\t"+str(TIMEBASE)) #actual timebase in system
    logger2.debug("------------------------------------------")
    logger2.info("Configuration file dates from: " + time_update)
    logger2.debug("")     

    #counters for pl.h. statistics - have to be reset in each new run!
    N_plh_ISKEF = 0
    N_plh_ISEGS = 0
    N_plh_Cband3, N_plh_Cband4, N_plh_Cband5, N_plh_Cband6 = 0,0,0,0    
    N_plh_ISX1 = 0
    N_plh_ISX2 = 0
    N_plh_Xband3, N_plh_Xband4, N_plh_Xband5, N_plh_Xband6 = 0,0,0,0
    N_plh_GFZ1 = 0
    N_plh_GFZ2 = 0
    N_plh_GFZ3 = 0
    N_plh_Cam4, N_plh_Cam5, N_plh_Cam6 = 0,0,0    
    N_plh_ISKEFm = 0
    N_plh_ISEGSm = 0
    N_plh_Cband3m, N_plh_Cband4m, N_plh_Cband5m, N_plh_Cband6m = 0,0,0,0  
    N_plh_ISX1m = 0
    N_plh_ISX2m = 0
    N_plh_Xband3m, N_plh_Xband4m, N_plh_Xband5m, N_plh_Xband6m = 0,0,0,0
    N_plh_air = 0
    N_plh_gr = 0
    N_plh_other = 0
    Latest_plh_ISKEF = 0
    Latest_plh_ISEGS = 0
    Latest_plh_Cband3,Latest_plh_Cband4,Latest_plh_Cband5,Latest_plh_Cband6 = 0,0,0,0
    Latest_plh_ISX1 = 0
    Latest_plh_ISX2 = 0
    Latest_plh_Xband3,Latest_plh_Xband4,Latest_plh_Xband5,Latest_plh_Xband6 = 0,0,0,0
    Latest_plh_GFZ1 = 0
    Latest_plh_GFZ2 = 0
    Latest_plh_GFZ3 = 0
    Latest_plh_Cam4,Latest_plh_Cam5,Latest_plh_Cam6 = 0,0,0
    Latest_plh_ISKEFm = 0
    Latest_plh_ISEGSm = 0
    Latest_plh_Cband3m,Latest_plh_Cband4m,Latest_plh_Cband5m,Latest_plh_Cband6m = 0,0,0,0    
    Latest_plh_ISX1m = 0
    Latest_plh_ISX2m = 0
    Latest_plh_Xband3m,Latest_plh_Xband4m,Latest_plh_Xband5m,Latest_plh_Xband6m = 0,0,0,0    
    Latest_plh_air = 0
    Latest_plh_gr = 0
    Latest_plh_other = 0 

# RETRIEVE DATA FILES FROM SERVERS AND STORE THEM LOCALLY
  
    def writeline(data):
        fd.write(data + "\n")

    SensOO=[ISKEF_on,ISEGS_on,Cband3_on,Cband4_on,Cband5_on,Cband6_on,ISX1_on,ISX2_on,Xband3_on,Xband4_on,Xband5_on,Xband6_on,GFZ1_on,GFZ2_on,GFZ3_on,Cam4_on,Cam5_on,Cam6_on]

    def ftp_import(onoroff,ipsrc,idsrc,dirsrc,filesrc):
        """imports auto-stream file from ftp server and stores it locally"""
        global verz
    
        filesrc_txt = filesrc+".txt"
        if onoroff == 1:
            try:
                f = FTP(ipsrc) # IP address of ftp server
                f.login()
                logger3.info(">>> "+str(idsrc)+" >>> connected!")
                f.cwd(dirsrc)                         #path of source file
                if filesrc_txt in f.nlst():           #name of source file
                    fd = open(filesrc+'.txt', 'w',encoding="utf-8", errors="surrogateescape")    #name of local file
                    f.retrlines('RETR '+filesrc_txt, writeline) 
                    fd.close()
                    logger3.info("OK - file transferred!")
                    f.quit()
                else:
                    logger3.warning ("!! No source file found for "+str(idsrc)+"!")
                    f.quit()
        
            except IOError:
                logger3.warning("!! "+str(idsrc)+" streaming site offline!")
                #adjusting the waiting period to delays caused by offline sites
                if verz > 239:
                    verz = 240 #maximum 240s
                else:
                    verz = verz+20
        else:
            logger3.info (str(idsrc)+": automatic data stream switched OFF")

    def import_autostreams(s_file,s_url,s_IP,s_dir,onoroff,idsrc):
        """retrieves autostream files and copies them to local drive"""
        global verz
        from radar_converter import retrieve_icelandic_radar,process_radar_file
        # radar_converter module download the radar data for the volcano of interest and create the radar files in the
        # format that REFIR is used to. Any future user should create his own radar_converter module
        if idsrc == 'ISKEF' or idsrc == 'ISEGS' or idsrc == 'ISX1' or idsrc == 'ISX2':
            retrieve_icelandic_radar(vulkan)
            process_radar_file()
        else:
            s_filetxt = s_file +".txt"
            if s_url !="":
                #www retrieval
                try:
                    if sys.version_info[0] >= 3:
                        from urllib.request import urlretrieve
                    else:
                        # Not Python 3
                        from urllib import urlretrieve
                    logger3.info("url >>> "+str(idsrc)+" >>> connected!")
                    urlretrieve(s_url, s_filetxt)
                    logger3.info("OK - file transferred!")
                except  EnvironmentError:
                    print("Error - url "+str(s_url)+" could not be opened!\n")
                    #adjusting the waiting period to delays caused by offline sites
                    if verz > 239:
                        verz = 240 #maximum 240s
                    else:
                        verz = verz+20
            else:
                #FTP
                ftp_import(onoroff,s_IP,idsrc,s_dir,s_file)
            
    for x in range (0,18):
        if ID[x]=="n.a.":
            print("...")#sensor slot not assigned
        else:
            if run_type == 1:
                import_autostreams(sens_file[x],sens_url[x],sens_IP[x],sens_dir[x],SensOO[x],ID[x])
   


    time_update=time_update[:19]
    time_OBS = time_OBS[:19]
    TimeConfig = datetime.datetime.strptime(time_update, "%Y-%m-%d %H:%M:%S")
    TimeOBS = datetime.datetime.strptime(time_OBS, "%Y-%m-%d %H:%M:%S")
    time_diff = TimeNOW - TimeOBS
    time_diff_sec = time_diff.total_seconds()
    logger3.info ("Time since last plume height input by operator:")
    time_diff_min = time_diff_sec/60
    logger3.info (str(time_diff_min) + " minutes")
    
    #NOTE. STACK VALUES ALL IN METER AND ABOVE VENT!!!
    
    stack3h=[[0.0,0.0,0.0,0.0,0,0,0]]
    stack1h=[[0.0,0.0,0.0,0.0,0,0,0]]
    stack30=[[0.0,0.0,0.0,0.0,0,0,0]]
    stack15=[[0.0,0.0,0.0,0.0,0,0,0]]
    
    logger3.info("")
    logger3.info("***********************************")
    logger3.info("Now reading input plume height data")
    logger3.info("***********************************")
    logger3.info("")
    

    def input_allphfile(timediffH,hminH,plhH,hmaxH,qfH,sourceH,onoffH):
        """ logs all obtained plumeheights in a file"""
        try:
            FILE1 = open(out_txt+"_plh_log_tmp.txt", "a",encoding="utf-8", errors="surrogateescape")
            TimiH = TimeNOW - datetime.timedelta(minutes=timediffH)
            FILE1.write(str(TimiH) +"\t"+str(hminH)+"\t"+str(plhH)+"\t"+str(hmaxH)\
            +"\t"+str(qfH)+"\t"+str(sourceH)+"\t"+str(onoffH)+"\n")
            FILE1.close()
               
        except EnvironmentError:
            FILE1 = open(out_txt+"_plh_log_tmp.txt", "w",encoding="utf-8", errors="surrogateescape")
            TimiH = TimeNOW - datetime.timedelta(minutes=timediffH)
            FILE1.write(str(TimiH) +"\t"+str(hminH)+"\t"+str(plhH)+"\t"+str(hmaxH)\
            +"\t"+str(qfH)+"\t"+str(sourceH)+"\t"+str(onoffH)+"\n")
            FILE1.close()
        #Remove duplettes
        lines = open(out_txt+"_plh_log_tmp.txt", 'r',encoding="utf-8", errors="surrogateescape").readlines()
        lines_set = set(lines)
        out  = open(out_txt+'_plh_log.txt', 'w',encoding="utf-8", errors="surrogateescape")
        for line in lines_set:
            out.write(line)

    def plot_src_analysis(l_c,l_cm,l_x,l_xm,l_cam,l_air,l_gr,l_other):
        """plots the results of the statistical plume height input data analyses"""
    
    # data to plot
        n_groups = 21
        data_auto = (l_c[0],l_c[1],l_c[2],l_c[3],l_c[4],l_c[5],l_x[0],l_x[1],l_x[2],\
    l_x[3],l_x[4],l_x[5],l_cam[0],l_cam[1],l_cam[2],l_cam[3],l_cam[4],l_cam[5],0,0,0)
        data_man = (l_cm[0],l_cm[1],l_cm[2],l_cm[3],l_cm[4],l_cm[5],l_xm[0],l_xm[1],\
    l_xm[2],l_xm[3],l_xm[4],l_xm[5],0,0,0,0,0,0,l_air,l_gr,l_other)
        #11,12,13,14,15,16,21,22,23,24,25,26,31,32,33,34,35,36,0,0,0
        #101,102,103,104,105,106,201,202,203,204,205,206,0,0,0,0,0,0,air,ground,other
        # create plot            
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.4
        opacity = 0.9
        index2 =[0,1,2,3,4,5] 
        rects1 = plt.bar(index, data_auto, bar_width,
                         alpha=opacity,
                         color='b',
                         label='autostream')
         
        rects2 = plt.bar(index + bar_width, data_man, bar_width,
                         alpha=opacity,
                         color='g',
                         label='manual feed')
         

        plt.ylabel('Age of latest data set')
        plt.title('Age of plume height data by source')
        plt.xticks(index + bar_width, (ID[0],ID[1],ID[2],ID[3],ID[4],ID[5],ID[6],\
    ID[7],ID[8],ID[9],ID[10],ID[11],ID[12],ID[13],ID[14],ID[15],ID[16],ID[17],"air","ground","other"),ha='right', rotation=45)
        plt.yticks(index2,("n.a.",">3h","3h","60min","30min","15min"))
        plt.legend()
         
        plt.tight_layout()
        plt.grid()
        plt.savefig(out_txt+"_SRC_stat.png",bbox_inches='tight', dpi=300) 
        plt.savefig(out_txt+'_SRC_stat.svg', bbox_inches='tight',format='svg', dpi=1200)
        
        del data_auto, rects1, rects2, index, data_man 
        ax.cla()
        fig.clf()
        plt.close('all')
        gc.collect()
        del gc.garbage[:]
        plt.close(fig)
        plt.close()

    def plot_src_totalcount(npl_c,npl_cm,npl_x,npl_xm,npl_cam,npl_air,npl_gr,npl_other):
        """plots the total amount of plume height input data by source"""
    
    # data to plot
        n_groups = 21
        data_auto = (npl_c[0],npl_c[1],npl_c[2],npl_c[3],npl_c[4],npl_c[5],npl_x[0],npl_x[1],npl_x[2],\
    npl_x[3],npl_x[4],npl_x[5],npl_cam[0],npl_cam[1],npl_cam[2],npl_cam[3],npl_cam[4],npl_cam[5],0,0,0)
        data_man = (npl_cm[0],npl_cm[1],npl_cm[2],npl_cm[3],npl_cm[4],npl_cm[5],npl_xm[0],npl_xm[1],\
    npl_xm[2],npl_xm[3],npl_xm[4],npl_xm[5],0,0,0,0,0,0,npl_air,npl_gr,npl_other)
        #1,2,3,4,5,6,7,11,21,31,41,81,82,83 
        # create plot
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.4
        opacity = 0.9
    
    
        rects1 = plt.bar(index, data_auto, bar_width,
                         alpha=opacity,
                         color='b',
                         label='autostream')
         
        rects2 = plt.bar(index + bar_width, data_man, bar_width,
                         alpha=opacity,
                         color='g',
                         label='manual feed')
    
        
        plt.ylabel('N_tot')
        plt.title('Total number of data since onset of eruption')
        plt.xticks(index + bar_width, (ID[0],ID[1],ID[2],ID[3],ID[4],ID[5],ID[6],\
    ID[7],ID[8],ID[9],ID[10],ID[11],ID[12],ID[13],ID[14],ID[15],ID[16],ID[17],"air","ground","other"),ha='right', rotation=45)
        plt.legend()
         
        plt.tight_layout()
        plt.grid()
        plt.savefig(out_txt+"_SRCtotal_stat.png",bbox_inches='tight', dpi=300)
        plt.savefig(out_txt+'_SRCtotal_stat.svg', bbox_inches='tight',format='svg', dpi=1200)
        del data_auto, rects1, rects2, index, data_man 
        ax.cla()
        fig.clf()
        plt.close(fig)
        plt.close('all')
        gc.collect()
        plt.close()
        del gc.garbage[:]

    def src_analysis1(stack_cat,source):
        """statistical analyzer for input plume height data"""
    #stack_cat: 1: older than 3h, 2: 3h, 3: 1h, 4: 30min, 5: 15min
        
        global N_plh_ISKEF
        global N_plh_ISEGS
        global N_plh_Cband3,N_plh_Cband4,N_plh_Cband5,N_plh_Cband6
        global N_plh_ISX1
        global N_plh_ISX2
        global N_plh_Xband3,N_plh_Xband4,N_plh_Xband5,N_plh_Xband6
        global N_plh_GFZ1
        global N_plh_GFZ2
        global N_plh_GFZ3
        global N_plh_Cam4, N_plh_Cam5, N_plh_Cam6
        global N_plh_ISKEFm
        global N_plh_ISEGSm
        global N_plh_Cband3m,N_plh_Cband4m,N_plh_Cband5m,N_plh_Cband6m        
        global N_plh_ISX1m
        global N_plh_ISX2m
        global N_plh_Xband3m,N_plh_Xband4m,N_plh_Xband5m,N_plh_Xband6m
        global N_plh_air
        global N_plh_gr
        global N_plh_other
        global Latest_plh_ISKEF
        global Latest_plh_ISEGS
        global Latest_plh_Cband3,Latest_plh_Cband4,Latest_plh_Cband5,Latest_plh_Cband6
        global Latest_plh_ISX1
        global Latest_plh_ISX2
        global Latest_plh_Xband3,Latest_plh_Xband4,Latest_plh_Xband5,Latest_plh_Xband6
        global Latest_plh_GFZ1
        global Latest_plh_GFZ2
        global Latest_plh_GFZ3
        global Latest_plh_Cam4, Latest_plh_Cam5, Latest_plh_Cam6
        global Latest_plh_ISKEFm
        global Latest_plh_ISEGSm
        global Latest_plh_Cband3m,Latest_plh_Cband4m,Latest_plh_Cband5m,Latest_plh_Cband6m  
        global Latest_plh_ISX1m
        global Latest_plh_ISX2m
        global Latest_plh_Xband3m,Latest_plh_Xband4m,Latest_plh_Xband5m,Latest_plh_Xband6m   
        global Latest_plh_air
        global Latest_plh_gr
        global Latest_plh_other 
        global N_PLH_C,N_PLH_Cm,N_PLH_X,N_PLH_Xm,N_PLH_Cam,N_plh_air,N_plh_gr,N_plh_other
        global LATE_C,LATE_Cm,LATE_X,LATE_Xm,LATE_Cam

    
        if source == 11:
            N_plh_ISKEF = N_plh_ISKEF + 1

            if stack_cat > Latest_plh_ISKEF:
                Latest_plh_ISKEF = stack_cat
            else:
                hjs=0
        elif source == 12:
            N_plh_ISEGS = N_plh_ISEGS + 1
            if stack_cat > Latest_plh_ISEGS:
                Latest_plh_ISEGS = stack_cat
            else:
                hjs=0
                
        elif source == 13:
            N_plh_Cband3 = N_plh_Cband3 + 1
            if stack_cat > Latest_plh_Cband3:
                Latest_plh_Cband3 = stack_cat
            else:
                hjs=0
                
        elif source == 14:
            N_plh_Cband4 = N_plh_Cband4 + 1
            if stack_cat > Latest_plh_Cband4:
                Latest_plh_Cband4 = stack_cat
            else:
                hjs=0
        elif source == 15:
            N_plh_Cband5 = N_plh_Cband5 + 1
            if stack_cat > Latest_plh_Cband5:
                Latest_plh_Cband5 = stack_cat
            else:
                hjs=0
        elif source == 16:
            N_plh_Cband6 = N_plh_Cband6 + 1
            if stack_cat > Latest_plh_Cband6:
                Latest_plh_Cband6 = stack_cat
            else:
                hjs=0
        elif source == 21:
            N_plh_ISX1 = N_plh_ISX1 + 1
            if stack_cat > Latest_plh_ISX1:
                Latest_plh_ISX1 = stack_cat
            else:
                hjs=0                
        elif source == 22:
            N_plh_ISX2 = N_plh_ISX2 + 1
            if stack_cat > Latest_plh_ISX2:
                Latest_plh_ISX2 = stack_cat
            else:
                hjs=0
        elif source == 23:
            N_plh_Xband3 = N_plh_Xband3 + 1
            if stack_cat > Latest_plh_Xband3:
                Latest_plh_Xband3 = stack_cat
            else:
                hjs=0
        elif source == 24:
            N_plh_Xband4 = N_plh_Xband4 + 1
            if stack_cat > Latest_plh_Xband4:
                Latest_plh_Xband4 = stack_cat
            else:
                hjs=0
        elif source == 25:
            N_plh_Xband5 = N_plh_Xband5 + 1
            if stack_cat > Latest_plh_Xband5:
                Latest_plh_Xband5 = stack_cat
            else:
                hjs=0
        elif source == 26:
            N_plh_Xband6 = N_plh_Xband6 + 1
            if stack_cat > Latest_plh_Xband6:
                Latest_plh_Xband6 = stack_cat
            else:
                hjs=0                
        elif source == 31:
            N_plh_GFZ1 = N_plh_GFZ1 + 1
            if stack_cat > Latest_plh_GFZ1:
                Latest_plh_GFZ1 = stack_cat
            else:
                hjs=0                
        elif source == 32:
            N_plh_GFZ2 = N_plh_GFZ2 + 1
            if stack_cat > Latest_plh_GFZ2:
                Latest_plh_GFZ2 = stack_cat
            else:
                hjs=0                
        elif source == 33:
            N_plh_GFZ3 = N_plh_GFZ3 + 1
            if stack_cat > Latest_plh_GFZ3:
                Latest_plh_GFZ3 = stack_cat
            else:
                hjs=0
        elif source == 34:
            N_plh_Cam4 = N_plh_Cam4 + 1
            if stack_cat > Latest_plh_Cam4:
                Latest_plh_Cam4 = stack_cat
            else:
                hjs=0
        elif source == 35:
            N_plh_Cam5 = N_plh_Cam5 + 1
            if stack_cat > Latest_plh_Cam5:
                Latest_plh_Cam5 = stack_cat
            else:
                hjs=0
        elif source == 36:
            N_plh_Cam6 = N_plh_Cam6 + 1
            if stack_cat > Latest_plh_Cam6:
                Latest_plh_Cam6 = stack_cat
            else:
                hjs=0                
        elif source == 101:
            N_plh_ISKEFm = N_plh_ISKEFm + 1
            if stack_cat > Latest_plh_ISKEFm:
                Latest_plh_ISKEFm = stack_cat
            else:
                hjs=0                
        elif source == 102:
            N_plh_ISEGSm = N_plh_ISEGSm + 1
            if stack_cat > Latest_plh_ISEGSm:
                Latest_plh_ISEGSm = stack_cat
            else:
                hjs=0
        elif source == 103:
            N_plh_Cband3m = N_plh_Cband3m + 1
            if stack_cat > Latest_plh_Cband3m:
                Latest_plh_Cband3m = stack_cat
            else:
                hjs=0
        elif source == 104:
            N_plh_Cband4m = N_plh_Cband4m + 1
            if stack_cat > Latest_plh_Cband4m:
                Latest_plh_Cband4m = stack_cat
            else:
                hjs=0
        elif source == 105:
            N_plh_Cband5m = N_plh_Cband5m + 1
            if stack_cat > Latest_plh_Cband5m:
                Latest_plh_Cband5m = stack_cat
            else:
                hjs=0
        elif source == 106:
            N_plh_Cband6m = N_plh_Cband6m + 1
            if stack_cat > Latest_plh_Cband6m:
                Latest_plh_Cband6m = stack_cat
            else:
                hjs=0                
        elif source == 201:
            N_plh_ISX1m = N_plh_ISX1m + 1
            if stack_cat > Latest_plh_ISX1m:
                Latest_plh_ISX1m = stack_cat
            else:
                hjs=0                
        elif source == 202:
            N_plh_ISX2m = N_plh_ISX2m + 1
            if stack_cat > Latest_plh_ISX2m:
                Latest_plh_ISX2m = stack_cat
            else:
                hjs=0
        elif source == 203:
            N_plh_Xband3m = N_plh_Xband3m + 1
            if stack_cat > Latest_plh_Xband3m:
                Latest_plh_Xband3m = stack_cat
            else:
                hjs=0
        elif source == 204:
            N_plh_Xband4m = N_plh_Xband4m + 1
            if stack_cat > Latest_plh_Xband4m:
                Latest_plh_Xband4m = stack_cat
            else:
                hjs=0
        elif source == 205:
            N_plh_Xband5m = N_plh_Xband5m + 1
            if stack_cat > Latest_plh_Xband5m:
                Latest_plh_Xband5m = stack_cat
            else:
                hjs=0
        elif source == 206:
            N_plh_Xband6m = N_plh_Xband6m + 1
            if stack_cat > Latest_plh_Xband6m:
                Latest_plh_Xband6m = stack_cat
            else:
                hjs=0                
        elif source == 700:
            N_plh_air = N_plh_air + 1
            if stack_cat > Latest_plh_air:
                Latest_plh_air = stack_cat
            else:
                hjs=0                
        elif source == 800:
            N_plh_gr = N_plh_gr + 1
            if stack_cat > Latest_plh_gr:
                Latest_plh_gr = stack_cat
            else:
                hjs=0                
        else:        
            N_plh_other = N_plh_other + 1
            if stack_cat > Latest_plh_other:
                Latest_plh_other = stack_cat
            else:
                hjs=0        
        N_PLH_C = [N_plh_ISKEF,N_plh_ISEGS,N_plh_Cband3, N_plh_Cband4, N_plh_Cband5, N_plh_Cband6]
        N_PLH_Cm = [N_plh_ISKEFm,N_plh_ISEGSm, N_plh_Cband3m, N_plh_Cband4m, N_plh_Cband5m, N_plh_Cband6m]
        N_PLH_X = [N_plh_ISX1,N_plh_ISX2,N_plh_Xband3,N_plh_Xband4,N_plh_Xband5,N_plh_Xband6]
        N_PLH_Xm= [N_plh_ISX1m,N_plh_ISX2m,N_plh_Xband3m, N_plh_Xband4m, N_plh_Xband5m, N_plh_Xband6m]
        N_PLH_Cam =[N_plh_GFZ1,N_plh_GFZ2,N_plh_GFZ3,N_plh_Cam4, N_plh_Cam5, N_plh_Cam6]

        LATE_C = [Latest_plh_ISKEF,Latest_plh_ISEGS,Latest_plh_Cband3,Latest_plh_Cband4,Latest_plh_Cband5,Latest_plh_Cband6]
        LATE_X =[Latest_plh_ISX1,Latest_plh_ISX2,Latest_plh_Xband3,Latest_plh_Xband4,Latest_plh_Xband5,Latest_plh_Xband6]
        LATE_Cam=[Latest_plh_GFZ1,Latest_plh_GFZ2,Latest_plh_GFZ3,Latest_plh_Cam4,Latest_plh_Cam5,Latest_plh_Cam6]
        LATE_Cm =[Latest_plh_ISKEFm,Latest_plh_ISEGSm,Latest_plh_Cband3m,Latest_plh_Cband4m,Latest_plh_Cband5m,Latest_plh_Cband6m]
        LATE_Xm = [Latest_plh_ISX1m,Latest_plh_ISX2m,Latest_plh_Xband3m,Latest_plh_Xband4m,Latest_plh_Xband5m,Latest_plh_Xband6m]
        del gc.garbage[:]

    def indiv_plh_stack(timediff,plh,unc,qf,source,onoff):
            """stacks all plume height data sorted by source"""
            global Cband1_stack
            global Cband2_stack
            global Cband3_stack
            global Cband4_stack
            global Cband5_stack
            global Cband6_stack
            global Xband1_stack
            global Xband2_stack
            global Xband3_stack
            global Xband4_stack
            global Xband5_stack
            global Xband6_stack
            global Cam1_stack
            global Cam2_stack
            global Cam3_stack
            global Cam4_stack
            global Cam5_stack
            global Cam6_stack
            global air_stack
            global ground_stack
            global other_stack
            global Cband1_t_stack
            global Cband2_t_stack
            global Cband3_t_stack
            global Cband4_t_stack
            global Cband5_t_stack
            global Cband6_t_stack
            global Xband1_t_stack
            global Xband2_t_stack
            global Xband3_t_stack
            global Xband4_t_stack
            global Xband5_t_stack
            global Xband6_t_stack
            global Cam1_t_stack
            global Cam2_t_stack
            global Cam3_t_stack
            global Cam4_t_stack
            global Cam5_t_stack
            global Cam6_t_stack
            global air_t_stack
            global ground_t_stack
            global other_t_stack
            source = int(source)
            if onoff == 0:
                print()
            else:
                if plh <=0:
                    logger3.critical("Plume height data corrupted!")
                else:
                    hmin = plh-unc
                    hmax = plh+unc
                    if timediff<0:
                        logger3.warning("------------data set seems to be from future!\n")
                        logger3.warning(str(timediff)+"min")
                    else:
                        if source==11 or source==101:
                            Cband1_stack.append(plh)
                            Cband1_t_stack.append(timediff)
                        elif source==12 or source==102:
                            Cband2_stack.append(plh)
                            Cband2_t_stack.append(timediff)
                        elif source==13 or source==103:
                            Cband3_stack.append(plh)
                            Cband3_t_stack.append(timediff)
                        elif source==14 or source==104:
                            Cband4_stack.append(plh)
                            Cband4_t_stack.append(timediff)
                        elif source==15 or source==105:
                            Cband5_stack.append(plh)
                            Cband5_t_stack.append(timediff)
                        elif source==16 or source==106:
                            Cband6_stack.append(plh)
                            Cband6_t_stack.append(timediff)
        
                        elif source==21 or source==201:
                            Xband1_stack.append(plh)
                            Xband1_t_stack.append(timediff)
                        elif source==22 or source==202:
                            Xband2_stack.append(plh)
                            Xband2_t_stack.append(timediff)
                        elif source==23 or source==203:
                            Xband3_stack.append(plh)
                            Xband3_t_stack.append(timediff)
                        elif source==24 or source==204:
                            Xband4_stack.append(plh)
                            Xband4_t_stack.append(timediff)
                        elif source==25 or source==205:
                            Xband5_stack.append(plh)
                            Xband5_t_stack.append(timediff)
                        elif source==26 or source==206:
                            Xband6_stack.append(plh)
                            Xband6_t_stack.append(timediff)
        
                        elif source==31:
                            Cam1_stack.append(plh)
                            Cam1_t_stack.append(timediff)
                        elif source==32:
                            Cam2_stack.append(plh)
                            Cam2_t_stack.append(timediff)                    
                        elif source==33:
                            Cam3_stack.append(plh)
                            Cam3_t_stack.append(timediff)
                        elif source==34:
                            Cam4_stack.append(plh)
                            Cam4_t_stack.append(timediff)
                        elif source==35:
                            Cam5_stack.append(plh)
                            Cam5_t_stack.append(timediff)
                        elif source==36:
                            Cam6_stack.append(plh)
                            Cam6_t_stack.append(timediff)
                            
                        elif source==700:
                            air_stack.append(plh)
                            air_t_stack.append(timediff)                   
                            
                        elif source==800:
                            ground_stack.append(plh)
                            ground_t_stack.append(timediff)                    
                        else:
                            other_stack.append(plh)
                            other_t_stack.append(timediff)                   
        
                        logger3.debug("*Stacked pl.h. data >> source: " + str(source)+"\t"+"time difference: "+str(timediff)+"\t"+"hmin: "+str(hmin)+"\t"+"hmax: "+str(hmax))
            del gc.garbage[:]
            return (True)

    def plot_indi_plh():
        """plots individual plume heights"""
        global Cband1_stack
        global Cband2_stack
        global Cband3_stack
        global Cband4_stack
        global Cband5_stack
        global Cband6_stack
        global Xband1_stack
        global Xband2_stack
        global Xband3_stack
        global Xband4_stack
        global Xband5_stack
        global Xband6_stack
        global Cam1_stack
        global Cam2_stack
        global Cam3_stack
        global Cam4_stack
        global Cam5_stack
        global Cam6_stack
        global air_stack
        global ground_stack
        global other_stack
        global loc_ISKEF
        global loc_ISEGS 
        global loc_Cband3 
        global loc_Cband4 
        global loc_Cband5 
        global loc_Cband6 
        global loc_ISX1 
        global loc_ISX2 
        global loc_Xband3 
        global loc_Xband4 
        global loc_Xband5 
        global loc_Xband6 
        global loc_GFZ1 
        global loc_GFZ2 
        global loc_GFZ3 
        global loc_Cam4 
        global loc_Cam5 
        global loc_Cam6 
        global Cband1_t_stack
        global Cband2_t_stack
        global Cband3_t_stack
        global Cband4_t_stack
        global Cband5_t_stack
        global Cband6_t_stack
        global Xband1_t_stack
        global Xband2_t_stack
        global Xband3_t_stack
        global Xband4_t_stack
        global Xband5_t_stack
        global Xband6_t_stack
        global Cam1_t_stack
        global Cam2_t_stack
        global Cam3_t_stack
        global Cam4_t_stack
        global Cam5_t_stack
        global Cam6_t_stack
        global air_t_stack
        global ground_t_stack
        global other_t_stack
        global APHmax_y

        def as_src(loc,pluh,tim,ide,secol):
            """assignes source to sector"""
            global APHmax_y
            
            t_vor = []            
            if time_axis == 1:
                for i in range(0,len(tim)):
                    t_zw = timin - tim[i]
                    t_vor.append(t_zw)
            else:
                t_vor = tim
            huj = 0
            if loc == -1:
                #Western sector
                lstyle = "-"
                plt.plot(t_vor,pluh,color=secol, linewidth=1.5, linestyle=lstyle,label=str(ide))
                try:
                    
                    if APHmax_y<max(pluh):
                        APHmax_y=max(pluh)
                    else:
                        huj=0
                except TypeError:
                    # APH and pluh are only single values
                    if APHmax_y<pluh:
                        APHmax_y=pluh
                    else:
                        huj=0

                except ValueError:
                        vaj=0
                
            elif loc == 1:
                #Eastern sector
                lstyle ="--"
                plt.plot(t_vor,pluh,color=secol, linewidth=1.5, linestyle=lstyle,label=str(ide))
                try:
                    if APHmax_y<max(pluh):
                        APHmax_y=max(pluh)
                    else:
                        huj=0
                except TypeError:
                    if APHmax_y<max(pluh):
                        APHmax_y=pluh
                    else:
                        huj=0
                except ValueError:
                    vaj=0
            elif loc == 2:
                    #not specified
                secol = "grey"
                plt.plot(t_vor,pluh,color=secol, linewidth=1.5, linestyle=":") 
                try:
                    if APHmax_y<max(pluh):
                        APHmax_y=max(pluh)
                    else:
                        huj=0
                except TypeError:
                    if APHmax_y<max(pluh):
                        APHmax_y=pluh
                    else:
                        huj=0
                except ValueError:
                    vaj=0
            else:
                secol = "black"
            del gc.garbage[:]
        def as_src2(loc,pluh,tim,ide,secol):
            """assignes source to sector"""
            
            t_vor = []        
            if time_axis == 1:
                for i in range(0,len(tim)):
                    t_zw = timin - tim[i]
                    t_vor.append(t_zw)
            else:
                t_vor = tim
            huj = 2

            if loc == -1:
                #Western sector
                ax1.plot(t_vor,pluh,color=secol, linewidth=1.5, linestyle="-",label=str(ide))
                #1 Added
                #2 xlim(0,tmin)
            elif loc == 1:
                #Eastern sector
                ax2.plot(t_vor,pluh,color=secol, linewidth=1.5, linestyle="--",label=str(ide))
                #1 Added
                #2 xlim(0, tmin)
            elif loc == 2:
                    #not specified
                secol = "grey"
            else:
                secol = "black"
            del gc.garbage[:]    
        fig=figure.Figure()
        ax = plt.gca()

        try:
            as_src(loc_ISKEF,Cband1_stack,Cband1_t_stack,ID[0],"red")
        except EnvironmentError:
            print ("Individual plot skipped")
        try:
            as_src(loc_ISEGS,Cband2_stack,Cband2_t_stack,ID[1],"blue")
        except EnvironmentError:
            print ("Individual plot skipped")
        try:
            as_src(loc_Cband3,Cband3_stack,Cband3_t_stack,ID[2],"darkgreen")
        except EnvironmentError:
            print ("Individual plot skipped")
        try:
            as_src(loc_Cband4,Cband4_stack,Cband4_t_stack,ID[3],"magenta")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src(loc_Cband5,Cband5_stack,Cband5_t_stack,ID[4],"cyan")
        except EnvironmentError:
            print ("Individual plot skipped")
            
        try:
            as_src(loc_Cband6,Cband6_stack,Cband6_t_stack,ID[5],"darkred")
        except EnvironmentError:
            print ("Individual plot skipped")
          
        try:
            as_src(loc_ISX1,Xband1_stack,Xband1_t_stack,ID[6],"darkcyan")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src(loc_ISX2,Xband2_stack,Xband2_t_stack,ID[7],"darkorange")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src(loc_Xband3,Xband3_stack,Xband3_t_stack,ID[8],"steelblue")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src(loc_Xband4,Xband4_stack,Xband4_t_stack,ID[9],"lime green")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src(loc_Xband5,Xband5_stack,Xband5_t_stack,ID[10],"gold")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src(loc_Xband6,Xband6_stack,Xband6_t_stack,ID[11],"coral")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src(loc_GFZ1,Cam1_stack,Cam1_t_stack,ID[12],"navy")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src(loc_GFZ2,Cam2_stack,Cam2_t_stack,ID[13],"darkviolet")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src(loc_GFZ3,Cam3_stack,Cam3_t_stack,ID[14],"olive")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src(loc_Cam4,Cam4_stack,Cam4_t_stack,ID[15],"violet")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src(loc_Cam5,Cam5_stack,Cam5_t_stack,ID[16],"deeppink")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src(loc_Cam6,Cam6_stack,Cam6_t_stack,ID[17],"cornflowerblue")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            if air_t_stack == []:
                print("")
            else:
                as_src(2,air_stack,air_t_stack,"air obs","grey")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            if ground_stack == []:
                print("")
            else:
                as_src(2,ground_stack,ground_t_stack,"ground obs","grey")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            if other_t_stack == []:
                print("")
            else:
                as_src(2,other_stack,other_t_stack,"other","grey")
        except EnvironmentError:
            print ("Individual plot skipped")        

        
        plt.figtext(0.35, 0.96, "East: dashed line", fontsize='large', color='k', ha ='right')
        plt.figtext(0.65, 0.96, "West: solid line", fontsize='large', color='k', ha ='left')
        plt.figtext(0.50, 0.96, '       ', fontsize='large', color='k', ha ='center')
        if time_axis == 0:
            plt.xlabel('time since present (min)')
        else:
            plt.xlabel('time since eruption start (min)')
        plt.ylabel('height a.v. [m]')
        plt.title('Plume Heights by Sources and Sectors')
        plt.ylim(0)


        # if(run_type) == 1:
        #     max_x = max(max(Cband1_t_stack, Cband2_t_stack, Cband3_t_stack, Cband4_t_stack, Cband5_t_stack, Cband6_t_stack, \
        #     Xband1_t_stack,Xband2_t_stack,Xband3_t_stack,Xband4_t_stack,Xband5_t_stack,Xband6_t_stack,\
        #     Cam1_t_stack,Cam2_t_stack,Cam3_t_stack,Cam4_t_stack,Cam5_t_stack,Cam6_t_stack))
        # else:
        max_x = timin
        plt.text(0.5*max_x, 0.5*APHmax_y, 'REFIR',fontsize=80, color='gray',ha='center', va='center', alpha=0.09)

        try:
            plt.xlim(0,max_x)
        except TypeError:
            plt.xlim(0,250)
        plt.xlim(0,max_x)
        if time_axis == 0:
            ax.invert_xaxis()
        else:
            huit = 1
        plt.legend(loc='upper left')
        plt.grid()
        

        plt.savefig(out_txt+"_APH_plot.png",bbox_inches='tight',dpi=300) 
        plt.savefig(out_txt+"_APH_plot.svg", format='svg', dpi=1200) #highresolution
        del gc.garbage[:]    
        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        ax = plt.gca()
    
        try:
            as_src2(loc_ISKEF,Cband1_stack,Cband1_t_stack,ID[0],"red")
        except EnvironmentError:
            print ("Individual plot skipped")
        try:
            as_src2(loc_ISEGS,Cband2_stack,Cband2_t_stack,ID[1],"blue")
        except EnvironmentError:
            print ("Individual plot skipped")
        try:
            as_src2(loc_Cband3,Cband3_stack,Cband3_t_stack,ID[2],"darkgreen")
        except EnvironmentError:
            print ("Individual plot skipped")
        try:
            as_src2(loc_Cband4,Cband4_stack,Cband4_t_stack,ID[3],"magenta")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src2(loc_Cband5,Cband5_stack,Cband5_t_stack,ID[4],"cyan")
        except EnvironmentError:
            print ("Individual plot skipped")
            
        try:
            as_src2(loc_Cband6,Cband6_stack,Cband6_t_stack,ID[5],"darkred")
        except EnvironmentError:
            print ("Individual plot skipped")
          
        try:
            as_src2(loc_ISX1,Xband1_stack,Xband1_t_stack,ID[6],"darkcyan")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src2(loc_ISX2,Xband2_stack,Xband2_t_stack,ID[7],"darkorange")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src2(loc_Xband3,Xband3_stack,Xband3_t_stack,ID[8],"steelblue")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src2(loc_Xband4,Xband4_stack,Xband4_t_stack,ID[9],"lime green")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src2(loc_Xband5,Xband5_stack,Xband5_t_stack,ID[10],"gold")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src2(loc_Xband6,Xband6_stack,Xband6_t_stack,ID[11],"coral")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src2(loc_GFZ1,Cam1_stack,Cam1_t_stack,ID[12],"navy")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src2(loc_GFZ2,Cam2_stack,Cam2_t_stack,ID[13],"darkviolet")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src2(loc_GFZ3,Cam3_stack,Cam3_t_stack,ID[14],"olive")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src2(loc_Cam4,Cam4_stack,Cam4_t_stack,ID[15],"violet")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src2(loc_Cam5,Cam5_stack,Cam5_t_stack,ID[16],"deeppink")
        except EnvironmentError:
            print ("Individual plot skipped")
    
        try:
            as_src2(loc_Cam6,Cam6_stack,Cam6_t_stack,ID[17],"cornflowerblue")
        except EnvironmentError:
            print ("Individual plot skipped")
    
           
        if time_axis == 0:
            plt.figtext(0.5, -0.01, "time since present (min)", fontsize='large', ha ='center')
        else:            
            plt.figtext(0.5, -0.01, "time since eruption start (min)", fontsize='large', ha ='center')
        
        plt.figtext(0.50, 0.96, ' Plume Heights a.v. (m) ', fontsize='large', color='k', ha ='center')


        ax1.set_title('Western sector',color='b')
        ax2.set_title('Eastern sector',color='r')
        plt.ylim(0)
        try:
            ax1.set_xlim(0,max_x)
            ax2.set_xlim(0,max_x)
        except TypeError:
            ax1.set_xlim(0,250)
            ax2.set_xlim(0,250)
        ax1.legend(loc='lower left')
        ax2.legend(loc='lower right')
        if time_axis == 0:
            ax1.invert_xaxis()
        else:
            huit = 2
        ax1.grid()
        if time_axis == 0:
            ax2.invert_xaxis()
        else:
            huit = 3
        ax2.grid()
        f.subplots_adjust(hspace=0)
        f.text(0.5, 0.5, 'REFIR',fontsize=80, color='gray',ha='center', va='center', alpha=0.09)

        plt.savefig(out_txt+"_PHSec_plot.png",bbox_inches='tight',dpi=300)
        plt.savefig(out_txt+"_PHSec_plot.svg", format='svg', dpi=1200) #highresolution
        plt.close("all")
        plt.close(fig)
        del gc.garbage[:]

    def stacksort(timediff,plh,unc,qf,source,onoff):
        """sorts data according to up-to-dateness"""
        if plh <=0:
            logger3.critical("Plume height data corrupted!")
        else:
            hmin = plh-unc
            if hmin <0:
#                hmin = 0     #Here is a potential problem. If all readings in stacks are 0, then there is a problem later.
                hmin = 1
            else:
                juh = 0
            hmax = plh+unc    
            
            if timediff<0:
                logger3.warning("------------data set seems to be from future!\n")
            else:
                indiv_plh_stack(timediff,plh,unc,qf,source,onoff)
                
                
                if timediff<16:
                    src_analysis1(5,source)
                elif timediff<31:
                    src_analysis1(4,source)
                elif timediff<61:
                    src_analysis1(3,source)
                elif timediff<181:
                    src_analysis1(2,source)
                else:
                    src_analysis1(1,source)
            
                huj=0
                if analysis == 0:
                    huj = 1
                else:
                    plot_src_totalcount(N_PLH_C,N_PLH_Cm,N_PLH_X,N_PLH_Xm,N_PLH_Cam,N_plh_air,N_plh_gr,N_plh_other) 
                                        
                                        
                    plot_src_analysis(LATE_C,LATE_Cm,LATE_X,LATE_Xm,LATE_Cam,Latest_plh_air,Latest_plh_gr,Latest_plh_other) 

                if timediff<181:
                    input_allphfile(timediff, hmin,plh,hmax,qf,source,onoff)
                    stack3h.append([timediff, hmin,plh,hmax,qf,source,onoff])
                else:
                    huj =1
                if timediff<61:
                    stack1h.append([timediff, hmin,plh,hmax,qf,source,onoff])

                else:
                    huj =1                    
                if timediff<31:
                    stack30.append([timediff, hmin,plh,hmax,qf,source,onoff])
                else:
                    huj =1
                if timediff<16:
                    stack15.append([timediff, hmin,plh,hmax,qf,source,onoff])
                else:
                    huj =1
                logger3.debug("*Stacked pl.h. data >> source: " + str(source)+"\t"+"time difference: "+str(timediff)+"\t"+"hmin: "+str(hmin)+"\t"+"hmax: "+str(hmax))
                del gc.garbage[:]
        return(True)

    #Getting data from manual input file
    logger3.info("")
    logger3.info("**************************************")
    logger3.info("Continuing with non-auto stream data")
    logger3.info("**************************************")
    logger3.info("")
    
    def OBSsourceOnOff(msrc):
        """provides false if specific manual source is turned off"""
        if msrc==101 and ISKEFm_on == 0:
            return False
        elif msrc== 102 and ISEGSm_on ==0:
            return False
        elif msrc== 103 and Cband3m_on ==0:
            return False
        elif msrc== 104 and Cband4m_on ==0:
            return False
        elif msrc== 105 and Cband5m_on ==0:
            return False
        elif msrc== 106 and Cband6m_on ==0:
            return False
        elif msrc== 201 and ISX1m_on ==0:
            return False
        elif msrc== 202 and ISX2m_on ==0:
            return False
        elif msrc== 203 and Xband3m_on ==0:
            return False
        elif msrc== 204 and Xband4m_on ==0:
            return False
        elif msrc== 205 and Xband5m_on ==0:
            return False
        elif msrc== 206 and Xband6m_on ==0:
            return False
        else:
            return True

    def OBSin ():
        """reads OBS data"""
        global TimeNOW
        global obsin_doo,obsin_src,obsin_hmin,obsin_havg,obsin_hmax,obsin_unc,\
    obsin_qf,time_diffo_min
        rlines = []
    
        obsin_doo,obsin_src,obsin_hmin,obsin_havg,obsin_hmax,obsin_unc,\
    obsin_qf = np.loadtxt("fix_OBSin.txt",usecols=(1,2,3,4,5,6,7), unpack=True, delimiter='\t')  
        with open("fix_OBSin.txt", "r",encoding="utf-8", errors="surrogateescape") as fp:
            for line in fp:
                rlines.append(line[:19])
        fp.close()  
        
        obsin_hmin = obsin_hmin - vent_h
        obsin_havg = obsin_havg - vent_h
        obsin_hmax = obsin_hmax - vent_h

        l = len(rlines)
        if l ==1:
            #catch one-liners
            if rlines[-1] == "":
                for x in range (0,l-1):
                    obsindate = rlines[x]
                    TimeO = datetime.datetime.strptime(obsindate, "%m %d %Y %H:%M:%S")
                    time_diffo = TimeNOW - TimeO
                    time_diffo_sec = time_diffo.total_seconds()
                    if time_diffo_sec < 0:
                        continue
                    time_diffo_min = time_diffo_sec/60
                    if obsin_doo == 1:
                        if OBSsourceOnOff(obsin_src):
                            logger3.info("***observed data stored!")
                            stacksort(time_diffo_min,obsin_havg,obsin_unc,\
                            obsin_qf,obsin_src,obsin_doo)
                        else:
                            return None
                    else:
                        return None
                    
            else:
                 for x in range (0,l):
                    obsindate = rlines[x]
                    TimeO = datetime.datetime.strptime(obsindate, "%m %d %Y %H:%M:%S")
                    time_diffo = TimeNOW - TimeO
                    time_diffo_sec = time_diffo.total_seconds()
                    if time_diffo_sec < 0:
                        continue
                    time_diffo_min = time_diffo_sec/60
                    if obsin_doo == 1:
                        if OBSsourceOnOff(obsin_src):
                            logger3.info("***observed data stored!")
                            stacksort(time_diffo_min,obsin_havg,obsin_unc,\
                            obsin_qf,obsin_src,obsin_doo)
                        else:
                            return None
                    else:
                        logger3.info ("data set discarded")
                        return None
        else:
            if rlines[-1] == "":
                for x in range (0,l-1):
                    obsindate = rlines[x]
                    TimeO = datetime.datetime.strptime(obsindate, "%m %d %Y %H:%M:%S")
                    time_diffo = TimeNOW - TimeO
                    time_diffo_sec = time_diffo.total_seconds()
                    if time_diffo_sec < 0:
                        continue
                    time_diffo_min = time_diffo_sec/60
                    if obsin_doo[x] == 1:#checks if individual data set should be considered
                        if OBSsourceOnOff(obsin_src[x]): #checks if manual data sets in general should be considered
                            logger3.info("***observed data stored!")
                            stacksort(time_diffo_min,obsin_havg[x],obsin_unc[x],\
                            obsin_qf[x],obsin_src[x],obsin_doo[x])
                        else:
                            return None
                    else:
                        return None
                    
            else:
                 for x in range (0,l):
                    obsindate = rlines[x]
                    TimeO = datetime.datetime.strptime(obsindate, "%m %d %Y %H:%M:%S")
                    time_diffo = TimeNOW - TimeO
                    time_diffo_sec = time_diffo.total_seconds()
                    if time_diffo_sec < 0:
                        continue
                    time_diffo_min = time_diffo_sec/60
                    if obsin_doo[x] == 1:
                        if OBSsourceOnOff(obsin_src[x]):
                            logger3.info("***observed data stored!")
                            stacksort(time_diffo_min,obsin_havg[x],obsin_unc[x],\
                            obsin_qf[x],obsin_src[x],obsin_doo[x])
                        else:
                            return None
                    else:
                        logger3.info ("data set discarded")

    if OBS_on == 1:
        try:
            FILE5 = open("fix_OBSin.txt", "r",encoding="utf-8", errors="surrogateescape")
            FILE5.close()
            OBSin()
        except EnvironmentError:
            logger3.info("!! No manually input observation data found!!")
    
    else:
        logger3.info("All non-auto stream data switched OFF!")

    #Getting data from radar files
    logger3.info("")
    logger3.info("*************************************************")
    logger3.info("Continuing with auto-stream C-band radar data")
    logger3.info("*************************************************")
    logger3.info("")
    
    def radartimeC (radarC_file, unc_C, qf_C, source_C):
        """reads C-radar data"""
        if source_C == 11:
            KF_a = cal_ISKEF_a
            KF_b = cal_ISKEF_b
        elif source_C == 12:
            KF_a = cal_ISEGS_a
            KF_b = cal_ISEGS_b
        elif source_C == 13:
            KF_a = cal_Cband3a
            KF_b = cal_Cband3b
        elif source_C == 14:
            KF_a = cal_Cband4a
            KF_b = cal_Cband4b
        elif source_C == 15:
            KF_a = cal_Cband5a
            KF_b = cal_Cband5b
        elif source_C == 16:
            KF_a = cal_Cband6a
            KF_b = cal_Cband6b

        global TimeNOW

        if run_type == 1:
            TimeNOW = datetime.datetime.utcnow()
        rlines =[]
        with open(radarC_file+".txt", "r",encoding="utf-8", errors="surrogateescape") as ins:
            for line in ins:
                rlines.append(line)

        ins.close()
        l=len(rlines)-1
#        l=(len(rlines)-11) #This was right with the previous configuration

        if rlines[-1] == "":
            for x in range (2,l+1):
                zeile = rlines[-x]
                indate = zeile[:19]
                TimeC = datetime.datetime.strptime(indate, "%Y-%m-%d %H:%M:%S")
                time_diffe = TimeNOW - TimeC
                time_diffe_sec = time_diffe.total_seconds()
                if time_diffe_sec < 0:
                    continue
                time_diffe_min = time_diffe_sec/60
                plumeh = float(zeile[-6:])
                if plumeh>99:
                    h_C = 0
                else:
                    h_C=KF_a+KF_b*(plumeh*1000-vent_h)
                stacksort(time_diffe_min,h_C,unc_C,qf_C,source_C,1)
                
        else:
             for x in range (1,l):
                zeile = rlines[-x]
                indate = zeile[:19]
                TimeC = datetime.datetime.strptime(indate, "%Y-%m-%d %H:%M:%S")
                time_diffe = TimeNOW - TimeC
                time_diffe_sec = time_diffe.total_seconds()
                if time_diffe_sec < 0:
                    continue
                time_diffe_min = time_diffe_sec/60
                plumeh = float(zeile[-6:])
                if plumeh>99:
                    h_C = 0
                else:
                    h_C=KF_a+KF_b*(plumeh*1000-vent_h)
                stacksort(time_diffe_min,h_C,unc_C,qf_C,source_C,1)

    uncertyC = [unc_ISKEF,unc_ISEGS,unc_Cband3,unc_Cband4,unc_Cband5,unc_Cband6]
    QF_C = [qfak_ISKEF,qfak_ISEGS,qfak_Cband3,qfak_Cband4,qfak_Cband5,qfak_Cband6]
    uncertyX = [unc_ISX1,unc_ISX2,unc_Xband3,unc_Xband4,unc_Xband5,unc_Xband6]
    QF_X = [qfak_ISX1,qfak_ISX2,qfak_Xband3,qfak_Xband4,qfak_Xband5,qfak_Xband6]
    
    for z in range (0,6):
        if ID[z]=="n.a.":
            huj=9
        else:
            
            try:
                Cbandfile = open(sens_file[z]+".txt", "r",encoding="utf-8", errors="surrogateescape")
                Cbandfile.close()
                if SensOO[z]==1:
                    logger3.info("checking ............"+ ID[z])
                    uncCband =uncertyC[z]*1000
                    radartimeC(sens_file[z],uncCband,QF_C[z],11+z)
                else:
                    logger3.info("---C-band radar "+ID[z]+" is switched off by operator!---")
            
            except EnvironmentError:
                logger3.warning("No "+ID[z]+" data found - check connection!")
                logger3.info("Continuing with next sensor")
  
        
    
    logger3.info("")
    logger3.info("***********************************************")
    logger3.info("Continuing with auto-stream X-band radar data")
    logger3.info("***********************************************")
    logger3.info("")
    
    def radartimeX (radarX_file, unc_X, qf_X, source_X):
        """reads X-radar data"""
        if source_X == 21:
            KF_a = cal_ISX1_a
            KF_b = cal_ISX1_b
        elif source_X == 22:
            KF_a = cal_ISX2_a
            KF_b = cal_ISX2_b
        elif source_X == 23:
            KF_a = cal_Xband3a
            KF_b = cal_Xband3b
        elif source_X == 24:
            KF_a = cal_Xband4a
            KF_b = cal_Xband4b
        elif source_X == 25:
            KF_a = cal_Xband5a
            KF_b = cal_Xband5b
        elif source_X == 26:
            KF_a = cal_Xband6a
            KF_b = cal_Xband6b


        global TimeNOW
        if run_type == 1:
            TimeNOW = datetime.datetime.utcnow()
        rlines = []
        with open(radarX_file+".txt", "r",encoding="utf-8", errors="surrogateescape") as ins:
            for line in ins:
                rlines.append(line)
        ins.close()
        l = len(rlines) - 1
        #        l=(len(rlines)-11) #This was right with the previous configuration

        if rlines[-1] == "":
            for x in range (2,l+1):
                zeile = rlines[-x]
                indate = zeile[:19]
                TimeX = datetime.datetime.strptime(indate, "%Y-%m-%d %H:%M:%S")
                time_diffe = TimeNOW - TimeX
                time_diffe_sec = time_diffe.total_seconds()
                if time_diffe_sec < 0:
                    continue
                time_diffe_min = time_diffe_sec/60
                plumeh = float(zeile[-6:])
                if plumeh>99:
                    h_X = 0
                else:
                    h_X= KF_a+KF_b*(plumeh*1000-vent_h)
     
                stacksort(time_diffe_min,h_X,unc_X,qf_X,source_X,1)
                
        else:
             for x in range (1,l):
                zeile = rlines[-x]
                indate = zeile[:19]
                TimeX = datetime.datetime.strptime(indate, "%Y-%m-%d %H:%M:%S")
                time_diffe = TimeNOW - TimeX
                time_diffe_sec = time_diffe.total_seconds()
                if time_diffe_sec < 0:
                    continue
                time_diffe_min = time_diffe_sec/60
                plumeh = float(zeile[-6:])
                if plumeh>99:
                    h_X = 0
                else:
                    h_X= KF_a+KF_b*(plumeh*1000-vent_h)

                stacksort(time_diffe_min,h_X,unc_X,qf_X,source_X,1)
    
    for zy in range (0,6):
        if ID[zy+6]=="n.a.":
            huj=10
        else:
            try:
                Xbandfile = open(sens_file[zy+6]+".txt", "r",encoding="utf-8", errors="surrogateescape")
                Xbandfile.close()
                if SensOO[zy+6]==1:
                    logger3.info("checking ............"+ ID[zy+6])
                    uncXband =uncertyX[zy]*1000
                    radartimeX(sens_file[zy+6],uncXband,QF_X[zy],21+zy)
                else:
                    logger3.info("---X-band radar "+ID[zy+6]+" is switched off by operator!---")
            
            except EnvironmentError:
                logger3.warning("No "+ID[zy+6]+" data found - check connection!")
                logger3.info("Continuing with next sensor")
    
    
    def GFZcam (GFZ_file, source_G):
        """reads GFZ Camera data"""
        global TimeNOW,gfz_vis,gfz_havg,gfz_hstd,l
        if run_type == 1:
            TimeNOW = datetime.datetime.utcnow()
        rlines = []
        gfz_vis,gfz_havg,gfz_hstd = np.loadtxt(GFZ_file+".txt",\
     usecols=(3,4,5), unpack=True, delimiter='\t')  
        with open(GFZ_file+".txt", "r",encoding="utf-8", errors="surrogateescape") as fp:
            for line in fp:
                rlines.append(line[:20])
        fp.close() 
      
        l = len(rlines)
        if l ==1:
        #issues if only one line, since array expected!
            if rlines[-1] == "":
                for x in range (0,l-1):
                    indate = rlines[x]
                    TimeG = datetime.datetime.strptime(indate, "%d-%b-%Y %H:%M:%S")
                    time_diffe = TimeNOW - TimeG
                    time_diffe_sec = time_diffe.total_seconds()
                    if time_diffe_sec < 0:
                        continue
                    time_diffe_min = time_diffe_sec/60
                    h_G = gfz_havg*1000
                    unc_G = gfz_hstd*1000
                    qf_G = gfz_vis                

                    stacksort(time_diffe_min,h_G,unc_G,qf_G,source_G,1)
                    
            else:
                 for x in range (0,l):
                     indate = rlines[x]
                     TimeG = datetime.datetime.strptime(indate, "%d-%b-%Y %H:%M:%S")
                     time_diffe = TimeNOW - TimeG
                     time_diffe_sec = time_diffe.total_seconds()
                     if time_diffe_sec < 0:
                         continue
                     time_diffe_min = time_diffe_sec/60
                     h_G = gfz_havg*1000
                     unc_G = gfz_hstd*1000
                     qf_G = gfz_vis

                     stacksort(time_diffe_min,h_G,unc_G,qf_G,source_G,1)
        else:
                    
            if rlines[-1] == "":
                for x in range (0,l-1):
                    indate = rlines[x]
                    TimeG = datetime.datetime.strptime(indate, "%d-%b-%Y %H:%M:%S")
                    time_diffe = TimeNOW - TimeG
                    time_diffe_sec = time_diffe.total_seconds()
                    if time_diffe_sec < 0:
                        continue
                    time_diffe_min = time_diffe_sec/60
                    h_G = gfz_havg[x]*1000
                    unc_G = gfz_hstd[x]*1000
                    qf_G = gfz_vis[x]                

                    stacksort(time_diffe_min,h_G,unc_G,qf_G,source_G,1)
                    
            else:
                 for x in range (0,l):
                     indate = rlines[x]
                     TimeG = datetime.datetime.strptime(indate, "%d-%b-%Y %H:%M:%S")
                     time_diffe = TimeNOW - TimeG
                     time_diffe_sec = time_diffe.total_seconds()
                     if time_diffe_sec < 0:
                         continue
                     time_diffe_min = time_diffe_sec/60
                     h_G = gfz_havg[x]*1000
                     unc_G = gfz_hstd[x]*1000
                     qf_G = gfz_vis[x]
                      
                     stacksort(time_diffe_min,h_G,unc_G,qf_G,source_G,1)
    
    logger3.info("")
    logger3.info("")
    logger3.info("******************************************")
    logger3.info("Continuing with auto-stream GFZ cam data")
    logger3.info("******************************************")
    logger3.info("")
    logger3.info("")
    
    for c in range (0,6):
        if ID[c+12] =="n.a.":
            huj=11
        else:
            try:
                Camfile = open(sens_file[c+12]+".txt", "r",encoding="utf-8", errors="surrogateescape")
                Camfile.close()
                if SensOO[c+12]==1:
                    logger3.info("checking ............" + ID[c+12])
                    GFZcam(sens_file[c+12],31+c)
        
                else:
                    logger3.info("---webcam "+ID[c+12]+" is switched off by operator!---")
            
            except EnvironmentError:
                logger3.warning("No "+ID[z+12]+" data found - check connection!")
                logger3.info("Continuing with next sensor")

    
    logger3.info("-------------------------------------")
    logger3.info("PLUME HEIGHT DATA SUMMARY REPORT:")
    
    logger3.info("-------------------------------------")
    
    N3h=0
    for x in range(0,len(stack3h)):
        
        N3h = int (N3h + stack3h[x][-1])
        
    N1h=0
    for x in range(0,len(stack1h)):
        
        N1h = int(N1h + stack1h[x][-1])
        
    N30min=0
    for x in range(0,len(stack30)):
        N30min = int(N30min + stack30[x][-1])
    
    N15min=0
    for x in range(0,len(stack15)):
        N15min = int(N15min + stack15[x][-1])
    
    logger3.info("number of plume height data considered by system:")
    logger3.info("within last 180 min: " +str(N3h))
    logger3.info("within last 60 min: " +str(N1h))
    logger3.info("within last 30 min: " +str(N30min))
    logger3.info("within last 15 min: " +str(N15min))
    logger3.info("-------------------------------------")
    logger3.info("-------------------------------------")
    logger3.info("")
    logger3.info("***** step 3 successful *****")
    logger3.info("")
    
    
    def PH_best(N,stack,twindow):
        if N == 0:
            logger4.warning("No plume height data - no calculation possible!")
            logger4.info("For a "+str(twindow)+"min time base\n")
            logger4.info("**   Canceled in step 4   **")
            code = 0
            Hmin = 0
            Havg = 0
            Hmax = 0
        if N == 1:
            logger4.debug("P.h. estimate based on N=1 data")
            logger4.debug("For a "+str(twindow)+"min time base")
            Hmin = stack[-1][1]
            if Hmin<0:
#1 Changed to avoid negative values
                #Hmin = 0
                Hmin = 1
            else:
                juh=0
            Havg = stack [-1][2]
            Hmax = stack[-1][3]
            code = 1
        
        if N== 2:
            logger4.info("P.h. estimate based on N=2 data")
            logger4.info("For a "+str(twindow)+"min time base\n")
            Max_hmin = max(stack[-1][1],stack[-2][1])
            Min_hmax_= min(stack[-1][3],stack[-2][3])
            Avg_havg = 0.5* (stack[-1][2] + stack[-2][2])
            Std_havg = (0.5)**0.5*((stack[-1][3]-stack[-1][2])**2 +(stack[-2][3]-stack[-2][2])**2)**(0.5)
            diff_havg = abs (max(stack[-1][2],stack[-2][2])\
    - min(stack[-1][3],stack[-2][3]))
            src_of01 = stack[-1][5]
            src_of02 = stack[-2][5]
            wfac01 = 0.01
            wfac02 = 0.01
            wfac01 = wfac01 + stack[-1][4]
            wfac02 = wfac01 + stack[-2][4]
            wtAvg = (wfac01*stack[-1][2]+wfac02*stack[-2][2])/(wfac01+wfac02)
            wtunc = (wfac01*(abs(stack[-1][3]-stack[-1][1]))+wfac02*(abs(stack[-2][3]-stack[-2][1])))/(wfac01+wfac02)
            if Min_hmax_ > Max_hmin:
            
                Havg = Avg_havg
                Hmin = Avg_havg - 0.5* Std_havg
                Hmax = Avg_havg + 0.5* Std_havg
                code = 2
            else:
                logger4.warning("2 divergent plume height data points!")
                if (src_of01<19 or 100<src_of01<109) and (src_of01<19 or 100<src_of01<109):
                    logger4.warning("plume height data from horizontal stepping radar only!\n")
                    Havg = Max_hmin
                    Hmin = Max_hmin - 0.5* wtunc 
                    Hmax = Max_hmin + 0.5* wtunc 
                    code = 21
                else:
                    #data from different sources
                    Havg = wtAvg
                    Hmin = wtAvg - 0.5* Std_havg 
                    Hmax = wtAvg + 0.5* Std_havg      
                    code = 22
#1 Added to avoid negative values
            if Hmin < 0:
                Hmin = 1
        if N>2:
            logger4.debug("P.h. estimate based on N="+str(N)+"data")
            logger4.debug("For a "+str(twindow)+"min time base\n")
            ar_stack = np.array(stack)
            hmin_stack = ar_stack[:,1]
            havg_stack = ar_stack[:,2]
            hmax_stack = ar_stack[:,3]
            hdiff_stack= ar_stack[:,3]-ar_stack[:,1]
            hdiff_2 = ar_stack[:,3]-ar_stack[:,2]
            Avg_havg = np.average(havg_stack[np.nonzero(havg_stack)])
            Min_hmax = np.min(hmax_stack[np.nonzero(hmax_stack)])
            Max_hmin = np.max(hmin_stack[np.nonzero(hmin_stack)])
            Bavg= 0.5 * (Min_hmax+Max_hmin)
            wa = 0.01
            wu = 0.01
            wf = 0.01

            for g in range (1,int(N)):

                wa = stack[g][4]*stack[g][2] + wa
                wf = stack[g][4] + wf
                wu = stack[g][4]*stack[g][1] + wu #minimum
           
            Whavg = wa/wf
            Wunc = Whavg - wu/wf
            Avg_diff = np.average(hdiff_stack[np.nonzero(hdiff_stack)])
            h_unc = N**(-0.5)*Avg_diff        
            Std_havg = np.std(havg_stack[np.nonzero(havg_stack)])
            sumdif = 0.0

            for a in range (0,int(N)):
                sumdif = hdiff_2[a]**2 + sumdif
            st_unc = (sumdif/N)**(0.5)
            
            if Avg_havg >= Min_hmax or Avg_havg<= Max_hmin:
                Havg = Whavg
                Hmin = Whavg - Wunc
                Hmax = Whavg + Wunc
                logger4.warning("!!! Plume height data poorly constrained !!!")
                logger4.info("For a "+str(twindow)+"min time base\n")
                code = 31
            else:
                Havg = Bavg
                Hmin = Bavg-st_unc
                Hmax = Bavg+st_unc
                code = 32
            if Hmin < 0:
                Hmin = 1
            logger4.debug("Hmin"+"\t"+"Havg"+"\t"+"Hmax"+"\t"+"code")
            logger4.debug(str(Hmin)+"\t"+str(Havg)+"\t"+str(Hmax)+"\t"+str(code))
        return(Hmin,Havg,Hmax,code)

    result3h_stack = PH_best(N3h,stack3h,180)#results plh 3h
    result1h_stack = PH_best(N1h,stack1h,60)
    result30_stack = PH_best(N30min,stack30,30) 
    result15_stack = PH_best(N15min,stack15,15) 

    if timebase == -1:
        proTB = 15 
    else:
        proTB = timebase
    
    if proTB == 15:
        ckcode = result15_stack[3]
    elif proTB == 30:
        ckcode = result30_stack[3]
    elif proTB == 60:
        ckcode = result1h_stack[3]
    elif proTB == 180:
        ckcode = result3h_stack[3]
    else:
        ckcode = result3h_stack[3]

    go_up = 0
    #check if there is any data within 15 minutes time base in case of Auto30
    if ckcode ==0:
        if TIMEBASE == 15 and timebase == -1:
            TIMEBASE = 30 #no data => switches back to 30 minutes time base
            logger4.info("** Time base automatically switched to 30 minutes, due to lack of data! **")
            ckcode = result30_stack[3]
            go_up = 1
        elif TIMEBASE == 30 and timebase == -1:
            ckcode = result30_stack[3]
        else:
            print()
            go_up = 0
    else:
        print()

    #write QUO_LOG
    qfct = open(out_txt+"_QUO_LOG.txt","a",encoding="utf-8", errors="surrogateescape")
    qfct.write(str(timin)+"\t"+str(ckcode)+"\t"+str(timebase)+"\n")
    qfct.close()

    #check if no data was within time frame of interest and if so skip all further steps
    if ckcode ==0:
        logger4.info("\n\n!! no new data within the selected time frame !!\n....MER computation steps skipped!\n\n")
        #winsound.Beep(Freq,Dur2)
        #winsound.Beep(Freq,Dur2)
        #winsound.Beep(Freq,Dur2)

    else:
        logger4.info("*** step 4 ***")
        logger4.info("resulting plume heights over vent \n >> time base: 15 minutes << : ")
        logger4.info("minimum: " + str(result15_stack[0])+ "m")
        logger4.info("best estimate: " + str(result15_stack[1])+ "m")
        logger4.info("maximum: " + str(result15_stack[2])+ "m")
        logger4.info("*")
        logger4.info("PHCC: " + str(result15_stack[3])) #code identifying plume height constraining method 
        logger4.info("*")
        logger4.info("*")
        logger4.info("resulting plume heights over vent \n >> time base: 30 minutes << : ")
        logger4.info("minimum: " + str(result30_stack[0])+ "m")
        logger4.info("best estimate: " + str(result30_stack[1])+ "m")
        logger4.info("maximum: " + str(result30_stack[2])+ "m")
        logger4.info("*")
        logger4.info("PHCC: " + str(result30_stack[3])) #code identifying plume height constraining method 
        logger4.info("*")
        logger4.info("*")
        logger4.info("resulting plume heights over vent \n >> time base: 60 minutes << : ")
        logger4.info("minimum: " + str(result1h_stack[0])+ "m")
        logger4.info("best estimate: " + str(result1h_stack[1])+ "m")
        logger4.info("maximum: " + str(result1h_stack[2])+ "m")
        logger4.info("*")
        logger4.info("PHCC: " + str(result1h_stack[3])) #code identifying plume height constraining method 
        logger4.info("*")
        logger4.info("*")
        logger4.info("resulting plume heights over vent \n >> time base: 180 minutes << : ")
        logger4.info("minimum: " + str(result3h_stack[0])+ "m")
        logger4.info("best estimate: " + str(result3h_stack[1])+ "m")
        logger4.info("maximum: " + str(result3h_stack[2])+ "m")
        logger4.info("*")
        logger4.info("PHCC: " + str(result3h_stack[3])) #code identifying plume height constraining method 
        logger4.info("*")
        logger4.info("*")
        

        def hbe_file(n,phmin,phbe,phmax,tiba):
            """ logs computed plumeheight summaries on time base tiba in a file"""
            global timin
            try:
                FILE1 = open(out_txt+"_hbe_"+str(tiba)+".txt", "a",encoding="utf-8", errors="surrogateescape")
                
                FILE1.write(str(timin) +"\t"+str(n)+"\t"+str(phmin)+"\t"+str(phbe)\
                +"\t"+str(phmax)+"\t"+str(tiba)+"\n")
                FILE1.close()
                   
            except EnvironmentError:
                FILE1 = open(out_txt+"_hbe_"+str(tiba)+".txt", "w",encoding="utf-8", errors="surrogateescape")
                logger4.info(">>>>>>>>>>>>new plume height best estimate log file written")
                
                FILE1.write(str(timin) +"\t"+str(n)+"\t"+str(phmin)+"\t"+str(phbe)\
                +"\t"+str(phmax)+"\t"+str(tiba)+"\n")
                FILE1.close()
                
        def plh_woo_file(phmin,phbe,phmax):
            """ logs plumeheight to be exported to Bristol on time base tiba in a file"""
            FILE2 = open(out_txt+"Foxi_hbe.txt", "a",encoding="utf-8", errors="surrogateescape")
            
            FILE2.write(str(timin) +"\t"+str(vulkan) +"\t"+str(vent_h)+"\t"+str(phmin)+"\t"+str(phbe)\
                +"\t"+str(phmax)+"\n")
            
            """ TO BE ACTIVATED WHEN PLUMERISE GETS GLOBAL!
            
            FILE2.write(str(timin) +"\t"+str(vulkan) +"\t"+str(vent_h)+"\t"+str(phmin)+"\t"+str(phbe)\
                +"\t"+str(phmax)+"\t"+str(volcLAT)+"\t"+str(volcLON)+"\n")
            """
            FILE2.close()

            TimeST = datetime.datetime.utcnow()
            TimeSTs = str(TimeST)
            YearSTs = TimeSTs[:4] 
            MonthSTs =TimeSTs[5:7]
            DaySTs =TimeSTs[8:10]
            HourSTs =TimeSTs[11:13]
            MinuteSTs =TimeSTs[14:16]
            stempel=str(YearSTs+MonthSTs+DaySTs+HourSTs+MinuteSTs)
            filename = "Foxi_hbe.txt"
            
            FILE8 = open(filename, "w",encoding="utf-8", errors="surrogateescape")
           
            FILE8.write(str(stempel)+"\n"+str(timin) +"\n"+str(vulkan) +"\n"+str(vent_h)+"\n"+str(phmin)+"\n"+str(phbe)\
                +"\n"+str(phmax)+"\n")
            
            """ TO BE ACTIVATED WHEN PLUMERISE GETS GLOBAL!
            FILE8.write(str(timin) +"\t"+str(vulkan) +"\t"+str(vent_h)+"\t"+str(phmin)+"\t"+str(phbe)\
                 +"\t"+str(phmax)+"\t"+str(volcLAT)+"\t"+str(volcLON)+"\n")
            """
            FILE8.close()       
            
# section which has to be adjusted to put your data on a webpage of your choice           
            #ftp = FTP("130.209.165.1")

        hbe_file(N3h,result3h_stack[0],result3h_stack[1],result3h_stack[2],180)
        hbe_file(N1h,result1h_stack[0],result1h_stack[1],result1h_stack[2],60)
        hbe_file(N30min,result30_stack[0],result30_stack[1],result30_stack[2],30)
        hbe_file(N15min,result15_stack[0],result15_stack[1],result15_stack[2],15)

        #HERE ADD ON OPTION POSSIBLE:
        
        if timebase == -1:
            #Timebase mode "AUTO30": working with timebase 30 min, unless change of  
            #pl.h. is more than 1.0km
            if go_up == 1:
                TIMEBASE = 30
            else:
                plh_grad = abs(result30_stack[1] - result15_stack[1])
                logger4.debug ("Change in plume height is: "+str(plh_grad)+"km")
                if plh_grad > 1000:
                    logger4.info("** automatically switched to time base mode 15MIN!**")
                    TIMEBASE = 15
                    hires_tiba = 15
                else:
                    TIMEBASE = 30
        else:
            TIMEBASE = timebase
        
        if TIMEBASE == 15:
            plh_woo_file(result15_stack[0],result15_stack[1],result15_stack[2])
        elif TIMEBASE == 30:
            plh_woo_file(result30_stack[0],result30_stack[1],result30_stack[2])
        elif TIMEBASE == 60:
            plh_woo_file(result1h_stack[0],result1h_stack[1],result1h_stack[2])
        else:
            plh_woo_file(result3h_stack[0],result3h_stack[1],result3h_stack[2])

        plot_indi_plh()
        del gc.garbage[:]
        logger4.info("***** step 4 successful *****")
        logger4.info("")
        
        def mer_WilWal(H_in):
            
            c_ww = 236 # Wilson & Walker, 1987 
            c_www = 295 # Wehrmann 2006
            c_wwa = 244 # Andronico 2007
            c_wws = 247 # Scollo 2008
            MER_ww=(H_in/c_ww)**4
            return(MER_ww)

        def mer_Sparks(H_in):
            
            V_sparks = (H_in/1670)**(1/0.259)
            M_sp = V_sparks * rho_dre
            return(M_sp)

        def mer_Mastin(H_in):
            rho_dre_M = 2500
            V_mastin = (H_in/2000)**(1/0.241)
            #M_ma = V_mastin * rho_dre_M
            M_ma = V_mastin * rho_dre
            return(M_ma)
        
        def mer_adjMastin(H_med,H_max):
            
            V_mtg = 0.0564*ki*((((H_med/1000) + (H_max/1000))/2)**4.15)
            M_mtg = rho_dre * V_mtg #Mastin, adjusted by Gudmundsson 2012
            logger5.debug("MTG: " + str(H_med)+"m "+ str(H_max)+"m "+ str(M_mtg)+"m ")
            return(M_mtg)

        def mer_woodhouse(H_in):
        # Solves for the Woodhouse et al. 2013 0D plume model
            g = 9.81  # gravitational acceleration (m s^-2)
            C_d = 998.  # specific heat capacity at constant pressure of dry air (J kg^-1 K^-1)
            Hplume_km = H_in/1000.
            if weather == 1:
                elaborate_weather(H_in)
                par_ws = (1 + 1.373*Ws)/(1 + 4.266*Ws + 0.3527*Ws**2)
                Mdot = 92.6171 * (Hplume_km/par_ws)**(1/0.253)
                result_Mdot = Mdot
            else:
                dummyH = [(x*10.) for x in range (0,int(int(H_in)/10+1))]

                #average square buoyancy frequency Nbar^2 = Gbar across height of the plume (s^-2)
                G1 = g**2./(C_d*theta_a0)*(1+C_d/g*tempGrad_1)
                G2 = g**2./(C_d*theta_a0)*(1+C_d/g*tempGrad_2)
                G3 = g**2./(C_d*theta_a0)*(1+C_d/g*tempGrad_3)

                gbar1=[G1 for hd in dummyH if hd <= H1]
                gbar2=[(G1*H1 + G2*(hd-H1))/hd for hd in dummyH if hd > H1 and hd <= H2]
                gbar3=[(G1*H1 + G2*(H2-H1) + G3*(hd-H2))/hd for hd in dummyH if hd > H2]

                for f in gbar2:
                    gbar1.append(f)
                for g in gbar3:
                    gbar1.append(g)

                Nbar=[g**.5 for g in gbar1]

                Ws_vec = [(1.44 * Vmax) / (Nbar[i] * H1) for i in range(0,len(Nbar))]
                par_ws_vec = [(1 + 1.373*Ws_vec[i])/(1 + 4.266*Ws_vec[i] + 0.3527*Ws_vec[i]**2)for i in range(0,len(Ws_vec))]
                Mdot = [92.6171 * (Hplume_km/par_ws_vec[i])**(1/0.253) for i in range(0,len(par_ws_vec))]

                result_Mdot = int(Mdot[-1])
            return(result_Mdot)

        def mer_degbon(H_in):
            g = 9.81 	#gravitational acceleration (m s^-2) 
            z_1 = 2.8 #maximum non-dimensional height (Morton et al.1956)
            R_d = 287. #specific gas constant of dry air (J kg^-1 K^- 1)
            C_d = 998.	#specific heat capacity at constant pressure of dry air (J kg^-1 K^-1) 
            C_s = 1250. #specific heat capacity at constant pressure of solids (J kg^-1 K^-1) 

            if weather == 1:
                elaborate_weather(H_in)
                rho_a0 = P_H_source / (R_d * T_H_source)
                gprime = g * (C_s * theta_0 - C_d * T_H_source) / (C_d * T_H_source)
                Mdot = math.pi*(rho_a0/gprime)*((((2.**(5./2.))*(alpha**2)*(N_avg**3))/(z_1**4.))*(H_in**4.)+(((beta**2)*(N_avg**2.)*(V_avg))/6.)*(H_in**3.))
                result_Mdot = Mdot
            else:
                dummyH = [(x*10.) for x in range (0,int(int(H_in)/10+1))]

                rho_a0 = P_0/(R_d*theta_a0)

                # reduced gravity (m s^-2)
                gprime = g*(C_s*theta_0-C_d*theta_a0)/(C_d*theta_a0)

                #average square buoyancy frequency Nbar^2 = Gbar across height of the plume (s^-2)
                G1 = g**2./(C_d*theta_a0)*(1+C_d/g*tempGrad_1)
                G2 = g**2./(C_d*theta_a0)*(1+C_d/g*tempGrad_2)
                G3 = g**2./(C_d*theta_a0)*(1+C_d/g*tempGrad_3)

                gbar1=[G1 for hd in dummyH if hd <= H1]
                gbar2=[(G1*H1 + G2*(hd-H1))/hd for hd in dummyH if hd > H1 and hd <= H2]
                gbar3=[(G1*H1 + G2*(H2-H1) + G3*(hd-H2))/hd for hd in dummyH if hd > H2]

                for f in gbar2:
                    gbar1.append(f)
                for g in gbar3:
                    gbar1.append(g)

                Nbar=[g**.5 for g in gbar1]

                # atmosphere wind profile (Bonadonna and Phillips, 2003)

                # average wind speed across height of the plume (m/s)
                Vbar=[Vmax*hd/H1/2. for hd in dummyH if hd <= H1]
                vbar2=[1./hd*(Vmax*H1/2. + Vmax*(hd-H1)-.9*Vmax/(H2-H1)*(hd-H1)**2./2.) for hd in dummyH if hd > H1 and hd <= H2]
                vbar3=[1./hd*(Vmax*H1/2. + .55*Vmax*(H2-H1)+.1*Vmax*(hd-H2)) for hd in dummyH if hd > H2]

                for w in vbar2:
                    Vbar.append(w)
                for x in vbar3:
                    Vbar.append(x)

                # equation (6) in Degruyter and Bonadonna, 2012
                Mdot = [math.pi*rho_a0/gprime*((2.**(5./2.)*alpha**2.*Nbar[i]**3./z_1**4.)*dummyH[i]**4. +(beta**2.*Nbar[i]**2.*Vbar[i]/6.)*dummyH[i]**3.) for i in range(0,len(Nbar))]
                result_Mdot = int(Mdot[-1])
            return(result_Mdot)
        
        def GreekPi(H_in):
            g = 9.81 	#gravitational acceleration (m s^-2) 
            z_1 = 2.8 #maximum non-dimensional height (Morton et al.1956)
            R_d = 287. #specific gas constant of dry air (J kg^-1 K^- 1)
            C_d = 998.	#specific heat capacity at constant pressure of dry air (J kg^-1 K^-1) 
            C_s = 1250. #specific heat capacity at constant pressure of solids (J kg^-1 K^-1) 

            if weather == 1:
                elaborate_weather(H_in)
                rho_a0 = P_H_source / (R_d * T_H_source)
                capitalGreekPi = 6.*((2.**(5./2.))/(z_1**4.))*((N_avg*H_in)/V_avg)*(alpha/beta)**2.

            else:

                dummyH = [(x*10.) for x in range (0,int(int(H_in)/10+1))]

                rho_a0 = P_0/(R_d*theta_a0)

                # adjusted gravity (m s^-2)
                gprime = g*(C_s*theta_0-C_d*theta_a0)/(C_d*theta_a0)

                #average square buoyancy frequency Nbar^2 = Gbar across height of the plume (s^-2)
                G1 = g**2./(C_d*theta_a0)*(1+C_d/g*tempGrad_1)
                G2 = g**2./(C_d*theta_a0)*(1+C_d/g*tempGrad_2)
                G3 = g**2./(C_d*theta_a0)*(1+C_d/g*tempGrad_3)

                gbar1=[G1 for hd in dummyH if hd <= H1]
                gbar2=[(G1*H1 + G2*(hd-H1))/hd for hd in dummyH if hd > H1 and hd <= H2]
                gbar3=[(G1*H1 + G2*(H2-H1) + G3*(hd-H2))/hd for hd in dummyH if hd > H2]

                for f in gbar2:
                    gbar1.append(f)
                for g in gbar3:
                    gbar1.append(g)

                Nbar=[g**.5 for g in gbar1]

                # atmosphere wind profile (Bonadonna and Phillips, 2003)

                # average wind speed across height of the plume (m/s)
                Vbar=[Vmax*hd/H1/2. for hd in dummyH if hd <= H1]
                vbar2=[1./hd*(Vmax*H1/2. + Vmax*(hd-H1)-.9*Vmax/(H2-H1)*(hd-H1)**2./2.) for hd in dummyH if hd > H1 and hd <= H2]
                vbar3=[1./hd*(Vmax*H1/2. + .55*Vmax*(H2-H1)+.1*Vmax*(hd-H2)) for hd in dummyH if hd > H2]

                for w in vbar2:
                    Vbar.append(w)
                for x in vbar3:
                    Vbar.append(x)
                capitalGreekPi= (6*2**(5/2))/(z_1**4)*(Nbar[-1]*H_in/Vbar[-1])*(alpha/beta)**2
            return(capitalGreekPi)

        def Woodh ():
            """reads Woodhouse data from file"""
            #!!! file should be a oneliner!!!
            global file_wood
            global Mwood
            global pr_date,pr_MERmin,pr_MERavg,pr_MERmax,pr_pradMin,pr_pradMax
            def asunicode_win(s):
                """Turns bytes into unicode, if needed.
                """
                if isinstance(s, bytes):
                    return s.decode(locale.getpreferredencoding())
                else:
                    return s
            data = urlopen(woodhlink)
            zz=0
            for line in data: # files are iterable
                zz=zz+1
                
                if zz ==1:
                    PR_date = asunicode_win(line)
                    pr_date = PR_date.strip("\n\r")
                elif zz == 3:
                    PR_MERmin = asunicode_win(line)
                    pr_MERmin = PR_MERmin.strip("\n") 
                elif zz == 4:
                    PR_MERavg = asunicode_win(line)
                    pr_MERavg = PR_MERavg.strip("\n")
                elif zz == 5:
                    PR_MERmax = asunicode_win(line)
                    pr_MERmax = PR_MERmax.strip("\n")
                elif zz == 6:
                    PR_pradMin = asunicode_win(line)
                    pr_pradMin = PR_pradMin.strip("\n")        
                elif zz == 7:
                    PR_pradMax = asunicode_win(line)
                    pr_pradMax = PR_pradMax.strip("\n")        
            FILE7 = open(out_txt+"_plumerise_log.txt", "a",encoding="utf-8", errors="surrogateescape") ##additional log file
            
            
            FILE7.write(str(pr_date) +"\t"+str(pr_MERmin)+"\t"+str(pr_MERavg)+"\t"+str(pr_MERmax)\
            +"\t"+str(pr_pradMin)+"\t"+str(pr_pradMax)+"\n")
            FILE7.close()            

            Mwoo = [pr_MERmin,pr_MERavg,pr_MERmax,pr_pradMin,pr_pradMax]
            return (Mwoo)
                     
        if oo_wood == 1:
            
            try:
                woofile = urlopen(woodhlink)   
                Mwood = Woodh() #Attention: now entrys treated as strings
                file_wood = 1 #indicates if Woodhouse is available and switched on
            except EnvironmentError:
                logger6.warning("No Woodhouse data file found - check connection!")
                Mwood = [0,0,0,0,0] 
                file_wood = 0
                wtf_wood = 0
        else:
            file_wood = 0
            Mwood = [0,0,0,0,0] 
            wtf_wood = 0
     
        """
        configuration of 4 mer_stack:
        MODEL
        0:MTG(!only one value!)
        1:WW [hmin,hbe,hmax],
        2:SP [hmin,hbe,hmax]
        3:MA [hmin,hbe,hmax]
        4:DB [hmin,hbe,hmax]
        5:WD0D [hmin,hbe,hmax]
        """
        wtf_wil = float(configlines[13])
        wtf_spa = float(configlines[14])
        wtf_mas = float(configlines[15])
        wtf_mtg = float(configlines[16])
        wtf_deg = float(configlines[17])
        wtf_wood0d = float(configlines[165])
        plh_correction = 1
        def centlcorr(H_in,min_DiaOBS,max_DiaOBS):
            global minPlRadius
            global maxPlRadius
            global plh_correction
            if GreekPi(H_in) > PI_THRESH: #vertically rising plume 
                minPlRadius = 0
                maxPlRadius = 0
            else:
                if max_DiaOBS == 0:
                    #if no observations then use PlumeRise estimates for radius
                    minPlRadius = float(Mwood[3])
                    maxPlRadius = float(Mwood[4])
                    if Mwood[4]==0:
                        plh_correction = 0
                        logger5.warning("*** Height of centerline cannot be estimated ***\n*** => modified Degruyter-Bonadonna model can't be considered! ***")
                        minPlRadius = 0
                        maxPlRadius = 0
                else:
                    minPlRadius = float(min_DiaOBS/2)
                    maxPlRadius = float(max_DiaOBS/2)
            return(minPlRadius,maxPlRadius)

        global PlumeRadiusMin, PlumeRadiusMax

        global currentAvgPlH #plume height for bent-over check according to current time base
        if timebase == 15:
            currentAvgPlH = result15_stack[1]
        elif timebase == 30:
            currentAvgPlH = result30_stack[1]
        elif timebase == -1: 
            currentAvgPlH = result30_stack[1] 
        elif timebase == 60:
            currentAvgPlH = result1h_stack[1]
        else:
            currentAvgPlH = result3h_stack[1]
            
        PlumeRadiusMin = float(centlcorr(currentAvgPlH,Min_DiaOBS,Max_DiaOBS)[0]) 
        PlumeRadiusMax = float(centlcorr(currentAvgPlH,Min_DiaOBS,Max_DiaOBS)[1]) 
        Min_DiaOBSold = float (2* PlumeRadiusMin)
        Max_DiaOBSold = float (2*PlumeRadiusMax)
        logger5.debug("*!! wtf Deg Bona is: " + str(wtf_deg))
        logger5.debug(str(Min_DiaOBSold))
        logger5.debug(str(Max_DiaOBSold))
        
        def mer_stack(res_stack,tib):
            """gives mer results, stack input according to time base"""    
            global wtf_deg
            H_min = res_stack[0]
            logger5.debug ("*************************************")
            logger5.debug ("H_min: "+str(H_min)+" m ")
            H_be = res_stack[1]
            logger5.debug ("H_be: "+ str(H_be)+" m ")
            H_max = res_stack[2]
            logger5.debug ("H_max: "+ str(H_max)+" m ")
            if res_stack[0]<PlumeRadiusMin:
                logger5.warning ("Supposed plume radius too large - Centreline height not considered")
                H_centrel_min = abs(res_stack[0])
            else:
                H_centrel_min = abs(res_stack[0] - PlumeRadiusMin)
            if res_stack[2]<PlumeRadiusMax:
                logger5.warning ("Supposed plume radius too large - Centreline height not considered")
                H_centrel_max = abs(res_stack[2])
            else:
                H_centrel_max = abs(res_stack[2] - PlumeRadiusMax)

            H_centrel_be = (H_centrel_max + H_centrel_min)/2
            logger5.debug ("H_centrel_min: "+ str(H_centrel_min)+" m ")
            logger5.debug ("H_centrel_be: "+ str(H_centrel_be)+" m ")
            logger5.debug ("H_centrel_max: "+str(H_centrel_max)+" m ")

            if plh_correction == 1:
                mer_restack=[mer_adjMastin(H_be,H_max),\
                [mer_WilWal(H_min),mer_WilWal(H_be),mer_WilWal(H_max)],\
                [mer_Sparks(H_min),mer_Sparks(H_be),mer_Sparks(H_max)],\
                [mer_Mastin(H_min), mer_Mastin(H_be),mer_Mastin(H_max)],\
                [mer_degbon(H_centrel_min),mer_degbon(H_centrel_be),mer_degbon(H_centrel_max)],\
                [mer_woodhouse(H_centrel_min),mer_woodhouse(H_centrel_be),mer_woodhouse(H_centrel_max)]]
            else:
                mer_restack=[mer_adjMastin(H_be,H_max),\
                [mer_WilWal(H_min),mer_WilWal(H_be),mer_WilWal(H_max)],\
                [mer_Sparks(H_min),mer_Sparks(H_be),mer_Sparks(H_max)],\
                [mer_Mastin(H_min), mer_Mastin(H_be),mer_Mastin(H_max)],\
                [mer_degbon(H_min),mer_degbon(H_be),mer_degbon(H_max)],\
                [mer_woodhouse(H_min),mer_woodhouse(H_be),mer_woodhouse(H_max)]]
            logger5.info ("::::::::::::::::::::::::::::::::::::::::::::::::")
            logger5.info("Computing plume height models")
            logger5.info (">>> time base: "+ str(tib) + " minutes <<<")
            logger5.info("best estimate plume height: "+str(round(H_be))+" m")
            logger5.info("...computation successful!")
            logger5.info("::::::::::::::::::::::::::::::::::::::::::::::::")
            logger5.info("")
            return(mer_restack)
        
        mer_stack3h = mer_stack(result3h_stack,180)
        mer_stack1h = mer_stack(result1h_stack,60)
        mer_stack30 = mer_stack(result30_stack,30)
        mer_stack15 = mer_stack(result15_stack,15)
        
        def allmer_file(n,hbe_used,model,merhmin,merhbe,merhmax,tiba):
            """ logs all computed mer values on time base tiba in a file"""
            try:
                FILE1 = open(out_txt+"_allmer_"+str(tiba)+".txt", "a",encoding="utf-8", errors="surrogateescape")
 
                FILE1.write(str(timin) +"\t"+str(n)+"\t"+str(hbe_used)+"\t"+str(model)\
                +"\t"+str(merhmin)+"\t"+str(merhbe)\
                +"\t"+str(merhmax)+"\t"+str(tiba)+"\n")
                FILE1.close()
                   
            except EnvironmentError:
                FILE1 = open(out_txt+"_allmer_"+str(tiba)+".txt", "w",encoding="utf-8", errors="surrogateescape")

                FILE1.write(str(timin) +"\t"+str(n)+"\t"+str(model)+"\t"+str(merhmin)+"\t"+str(merhbe)\
                +"\t"+str(merhmax)+"\t"+str(tiba)+"\n")
                FILE1.close()
          
         
        if analysis == 1:
            """
            ANALYSIS MODE: Calculates all models for all time bases and save them 
            in "allmer" file according to time bases
            """
            allmer_file(N3h,result3h_stack[1],0,0,mer_stack3h[0],0,180)
            allmer_file(N3h,result3h_stack[1],1,mer_stack3h[1][0],mer_stack3h[1][1],mer_stack3h[1][2],180)
            allmer_file(N3h,result3h_stack[1],2,mer_stack3h[2][0],mer_stack3h[2][1],mer_stack3h[2][2],180)
            allmer_file(N3h,result3h_stack[1],3,mer_stack3h[3][0],mer_stack3h[3][1],mer_stack3h[3][2],180)
            allmer_file(N3h,result3h_stack[1],4,mer_stack3h[4][0],mer_stack3h[4][1],mer_stack3h[4][2],180)
            allmer_file(N3h,result3h_stack[1],5,mer_stack3h[5][0],mer_stack3h[5][1],mer_stack3h[5][2], 180)
        
            allmer_file(N1h,result1h_stack[1],0,0,mer_stack1h[0],0,60)
            allmer_file(N1h,result1h_stack[1],1,mer_stack1h[1][0],mer_stack1h[1][1],mer_stack1h[1][2],60)
            allmer_file(N1h,result1h_stack[1],2,mer_stack1h[2][0],mer_stack1h[2][1],mer_stack1h[2][2],60)
            allmer_file(N1h,result1h_stack[1],3,mer_stack1h[3][0],mer_stack1h[3][1],mer_stack1h[3][2],60)
            allmer_file(N1h,result1h_stack[1],4,mer_stack1h[4][0],mer_stack1h[4][1],mer_stack1h[4][2],60)
            allmer_file(N1h,result1h_stack[1],5,mer_stack1h[5][0],mer_stack1h[5][1],mer_stack1h[5][2],60)
        
            allmer_file(N30min,result30_stack[1],0,0,mer_stack30[0],0,30)
            allmer_file(N30min,result30_stack[1],1,mer_stack30[1][0],mer_stack30[1][1],mer_stack30[1][2],30)
            allmer_file(N30min,result30_stack[1],2,mer_stack30[2][0],mer_stack30[2][1],mer_stack30[2][2],30)
            allmer_file(N30min,result30_stack[1],3,mer_stack30[3][0],mer_stack30[3][1],mer_stack30[3][2],30)
            allmer_file(N30min,result30_stack[1],4,mer_stack30[4][0],mer_stack30[4][1],mer_stack30[4][2],30)
            allmer_file(N30min,result30_stack[1],5,mer_stack30[5][0],mer_stack30[5][1],mer_stack30[5][2],30)
            
            allmer_file(N15min,result15_stack[1],0,0,mer_stack15[0],0,15)
            allmer_file(N15min,result15_stack[1],1,mer_stack15[1][0],mer_stack15[1][1],mer_stack15[1][2],15)
            allmer_file(N15min,result15_stack[1],2,mer_stack15[2][0],mer_stack15[2][1],mer_stack15[2][2],15)
            allmer_file(N15min,result15_stack[1],3,mer_stack15[3][0],mer_stack15[3][1],mer_stack15[3][2],15)
            allmer_file(N15min,result15_stack[1],4,mer_stack15[4][0],mer_stack15[4][1],mer_stack15[4][2],15)
            allmer_file(N15min,result15_stack[1],5,mer_stack15[5][0],mer_stack15[5][1],mer_stack15[5][2],15)
            logger5.info("\n Analysis mode: switched ON")
            logger5.warning("ALL individual MER values are logged \"in _allmer_\" files!")
            logger5.warning("Source Stats Plots are activated!")
            logger5.info("")
        else:
            logger5.info("")
            logger5.info("Analysis mode switched off -> no individual MER logged")
            logger5.info("")
        
        logger5.info("***** step 5 successful *****")
        """
        compute 
        for specific timebase
        MERMIN_hmin: Min(MER(hmin)) ... out of 4 models     -absolute thinkable minimum
        MERMAX_hmin: Max(MER(hmin)) ... out of 4 models     -lower boundary
        MERWE:  wAVG(MER(hbe,mtg)) ... out of 5 models      -weighted average
        MERMTG: MERmtg(hbe)        ... out of 1 model       -result of model scaled by ground truth
        MERDB:  MERdb(hbe)         ... out of 1 model       -result of wind affected model
        MERMAX_PLUS wAVG(MER(hmax,mtg)) ... out of 5 models -potential upper boundary
        Max(MER(hmax))                  ... out of 4 models -absolute thinkable maximum
        R_MER: AVG(MERMAX_hmin,MERWE,MERMAX_PLUS)           -
        MERmaxNowiHmin: MERMAX_hmin with the 3 not wind-affected models 
        """
       
        
        def stat_mer(stack_mer):
            """computes statistical MER numbers for REFIR-internal models (RMER)"""
            mermtg = stack_mer[0]
            merdb = stack_mer[4][1]
            merwd0d = stack_mer[5][1]
            tempstack = [stack_mer[1][0], stack_mer[2][0], stack_mer[3][0], stack_mer[4][0], stack_mer[5][0]]
            # Initializes model switches
            if tempstack != [0.0, 0.0, 0.0, 0.0, 0.0]:
                a = np.array(tempstack)
                mermin_hmin = np.min(a.ravel()[np.flatnonzero(a)])
            else:
                mermin_hmin = 0
                logger6.info("NO DATA!")

            def model_switches():
                if wtf_wil == 0:
                    wil_on = 0
                else:
                    wil_on = 1

                if wtf_spa == 0:
                    spa_on = 0
                else:
                    spa_on = 1

                if wtf_mas == 0:
                    mas_on = 0
                else:
                    mas_on = 1

                if wtf_deg == 0:
                    deg_on = 0
                else:
                    deg_on = 1

                if wtf_wood0d == 0:
                    wood0d_on = 0
                else:
                    wood0d_on = 1

                if wtf_mtg == 0:
                    mtg_on = 0
                else:
                    mtg_on = 1
                return wil_on, spa_on, mas_on, deg_on, wood0d_on, mtg_on

            [wil_on,spa_on,mas_on,deg_on,wood0d_on,mtg_on] = model_switches()

            mermax_hmin = (wtf_wil*stack_mer[1][0]+wtf_spa*stack_mer[2][0]+\
            +wtf_mas*stack_mer[3][0]+wtf_deg*stack_mer[4][0]+wtf_wood0d*stack_mer[5][0])/(wtf_wil+\
            wtf_spa+wtf_mas+wtf_deg+wtf_wood0d)

            QmaxNowiHmin = min(max(wil_on*stack_mer[1][0],spa_on*stack_mer[2][0],mas_on*stack_mer[3][0]),min(wil_on*stack_mer[1][1],spa_on*stack_mer[2][1],mas_on*stack_mer[3][1]))

            merwe = (wtf_wil*stack_mer[1][1]+wtf_spa*stack_mer[2][1]+\
            +wtf_mas*stack_mer[3][1]+wtf_deg*stack_mer[4][1]+wtf_wood0d*stack_mer[5][1]+wtf_mtg*stack_mer[0])/(wtf_wil+\
            wtf_spa+wtf_mas+wtf_mtg+wtf_deg+wtf_wood0d)

            logger6.info("MERWE >>> " + str(merwe))

            meravg = (1*stack_mer[1][1]+1*stack_mer[2][1]+\
            +1*stack_mer[3][1]+1*stack_mer[4][1]+1*stack_mer[5][1]+1*stack_mer[0])/5

            mermaxplus = (wtf_wil*stack_mer[1][2]+wtf_spa*stack_mer[2][2]+\
            +wtf_mas*stack_mer[3][2]+wtf_deg*stack_mer[4][2]+wtf_wood0d*stack_mer[5][2])/(wtf_wil+\
            wtf_spa+wtf_mas+wtf_deg+wtf_wood0d)
            
            mermax_hmax =max(mtg_on*stack_mer[0],wil_on*stack_mer[1][2],spa_on*stack_mer[2][2],mas_on*stack_mer[3][2],deg_on*stack_mer[4][2],wood0d_on*stack_mer[5][2])
            
            Rmer = (QmaxNowiHmin + mermaxplus + merwe)/3.0
            if QmaxNowiHmin == 0:
                Rmer = (mermaxplus + merwe) / 2.0
            logger6.info("RMER >>> "+str(Rmer))
            
            mer_stat= [0,0,0,0,0,0,0,0,0,0,0]
            mer_stat[0] = mermin_hmin
            mer_stat[1] = mermax_hmin
            mer_stat[2] = merwe
            mer_stat[3] = mermaxplus
            mer_stat[4] = mermax_hmax
            mer_stat[5] = mtg_on*mermtg
            mer_stat[6] = deg_on*merdb
            mer_stat[7] = Rmer
            mer_stat[8] = meravg
            mer_stat[9] = QmaxNowiHmin
            mer_stat[10] = wood0d_on*merwd0d
            return(mer_stat)
    
        
        def stat2_mer(stack_mer):
            """computes statistical MER numbers for conventional models (CMER)"""
            mermtg = stack_mer[0]
            merdb = stack_mer[4][1]
            merwd0d = stack_mer[5][1]
            tempstack = [stack_mer[1][0], stack_mer[2][0], stack_mer[3][0], stack_mer[4][0], stack_mer[5][0]]
            if tempstack != [0.0, 0.0, 0.0, 0.0, 0.0]:
                a = np.array(tempstack)
                mermin_hmin = np.min(a.ravel()[np.flatnonzero(a)])
            else:
                mermin_hmin = 0
                logger6.info("NO DATA!")

            def model_switches():
                if wtf_wil == 0:
                    wil_on = 0
                else:
                    wil_on = 1

                if wtf_spa == 0:
                    spa_on = 0
                else:
                    spa_on = 1

                if wtf_mas == 0:
                    mas_on = 0
                else:
                    mas_on = 1

                if wtf_deg == 0:
                    deg_on = 0
                else:
                    deg_on = 1

                if wtf_wood0d == 0:
                    wood0d_on = 0
                else:
                    wood0d_on = 1

                if wtf_mtg == 0:
                    mtg_on = 0
                else:
                    mtg_on = 1

                if wtf_wood == 0:
                    wood_on = 0
                else:
                    wood_on = 1
                return wil_on, spa_on, mas_on, deg_on, wood0d_on, mtg_on, wood_on

            [wil_on, spa_on, mas_on, deg_on, wood0d_on, mtg_on, wood_on] = model_switches()

            mermax_hmin = (wtf_wil*stack_mer[1][0]+wtf_spa*stack_mer[2][0]+\
            +wtf_mas*stack_mer[3][0]+wtf_deg*stack_mer[4][0]+wtf_wood0d*stack_mer[5][0]+wtf_wood*float(Mwood[2]))/(wtf_wil+\
            wtf_spa+wtf_mas+wtf_deg+wtf_wood0d+wtf_wood)

            QmaxNowiHmin = min(max(wil_on*stack_mer[1][0],spa_on*stack_mer[2][0],mas_on*stack_mer[3][0]),min(wil_on*stack_mer[1][1],spa_on*stack_mer[2][1],mas_on*stack_mer[3][1]))
            merwe1 = (wtf_wil*stack_mer[1][1]+wtf_spa*stack_mer[2][1]+\
            +wtf_mas*stack_mer[3][1]+wtf_deg*stack_mer[4][1]+wtf_wood0d*stack_mer[5][1]+wtf_mtg*stack_mer[0])/(wtf_wil+\
            wtf_spa+wtf_mas+wtf_mtg+wtf_deg+wtf_wood0d)
            
            merwe = (wtf_5MER*merwe1 + wtf_wood*float(Mwood[1]))/(wtf_5MER+wtf_wood)
            
            meravg = (1*stack_mer[1][1]+1*stack_mer[2][1]+\
            +1*stack_mer[3][1]+1*stack_mer[4][1]+1*stack_mer[5][1]+1*stack_mer[0]+float(Mwood[1]))/6

            mermaxplus1 = (wtf_wil*stack_mer[1][2]+wtf_spa*stack_mer[2][2]+\
            +wtf_mas*stack_mer[3][2]+wtf_deg*stack_mer[4][2]+wtf_wood0d*stack_mer[5][2])/(wtf_wil+\
            wtf_spa+wtf_mas+wtf_deg+wtf_wood0d)

            mermaxplus = (wtf_5MER*mermaxplus1 + wtf_wood*float(Mwood[2]))/(wtf_5MER+wtf_wood)
            
            mermax_hmax =max(mtg_on*stack_mer[0],wil_on*stack_mer[1][2],spa_on*stack_mer[2][2],mas_on*stack_mer[3][2], \
                             deg_on *stack_mer[4][2],wood0d_on*stack_mer[5][2],wood_on*float(Mwood[2]))
            
            Rmer = (QmaxNowiHmin + mermaxplus + merwe)/3.0 #Note that this "Rmer" is now in fact Cmer
            logger6.info("CMER >>> "+str(Rmer))
            
            mer_stat= [0,0,0,0,0,0,0,0,0,0,0]
            mer_stat[0] = mermin_hmin
            mer_stat[1] = mermax_hmin
            mer_stat[2] = merwe
            mer_stat[3] = mermaxplus
            mer_stat[4] = mermax_hmax
            mer_stat[5] = mtg_on*mermtg
            mer_stat[6] = deg_on*merdb
            mer_stat[7] = Rmer
            mer_stat[8] = meravg
            mer_stat[9] = QmaxNowiHmin
            mer_stat[10] = wood0d_on*merwd0d
            return(mer_stat)  
    
    
        if file_wood == 0:
            MER_Stat3h = stat_mer(mer_stack3h)#gives statistical results for timebase 3h
            MER_Stat1h = stat_mer(mer_stack1h)
            MER_Stat30 = stat_mer(mer_stack30)
            MER_Stat15 = stat_mer(mer_stack15)
        else:
            MER_Stat3h = stat2_mer(mer_stack3h)#gives statistical results for timebase 3h with Woodhouse
            MER_Stat1h = stat2_mer(mer_stack1h)
            MER_Stat30 = stat2_mer(mer_stack30)
            MER_Stat15 = stat2_mer(mer_stack15)

        def merstat_file(n,mer_stat,tiba):
            """ logs statistic summary of  MER on spec. time base tiba in a file"""
            try:
                FILE1 = open(out_txt+"_statmer_"+str(tiba)+".txt", "a",encoding="utf-8", errors="surrogateescape")
                
                FILE1.write(str(timin) +"\t"+str(n)+"\t"+str(mer_stat[0])+"\t"+str(mer_stat[1])\
                +"\t"+str(mer_stat[2])+"\t"+str(mer_stat[3])\
                +"\t"+str(mer_stat[4])+"\t"+str(mer_stat[5])+"\t"+str(mer_stat[6])+\
                "\t"+str(mer_stat[7])+"\t"+str(mer_stat[8])+"\t"+str(mer_stat[9])+"\t"+str(tiba)+"\n")
                FILE1.close()
            except EnvironmentError:
                FILE1 = open(out_txt+"_statmer_"+str(tiba)+".txt", "w",encoding="utf-8", errors="surrogateescape")
                
                FILE1.write(str(timin) +"\t"+str(n)+"\t"+str(mer_stat[0])+"\t"+str(mer_stat[1])\
                +"\t"+str(mer_stat[2])+"\t"+str(mer_stat[3])\
                +"\t"+str(mer_stat[4])+"\t"+str(mer_stat[5])+"\t"+str(mer_stat[6])+\
                "\t"+str(mer_stat[7])+"\t"+str(mer_stat[8])+"\t"+str(mer_stat[9])+"\t"+str(tiba)+"\n")
                FILE1.close()
        
        if analysis == 1:
            merstat_file(N3h,MER_Stat3h,180)
            merstat_file(N1h,MER_Stat1h,60)
            merstat_file(N30min,MER_Stat30,30)
            merstat_file(N15min,MER_Stat15,15)
            logger6.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            logger6.info ("\n Analysis mode: switched ON")
            logger6.info ("MER stats logged for ALL time bases in \"_statmer_\" files!")
            print("")
        else:
             logger6.info ("\n NOTE: analysis mode: switched OFF -> MER timbase stats not logged")
        
        def save_current_mer(n,mer_stat,tiba):
            """gives current overall MER - always overwritten"""
            global cur_MERwood_avg
            global Qf_absmin,Qf_absmax,a_man,Qfmer_min,Qfmer_max,Qfmer
            if mer_stat[6] == 0:
                if float(Mwood[1]) == 0:    
                    cur_Qlower = min (mer_stat[1],mer_stat[9])
                else:
                    cur_Qlower = min (mer_stat[1],mer_stat[9],float(Mwood[1]))
            else:
                if cur_MERwood_avg == 0:    
                    cur_Qlower = min (mer_stat[1],mer_stat[9],mer_stat[6])
                else:
                    cur_Qlower = min (mer_stat[1],mer_stat[9],float(Mwood[1]),mer_stat[6])


            Qlower = cur_Qlower
            FILE1 = open(out_txt+"_mer_NOW.txt", "w",encoding="utf-8", errors="surrogateescape")
            
            FILE1.write(str(timin) +"\t"+str(n)+"\t"+str(mer_stat[0])+"\t"+str(mer_stat[1])\
            +"\t"+str(mer_stat[2])+"\t"+str(mer_stat[3])+"\t"+str(mer_stat[4])+"\t"\
            +str(mer_stat[5])+"\t"+str(mer_stat[6])+\
            "\t"+str(mer_stat[7])+"\t"+str(mer_stat[8])+"\"t"+ str(Qlower)+"\t"\
+str(mer_stat[9])+"\t"+str(Qf_absmin)+"\t"\
+str(Qf_absmax)+"\t"+str(Qfmer_min)+"\t"+str(Qfmer)+"\t"+str(Qfmer_max)+"\t"+str(tiba)+"\n")
            FILE1.close()
        

        def save_mer_logfile(n,hbe,mer_stat,MERww,MERsp,MERma,MERwood0d,tiba):
            """ logs continously statistic summary of MER in a file"""
            global cur_hbe,cur_hbe_min,cur_hbe_max,cur_MERMIN_hmin,cur_MERMAX_hmin,\
    cur_MERWE,cur_MERMAX_PLUS,cur_MaxMERhmax,cur_MERww,cur_MERsp,cur_MERma,\
    cur_MERmtg,cur_MERdb,cur_RMER,cur_MERavg,cur_MERwood_min,cur_MERwood_avg,\
    cur_MERwood_max, cur_N,cur_QmaxNowiHmin, cur_Qlower, cur_PlumeRadiusMin, cur_PlumeRadiusMax
            global Qf_absmin,Qf_absmax,a_man,Qfmer_min,Qfmer_max,Qfmer
            global dt_sec, timin_sec_cum
            global hbe_min_sum, hbe_sum, hbe_max_sum, Qfmer_min_sum, Qfmer_sum, Qfmer_max_sum, ndata, nsources, NAME_out_on
            cur_N = n
            cur_hbe = int(hbe) # current b.e. plume height
            cur_hbe_min = int(hbe_min)
            cur_hbe_max = int(hbe_max)
            cur_MERMIN_hmin = mer_stat[0]
            cur_MERMAX_hmin = mer_stat[1]
            cur_MERWE = mer_stat[2]
            cur_MERMAX_PLUS = mer_stat[3]
            cur_MaxMERhmax = mer_stat[4]
            cur_MERww = MERww
            cur_MERsp = MERsp
            cur_MERma = MERma
            cur_MERwood0d = MERwood0d
            cur_MERmtg = mer_stat[5]
            cur_MERdb = mer_stat[6]
            cur_RMER = mer_stat[7]
            cur_MERavg = mer_stat[8]
            cur_QmaxNowiHmin = mer_stat[9]
            cur_MERwood_min = float(Mwood[0])
            cur_MERwood_avg = float(Mwood[1])
            cur_MERwood_max = float(Mwood[2])
            cur_Qlower = mer_stat[1]
            cur_PlumeRadiusMin = PlumeRadiusMin
            cur_PlumeRadiusMax = PlumeRadiusMax


            FILE1 = open(out_txt+"_mer_LOG.txt", "a",encoding="utf-8", errors="surrogateescape")
            FILE1.write(str(timin) +"\t"+str(n)+"\t"+str(hbe)+"\t"\
            +str(mer_stat[0])+"\t"+str(mer_stat[1])\
            +"\t"+str(mer_stat[2])+"\t"+str(mer_stat[3])+"\t"+str(mer_stat[4])+\
            "\t"+str(wtf_wil)+"\t"+str(wtf_spa)+"\t"+str(wtf_mas)+"\t"+str(wtf_mtg)\
            +"\t"+str(wtf_deg)+"\t"+str(MERww)+"\t"+str(MERsp)+"\t"+str(MERma)+"\t"+str(mer_stat[5])+\
           "\t"+str(mer_stat[6])+"\t"+str(mer_stat[7])+"\t"+str(mer_stat[8])+"\t"\
+str(Mwood[0])+"\t"+str(Mwood[1])+"\t"+str(Mwood[2])+"\t"\
+str(OBS_on)+"\t"+str(theta_a0)+"\t"+str(P_0)+"\t"+str(theta_0)+"\t"+str(rho_dre)+"\t"\
+str(alpha)+"\t"+str(beta)+"\t"+str(wtf_wil)+"\t"+str(wtf_spa)+"\t"+str(wtf_mas)+"\t"\
+str(wtf_mtg)+"\t"+str(wtf_deg)+"\t"+str(H1)+"\t"+str(H2)+"\t"+str(tempGrad_1)+"\t"\
+str(tempGrad_2)+"\t"+str(tempGrad_3)+"\t"+str(Vmax)+"\t"+str(ki)+"\t"+str(qfak_ISKEF)+"\t"\
+str(qfak_ISEGS)+"\t"+str(qfak_ISX1)+"\t"+str(qfak_ISX2)+"\t"+str(qfak_GFZ1)+"\t"+str(qfak_GFZ2)+"\t"\
+str(qfak_GFZ3)+"\t"+str(unc_ISKEF)+"\t"+str(unc_ISEGS)+"\t"+str(unc_ISX1)+"\t"+str(unc_ISX2)+"\t"\
+str(vent_h)+"\t"+str(ISKEF_on)+"\t"+str(ISEGS_on)+"\t"+str(ISX1_on)+"\t"+str(ISX2_on)+"\t"\
+str(GFZ1_on)+"\t"+str(GFZ2_on)+"\t"+str(GFZ3_on)+"\t"+str(analysis)+"\t"+str(timebase)+"\t"\
+str(oo_exp)+"\t"+str(oo_con)+"\t"+str(wtf_exp)+"\t"+str(wtf_con)+"\t"+str(cur_MERMAX_PLUS)+"\t"\
+str(a_man)+"\t"+str(min_manMER)+"\t"+str(max_manMER)+"\t"+str(oo_wood)+"\t"+str(oo_5MER)+"\t"\
+str(wtf_wood)+"\t"+str(wtf_5MER)+"\t"+str(oo_isound)+"\t"+str(wtf_isound)+"\t"+str(oo_esens)+"\t"\
+str(wtf_esens)+"\t"+str(oo_pulsan)+"\t"+str(wtf_pulsan)+"\t"+str(oo_scatter)+"\t"+str(wtf_scatter)+"\t"\
+str(cal_ISKEF_a)+"\t"+str(cal_ISKEF_b)+"\t"+str(cal_ISEGS_a)+"\t"+str(cal_ISEGS_b)+"\t"+str(cal_ISX1_a)+"\t"\
+str(cal_ISX1_b)+"\t"+str(cal_ISX2_a)+"\t"+str(cal_ISX2_b)+"\t"+str(ISKEFm_on)+"\t"+str(ISEGSm_on)+"\t"\
+str(ISX1m_on)+"\t"+str(ISX2m_on)+"\t"+str(hbe_min)+"\t"+str(hbe_max)+"\t"\
+str(cur_QmaxNowiHmin)+"\t"\
+str(result15_stack[0])+"\t"+str(result15_stack[1])+"\t"+str(result15_stack[2])+"\t"\
+str(result30_stack[0])+"\t"+str(result30_stack[1])+"\t"+str(result30_stack[2])+"\t"\
+str(result1h_stack[0])+"\t"+str(result1h_stack[1])+"\t"+str(result1h_stack[2])+"\t"\
+str(result3h_stack[0])+"\t"+str(result3h_stack[1])+"\t"+str(result3h_stack[2])+"\t"\
+str(cur_Qlower)+"\t"+str(wemer_min)+"\t"+str(wemer_avg)+"\t"+str(wemer_max)+"\t"\
+str(mwmer_min)+"\t"+str(mwmer_avg)+"\t"+str(mwmer_max)+"\t"+str(Qf_absmin)+"\t"\
+str(Qf_absmax)+"\t"+str(Qfmer_min)+"\t"+str(Qfmer)+"\t"+str(Qfmer_max)+"\t"\
+str(PlumeRadiusMin)+"\t"+str(PlumeRadiusMax)+"\t"+"-99"+"\t"+"-99"+"\t"+str(tiba)+"\t"\
+ str(time_tveir)+"\t"+str(Cband3_on)+"\t"+str(Cband4_on)+"\t"+str(Cband5_on)+"\t"\
+str(Cband6_on)+"\t"+str(Xband3_on)+"\t"+str(Xband4_on)+"\t"+str(Xband5_on)+"\t"\
+str(Xband6_on)+"\t"+str(Cam4_on)+"\t"+str(Cam5_on)+"\t"+str(Cam6_on)+\
"\t"+str(Cband3m_on)+"\t"+str(Cband4m_on)+"\t"+str(Cband5m_on)+"\t"+str(Cband6m_on)+\
"\t"+str(Xband3m_on)+"\t"+str(Xband4m_on)+"\t"+str(Xband5m_on)+"\t"+str(Xband6m_on)+\
"\t"+str(cal_Cband3a)+"\t"+str(cal_Cband3b)+"\t"+str(cal_Cband4a)+"\t"+str(cal_Cband4b)+\
"\t"+str(cal_Cband5a)+"\t"+str(cal_Cband5b)+"\t"+str(cal_Cband6a)+"\t"+str(cal_Cband6b)+\
"\t"+str(cal_Xband3a)+"\t"+str(cal_Xband3b)+"\t"+str(cal_Xband4a)+"\t"+str(cal_Xband4b)+\
"\t"+str(cal_Xband5a)+"\t"+str(cal_Xband5b)+"\t"+str(cal_Xband6a)+"\t"+str(cal_Xband6b)+\
"\t"+str(unc_Cband3)+"\t"+str(unc_Cband4)+"\t"+str(unc_Cband5)+"\t"+str(unc_Cband6)+\
"\t"+str(unc_Xband3)+"\t"+str(unc_Xband4)+"\t"+str(unc_Xband5)+"\t"+str(unc_Xband6)+\
"\t"+str(qfak_Cband3)+"\t"+str(qfak_Cband4)+"\t"+str(qfak_Cband5)+"\t"+str(qfak_Cband6)+\
"\t"+str(qfak_Xband3)+"\t"+str(qfak_Xband4)+"\t"+str(qfak_Xband5)+"\t"+str(qfak_Xband6)+\
"\t"+str(qfak_Cam4)+"\t"+str(qfak_Cam5)+"\t"+str(qfak_Cam6)+"\t"+str(wtf_wood0d)+"\t"+str(MERwood0d)+"\n")
            FILE1.close()
            FILE2 = open(out_txt + "_FMER.txt", "a",encoding="utf-8", errors="surrogateescape")
            FILE2.write(str(TimeNOW) + "\t" + str(timin) + "\t" + str(Qfmer_min) + "\t" + str(Qfmer) + "\t" + str(
                Qfmer_max) + "\n")
            FILE2.close()
            FILE3 = open(out_txt + "_PLH.txt", "a",encoding="utf-8", errors="surrogateescape")
            FILE3.write(
                str(TimeNOW) + "\t" + str(timin) + "\t" + str(hbe_min) + "\t" + str(hbe) + "\t" + str(hbe_max) + "\n")
            FILE3.close()

# Time averaged variables
            if NAME_out_on == 1 and PM_TAV == 0:
                NAME_out_on = 0 #NAME source file cannot be written if the time averaging of the output is not activated
            timin_sec_cum = timin_sec_cum + dt_sec
            if PM_TAV != 0:
                FILE13 = open(out_txt + "_tavg_PLH.txt", "a",encoding="utf-8", errors="surrogateescape")
                FILE14 = open(out_txt + "_tavg_FMER.txt", "a", encoding="utf-8", errors="surrogateescape")
                if NAME_out_on == 1:
                    FILE15 = open(out_txt + "_NAME_sources_avg.txt", "a", encoding="utf-8", errors="surrogateescape")
                    FILE15_writer = csv.writer(FILE15, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    FILE16 = open(out_txt + "_NAME_sources_max.txt", "a", encoding="utf-8", errors="surrogateescape")
                    FILE16_writer = csv.writer(FILE16, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    FILE17 = open(out_txt + "_NAME_sources_min.txt", "a", encoding="utf-8", errors="surrogateescape")
                    FILE17_writer = csv.writer(FILE17, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                ndata = ndata + 1
                hbe_min_sum = hbe_min_sum + hbe_min * dt_sec
                hbe_sum = hbe_sum + hbe * dt_sec
                hbe_max_sum = hbe_max_sum + hbe_max * dt_sec
                Qfmer_min_sum = Qfmer_min_sum + Qfmer_min * dt_sec
                Qfmer_sum = Qfmer_sum + Qfmer * dt_sec
                Qfmer_max_sum = Qfmer_max_sum + Qfmer_max * dt_sec
                if PM_TAV == 1:
                    if run > 1 and timin_sec_cum % 900 < 299:
                        hbe_min_tavg = hbe_min_sum / timin_sec_cum
                        hbe_tavg = hbe_sum / timin_sec_cum
                        hbe_max_tavg = hbe_max_sum / timin_sec_cum
                        hbe_min_tavg_str = '{0:.4E}'.format(hbe_min_tavg)
                        hbe_tavg_str = '{0:.4E}'.format(hbe_tavg)
                        hbe_max_tavg_str = '{0:.4E}'.format(hbe_max_tavg)
                        Qfmer_min_tavg = Qfmer_min_sum / timin_sec_cum
                        Qfmer_tavg = Qfmer_sum / timin_sec_cum
                        Qfmer_max_tavg = Qfmer_max_sum / timin_sec_cum
                        FILE13.write(str(TimeNOW) + "\t" + str(timin) + "\t" + str(hbe_min_tavg) + "\t" + str(hbe_tavg) +
                                     "\t" + str(hbe_max_tavg) + "\n")
                        FILE14.write(str(TimeNOW) + "\t" + str(timin) + "\t" + str(Qfmer_min_tavg) + "\t" + str(Qfmer_tavg) +
                                     "\t" + str(Qfmer_max_tavg) + "\n")
                        if NAME_out_on == 1:
                            nsources = nsources + 1
                            nsource_str = 'Source {0:4}'.format(nsources)
                            Z_min_tavg = vent_h + hbe_min_tavg / 2
                            Z_min_tavg_str = '{0:.4E}'.format(Z_min_tavg)
                            Z_tavg = vent_h + hbe_tavg / 2
                            Z_tavg_str = '{0:.4E}'.format(Z_tavg)
                            Z_max_tavg = vent_h + hbe_max_tavg / 2
                            Z_max_tavg_str = '{0:.4E}'.format(Z_max_tavg)
                            Qfmer_NAME_min_tavg = Qfmer_min_tavg * 1000 * 3600
                            Qfmer_NAME_min_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_min_tavg)
                            Qfmer_NAME_tavg = Qfmer_tavg * 1000 * 3600
                            Qfmer_NAME_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_tavg)
                            Qfmer_NAME_max_tavg = Qfmer_max_tavg * 1000 * 3600
                            Qfmer_NAME_max_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_max_tavg)
                            Stop_Time = TimeNOW.strftime("%d/%m/%Y %H:%M")
                            Start_Time = (TimeNOW - datetime.timedelta(seconds=timin_sec_cum)).strftime(
                                "%d/%m/%Y %H:%M")
                            FILE15_writer.writerow([nsource_str,Z_tavg_str,hbe_tavg_str,Qfmer_NAME_tavg_str,Start_Time,Stop_Time])
                            FILE16_writer.writerow([nsource_str,Z_max_tavg_str,hbe_max_tavg_str,Qfmer_NAME_max_tavg_str,Start_Time,Stop_Time])
                            FILE17_writer.writerow([nsource_str,Z_min_tavg_str,hbe_min_tavg_str,Qfmer_NAME_min_tavg_str,Start_Time,Stop_Time])
                        hbe_min_sum = 0
                        hbe_sum = 0
                        hbe_max_sum = 0
                        Qfmer_min_sum = 0
                        Qfmer_sum = 0
                        Qfmer_max_sum = 0
                        timin_sec_cum = 0
                elif PM_TAV == 2:
                    if run > 1 and timin_sec_cum % 1800 < 299:
                        hbe_min_tavg = hbe_min_sum / timin_sec_cum
                        hbe_tavg = hbe_sum / timin_sec_cum
                        hbe_max_tavg = hbe_max_sum / timin_sec_cum
                        hbe_min_tavg_str = '{0:.4E}'.format(hbe_min_tavg)
                        hbe_tavg_str = '{0:.4E}'.format(hbe_tavg)
                        hbe_max_tavg_str = '{0:.4E}'.format(hbe_max_tavg)
                        Qfmer_min_tavg = Qfmer_min_sum / timin_sec_cum
                        Qfmer_tavg = Qfmer_sum / timin_sec_cum
                        Qfmer_max_tavg = Qfmer_max_sum / timin_sec_cum
                        FILE13.write(str(TimeNOW) + "\t" + str(timin) + "\t" + str(hbe_min_tavg) + "\t" + str(hbe_tavg) +
                                     "\t" + str(hbe_max_tavg) + "\n")
                        FILE14.write(str(TimeNOW) + "\t" + str(timin) + "\t" + str(Qfmer_min_tavg) + "\t" + str(Qfmer_tavg) +
                                     "\t" + str(Qfmer_max_tavg) + "\n")
                        if NAME_out_on == 1:
                            nsources = nsources + 1
                            nsource_str = 'Source {0:4}'.format(nsources)
                            Z_min_tavg = vent_h + hbe_min_tavg / 2
                            Z_min_tavg_str = '{0:.4E}'.format(Z_min_tavg)
                            Z_tavg = vent_h + hbe_tavg / 2
                            Z_tavg_str = '{0:.4E}'.format(Z_tavg)
                            Z_max_tavg = vent_h + hbe_max_tavg / 2
                            Z_max_tavg_str = '{0:.4E}'.format(Z_max_tavg)
                            Qfmer_NAME_min_tavg = Qfmer_min_tavg * 1000 * 3600
                            Qfmer_NAME_min_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_min_tavg)
                            Qfmer_NAME_tavg = Qfmer_tavg * 1000 * 3600
                            Qfmer_NAME_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_tavg)
                            Qfmer_NAME_max_tavg = Qfmer_max_tavg * 1000 * 3600
                            Qfmer_NAME_max_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_max_tavg)
                            Stop_Time = TimeNOW.strftime("%d/%m/%Y %H:%M")
                            Start_Time = (TimeNOW - datetime.timedelta(seconds=timin_sec_cum)).strftime(
                                "%d/%m/%Y %H:%M")
                            FILE15_writer.writerow([nsource_str,Z_tavg_str,hbe_tavg_str,Qfmer_NAME_tavg_str,Start_Time,Stop_Time])
                            FILE16_writer.writerow([nsource_str,Z_max_tavg_str,hbe_max_tavg_str,Qfmer_NAME_max_tavg_str,Start_Time,Stop_Time])
                            FILE17_writer.writerow([nsource_str,Z_min_tavg_str,hbe_min_tavg_str,Qfmer_NAME_min_tavg_str,Start_Time,Stop_Time])
                        hbe_min_sum = 0
                        hbe_sum = 0
                        hbe_max_sum = 0
                        Qfmer_min_sum = 0
                        Qfmer_sum = 0
                        Qfmer_max_sum = 0
                        timin_sec_cum = 0
                elif PM_TAV == 3:
                    if run > 1 and timin_sec_cum % 3600 < 299:
                        hbe_min_tavg = hbe_min_sum / timin_sec_cum
                        hbe_tavg = hbe_sum / timin_sec_cum
                        hbe_max_tavg = hbe_max_sum / timin_sec_cum
                        hbe_min_tavg_str = '{0:.4E}'.format(hbe_min_tavg)
                        hbe_tavg_str = '{0:.4E}'.format(hbe_tavg)
                        hbe_max_tavg_str = '{0:.4E}'.format(hbe_max_tavg)
                        Qfmer_min_tavg = Qfmer_min_sum / timin_sec_cum
                        Qfmer_tavg = Qfmer_sum / timin_sec_cum
                        Qfmer_max_tavg = Qfmer_max_sum / timin_sec_cum
                        FILE13.write(str(TimeNOW) + "\t" + str(timin) + "\t" + str(hbe_min_tavg) + "\t" + str(hbe_tavg) +
                                     "\t" + str(hbe_max_tavg) + "\n")
                        FILE14.write(str(TimeNOW) + "\t" + str(timin) + "\t" + str(Qfmer_min_tavg) + "\t" + str(Qfmer_tavg) +
                                     "\t" + str(Qfmer_max_tavg) + "\n")
                        if NAME_out_on == 1:
                            nsources = nsources + 1
                            nsource_str = 'Source {0:4}'.format(nsources)
                            Z_min_tavg = vent_h + hbe_min_tavg / 2
                            Z_min_tavg_str = '{0:.4E}'.format(Z_min_tavg)
                            Z_tavg = vent_h + hbe_tavg / 2
                            Z_tavg_str = '{0:.4E}'.format(Z_tavg)
                            Z_max_tavg = vent_h + hbe_max_tavg / 2
                            Z_max_tavg_str = '{0:.4E}'.format(Z_max_tavg)
                            Qfmer_NAME_min_tavg = Qfmer_min_tavg * 1000 * 3600
                            Qfmer_NAME_min_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_min_tavg)
                            Qfmer_NAME_tavg = Qfmer_tavg * 1000 * 3600
                            Qfmer_NAME_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_tavg)
                            Qfmer_NAME_max_tavg = Qfmer_max_tavg * 1000 * 3600
                            Qfmer_NAME_max_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_max_tavg)
                            Stop_Time = TimeNOW.strftime("%d/%m/%Y %H:%M")
                            Start_Time = (TimeNOW - datetime.timedelta(seconds=timin_sec_cum)).strftime(
                                "%d/%m/%Y %H:%M")
                            FILE15_writer.writerow([nsource_str,Z_tavg_str,hbe_tavg_str,Qfmer_NAME_tavg_str,Start_Time,Stop_Time])
                            FILE16_writer.writerow([nsource_str,Z_max_tavg_str,hbe_max_tavg_str,Qfmer_NAME_max_tavg_str,Start_Time,Stop_Time])
                            FILE17_writer.writerow([nsource_str,Z_min_tavg_str,hbe_min_tavg_str,Qfmer_NAME_min_tavg_str,Start_Time,Stop_Time])
                        hbe_min_sum = 0
                        hbe_sum = 0
                        hbe_max_sum = 0
                        Qfmer_min_sum = 0
                        Qfmer_sum = 0
                        Qfmer_max_sum = 0
                        timin_sec_cum = 0
                elif PM_TAV == 4:
                    if run > 1 and timin_sec_cum % 10800 < 299:
                        hbe_min_tavg = hbe_min_sum / timin_sec_cum
                        hbe_tavg = hbe_sum / timin_sec_cum
                        hbe_max_tavg = hbe_max_sum / timin_sec_cum
                        hbe_min_tavg_str = '{0:.4E}'.format(hbe_min_tavg)
                        hbe_tavg_str = '{0:.4E}'.format(hbe_tavg)
                        hbe_max_tavg_str = '{0:.4E}'.format(hbe_max_tavg)
                        Qfmer_min_tavg = Qfmer_min_sum / timin_sec_cum
                        Qfmer_tavg = Qfmer_sum / timin_sec_cum
                        Qfmer_max_tavg = Qfmer_max_sum / timin_sec_cum
                        FILE13.write(str(TimeNOW) + "\t" + str(timin) + "\t" + str(hbe_min_tavg) + "\t" + str(hbe_tavg) +
                                     "\t" + str(hbe_max_tavg) + "\n")
                        FILE14.write(str(TimeNOW) + "\t" + str(timin) + "\t" + str(Qfmer_min_tavg) + "\t" + str(Qfmer_tavg) +
                                     "\t" + str(Qfmer_max_tavg) + "\n")
                        if NAME_out_on == 1:
                            nsources = nsources + 1
                            nsource_str = 'Source {0:4}'.format(nsources)
                            Z_min_tavg = vent_h + hbe_min_tavg / 2
                            Z_min_tavg_str = '{0:.4E}'.format(Z_min_tavg)
                            Z_tavg = vent_h + hbe_tavg / 2
                            Z_tavg_str = '{0:.4E}'.format(Z_tavg)
                            Z_max_tavg = vent_h + hbe_max_tavg / 2
                            Z_max_tavg_str = '{0:.4E}'.format(Z_max_tavg)
                            Qfmer_NAME_min_tavg = Qfmer_min_tavg * 1000 * 3600
                            Qfmer_NAME_min_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_min_tavg)
                            Qfmer_NAME_tavg = Qfmer_tavg * 1000 * 3600
                            Qfmer_NAME_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_tavg)
                            Qfmer_NAME_max_tavg = Qfmer_max_tavg * 1000 * 3600
                            Qfmer_NAME_max_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_max_tavg)
                            Stop_Time = TimeNOW.strftime("%d/%m/%Y %H:%M")
                            Start_Time = (TimeNOW - datetime.timedelta(seconds=timin_sec_cum)).strftime(
                                "%d/%m/%Y %H:%M")
                            FILE15_writer.writerow([nsource_str,Z_tavg_str,hbe_tavg_str,Qfmer_NAME_tavg_str,Start_Time,Stop_Time])
                            FILE16_writer.writerow([nsource_str,Z_max_tavg_str,hbe_max_tavg_str,Qfmer_NAME_max_tavg_str,Start_Time,Stop_Time])
                            FILE17_writer.writerow([nsource_str,Z_min_tavg_str,hbe_min_tavg_str,Qfmer_NAME_min_tavg_str,Start_Time,Stop_Time])
                        hbe_min_sum = 0
                        hbe_sum = 0
                        hbe_max_sum = 0
                        Qfmer_min_sum = 0
                        Qfmer_sum = 0
                        Qfmer_max_sum = 0
                        timin_sec_cum = 0
                elif PM_TAV == 5:
                    if run > 1 and timin_sec_cum % 21600 < 299:
                        hbe_min_tavg = hbe_min_sum / timin_sec_cum
                        hbe_tavg = hbe_sum / timin_sec_cum
                        hbe_max_tavg = hbe_max_sum / timin_sec_cum
                        hbe_min_tavg_str = '{0:.4E}'.format(hbe_min_tavg)
                        hbe_tavg_str = '{0:.4E}'.format(hbe_tavg)
                        hbe_max_tavg_str = '{0:.4E}'.format(hbe_max_tavg)
                        Qfmer_min_tavg = Qfmer_min_sum / timin_sec_cum
                        Qfmer_tavg = Qfmer_sum / timin_sec_cum
                        Qfmer_max_tavg = Qfmer_max_sum / timin_sec_cum
                        FILE13.write(str(TimeNOW) + "\t" + str(timin) + "\t" + str(hbe_min_tavg) + "\t" + str(hbe_tavg) +
                                     "\t" + str(hbe_max_tavg) + "\n")
                        FILE14.write(str(TimeNOW) + "\t" + str(timin) + "\t" + str(Qfmer_min_tavg) + "\t" + str(Qfmer_tavg) +
                                     "\t" + str(Qfmer_max_tavg) + "\n")
                        if NAME_out_on == 1:
                            nsources = nsources + 1
                            nsource_str = 'Source {0:4}'.format(nsources)
                            Z_min_tavg = vent_h + hbe_min_tavg / 2
                            Z_min_tavg_str = '{0:.4E}'.format(Z_min_tavg)
                            Z_tavg = vent_h + hbe_tavg / 2
                            Z_tavg_str = '{0:.4E}'.format(Z_tavg)
                            Z_max_tavg = vent_h + hbe_max_tavg / 2
                            Z_max_tavg_str = '{0:.4E}'.format(Z_max_tavg)
                            Qfmer_NAME_min_tavg = Qfmer_min_tavg * 1000 * 3600
                            Qfmer_NAME_min_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_min_tavg)
                            Qfmer_NAME_tavg = Qfmer_tavg * 1000 * 3600
                            Qfmer_NAME_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_tavg)
                            Qfmer_NAME_max_tavg = Qfmer_max_tavg * 1000 * 3600
                            Qfmer_NAME_max_tavg_str = 'VOLCANIC_ASH {0:.4E} g/hr'.format(Qfmer_NAME_max_tavg)
                            Stop_Time = TimeNOW.strftime("%d/%m/%Y %H:%M")
                            Start_Time = (TimeNOW - datetime.timedelta(seconds=timin_sec_cum)).strftime(
                                "%d/%m/%Y %H:%M")
                            FILE15_writer.writerow([nsource_str,Z_tavg_str,hbe_tavg_str,Qfmer_NAME_tavg_str,Start_Time,Stop_Time])
                            FILE16_writer.writerow([nsource_str,Z_max_tavg_str,hbe_max_tavg_str,Qfmer_NAME_max_tavg_str,Start_Time,Stop_Time])
                            FILE17_writer.writerow([nsource_str,Z_min_tavg_str,hbe_min_tavg_str,Qfmer_NAME_min_tavg_str,Start_Time,Stop_Time])
                        hbe_min_sum = 0
                        hbe_sum = 0
                        hbe_max_sum = 0
                        Qfmer_min_sum = 0
                        Qfmer_sum = 0
                        Qfmer_max_sum = 0
                        timin_sec_cum = 0
                else:
                    FILE13.close()
                    FILE14.close()
                FILE13.close()
                FILE14.close()
                if NAME_out_on == 1:
                    FILE15.close()
                    FILE16.close()
                    FILE17.close()

        """
        _mer_log.txt file contains overview of all parameter used for MER plus results:
        
        0 time since eruption start
        1 N (number of plume height sources used)
        2 hbe (best estimate plume height)
        3 MERMIN_hmin
        4 MERMAX_hmin
        5 MERWE
        6 MERMAX_PLUS 
        7 Max(MER(hmax))
        8 w.fc. ww
        9 w.fc. sp
        10 w.fc. ma
        11 w.fc. mtg
        12 w.fc. db
        13 MERww
        14 MERsp
        15 MERma
        16 MERmtg
        17 MERdb
        18 CMER (RMER in case that Woodh switched off!)
        19 MERavg
        20 MERwood_min
        21 MERwood_avg
        22 MERwood_max
        23 OBS_on (non-auto data switch)
        24 theta_a0 (ambient temp at vent)
        25 P_0 (ambient pressure at vent)
        26 theta_0 (magma temperature)
        27 rho_dre
        28 alpha (radial entr coeff)
        29 beta (wind entr coeff)
        30 wtf_wil
        31 wtf_spa
        32 wtf_mas
        33 wtf_mtg
        34 wtf_deg
        35 H1 (Height tropopause)
        36 H2 (Height stratosphere)
        37 tempGrad_1 (temp grad in troposphere)
        38 tempGrad_2 (temperature gradient between troposphere and stratosphere)
        39 tempGrad_3 (temp grad in stratosphere)
        40 Vmax (windspeed in tropopause)
        41 ki
        42 qfak_ISKEF
        43 qfak_ISEGS
        44 qfak_ISX1
        45 qfak_ISX2
        46 qfak_GFZ1
        47 qfak_GFZ2
        48 qfak_GFZ3
        49 unc_ISKEF
        50 unc_ISEGS
        51 unc_ISX1
        52 unc_ISX2
        53 vent_h
        54 ISKEF_on
        55 ISEGS_on
        56 ISX1_on
        57 ISX2_on
        58 GFZ1_on
        59 GFZ2_on
        60 GFZ3_on
        61 analysis
        62 timebase (time base set in config file)
        63 oo_exp (switch experimental MER systems)
        64 oo_con (switch conventional models)
        65 wtf_exp 
        66 wtf_con 
        67 Qupper (=Qmaxhplus)
        68 wtf_manual
        69 min_manMER 
        70 max_manMER 
        71 oo_wood (switch Woodhouse)
        72 oo_5MER (switch 5 internal models)
        73 wtf_wood
        74 wtf_5MER
        75 oo_isound
        76 wtf_isound
        77 oo_esens
        78 wtf_esens
        79 oo_pulsan
        80 wtf_pulsan
        81 oo_scatter
        82 wtf_scatter
        83 cal_ISKEF_a
        84 cal_ISKEF_b
        85 cal_ISEGS_a
        86 cal_ISEGS_b
        87 cal_ISX1_a
        88 cal_ISX1_b
        89 cal_ISX2_a
        90 cal_ISX2_b
        91 ISKEFm_on (switch manual input from ISKEF radar source)
        92 ISEGSm_on (switch manual input from ISEGS radar source)
        93 ISX1m_on (switch manual input from ISX1 radar source)
        94 ISX2m_on (switch manual input from ISX2 radar source)
        95 hbe_min
        96 hbe_max
        97 MERmaxNowiHmin (max of non-wind affected models fed by hmin)  
        98 hbe_min15    
        99 hbe_15    
        100 hbe_max15    
        101 hbe_min30    
        102 hbe_30    
        103 hbe_max30    
        104 hbe_min1h    
        105 hbe_1h    
        106 hbe_max1h    
        107 hbe_min3h    
        108 hbe_3h    
        109 hbe_max3h    
        110 Qlower  
        111 Q_exp_min
        112 Q_exp wavg  
        113 Q_exp_max
        114 Q_man_min
        115 Q_man_wavg
        116 Q_man_max
        117 Qf_abs. min
        118 Qf_abs. max
        119 QFMER_min
        120 QFMER
        121 QFMER_max 
        122 PlumeRadiusMin  
        123 PlumeRadiusMax
        124 empty slot (-99) 
        125 empty slot (-99)
        126 tiba (time base for calculation)
        127 time of eruption start 
        128 Cband3_on
        129 Cband4_on
        130 Cband5_on
        131 Cband6_on
        132 Xband3_on
        133 Xband4_on
        134 Xband5_on
        135 Xband6_on
        136 Cam4_on)
        137 Cam5_on
        138 Cam6_on
        139 Cband3m_on
        140 Cband4m_on
        141 Cband5m_on
        142 Cband6m_on
        143 Xband3m_on
        144 Xband4m_on
        145 Xband5m_on
        146 Xband6m_on
        147 cal_Cband3a
        148 cal_Cband3b
        149 cal_Cband4a
        150 cal_Cband4b
        151 cal_Cband5a
        152 cal_Cband5b
        153 cal_Cband6a
        154 cal_Cband6b
        155 cal_Xband3a
        156 cal_Xband3b
        157 cal_Xband4a
        158 cal_Xband4b
        159 cal_Xband5a
        160 cal_Xband5b
        161 cal_Xband6a
        162 cal_Xband6b
        163 unc_Cband3
        164 unc_Cband4
        165 unc_Cband5
        166 unc_Cband6
        167 unc_Xband3
        168 unc_Xband4
        169 unc_Xband5
        170 unc_Xband6
        171 qfak_Cband3
        172 qfak_Cband4
        173 qfak_Cband5
        174 qfak_Cband6
        175 qfak_Xband3
        176 qfak_Xband4
        177 qfak_Xband5
        178 qfak_Xband6
        179 qfak_Cam4
        180 qfak_Cam5
        181 qfak_Cam6
        182 wtf_wood0d
        183 MERwood0d
        
        """
        #STARTING FROM HERE: FMER SECTION
        # EXPERIMENTAL MER
        
        Qexp_stack3h = [[0,0,0,0,0,0,0]]
        Qexp_stack1h = [[0,0,0,0,0,0,0]]
        Qexp_stack30 = [[0,0,0,0,0,0,0]]
        Qexp_stack15 = [[0,0,0,0,0,0,0]]
        
        #Qexp stacks contain:
        #timediff,Qmin, Q, Qmax, wtf, src, flag
        
        def Qstacksort(timdiff,emer_min, emer_max,wf,exp_src,exp_onoff):
            """sorts data according to up-to-dateness"""
            emer = (emer_min+emer_max)/2
            
            if timdiff<181:
                Qexp_stack3h.append([timdiff, emer_min,emer,emer_max,wf,exp_src,exp_onoff])
                
            if timdiff<61:
                Qexp_stack1h.append([timdiff, emer_min,emer,emer_max,wf,exp_src,exp_onoff])
                
            if timdiff<31:
                Qexp_stack30.append([timdiff, emer_min,emer,emer_max,wf,exp_src,exp_onoff])
                
            if timdiff<16:
                Qexp_stack15.append([timdiff, emer_min,emer,emer_max,wf,exp_src,exp_onoff])
                
            else:
                print("") #...data set older than 180 minutes...
            logger7.debug("*Stacked MER data >> source: " + str(exp_src)+"\t"+"time difference: "+timdiff+"\t"+"exp.Qmin: "+emer_min+"\t"+"exp.Q: "+emer+"\t"+"exp.Qmin: "+emer_max)

        def saveEMER(tiba_in):
            global Qcode
            qfrt = open(out_txt+"_EMER_LOG.txt","a",encoding="utf-8", errors="surrogateescape")
            qfrt.write(str(timin)+"\t"+str(wemer_min)+"\t"+str(wemer_avg)+"\t"+\
        str(wemer_max)+"\t"+str(Qcode)+"\t"+str(tiba_in)+"\n")
            qfrt.close()
            return(True)
        
        def ExpMER_import(importfile,exp_src,wf_exp):
            """importing routine for exp. MER data"""
            global wf
            expMERmin,expMERmax,expMER_flag = np.loadtxt(importfile+".txt",\
        usecols=(1,2,3), unpack=True, delimiter='\t')  
            rlines = []
            with open(importfile+".txt", "r",encoding="utf-8", errors="surrogateescape") as fp:
                for line in fp:
                    rlines.append(line[:19])
            fp.close() 
          
            l = len(rlines)
            if l ==1:
            
                if rlines[-1] == "":
                    for x in range (0,l-1):
                        indate = rlines[x]
                        TimeE = datetime.datetime.strptime(indate, "%Y-%m-%d %H:%M:%S")
                        time_diffe = TimeNOW - TimeE
                        time_diffe_sec = time_diffe.total_seconds()
                        if time_diffe_sec < 0:
                            continue
                        time_diffe_min = time_diffe_sec/60
                        if expMER_flag == 0:
                            print()
                        else:
                            if expMERmin==0:
                                print()
                            else:
                                Qstacksort(time_diffe_min,expMERmin,expMERmax,wf,exp_src,expMER_flag)
                        
                else:
                     for x in range (0,l):
                         indate = rlines[x]
                         TimeE = datetime.datetime.strptime(indate, "%Y-%m-%d %H:%M:%S")
                         time_diffe = TimeNOW - TimeE
                         time_diffe_sec = time_diffe.total_seconds()
                         if time_diffe_sec < 0:
                             continue
                         time_diffe_min = time_diffe_sec/60
                         if expMER_flag == 0:
                            print()
                         else:
                            if expMERmin==0:
                                print()
                            else:
                                Qstacksort(time_diffe_min,expMERmin,expMERmax,wf,exp_src,expMER_flag)
            else:
                        
                if rlines[-1] == "":
                    for x in range (0,l-1):
                        indate = rlines[x]
                        TimeE = datetime.datetime.strptime(indate, "%Y-%m-%d %H:%M:%S")
                        time_diffe = TimeNOW - TimeE
                        time_diffe_sec = time_diffe.total_seconds()
                        if time_diffe_sec < 0:
                            continue
                        time_diffe_min = time_diffe_sec/60
                        if expMER_flag == 0:
                            print()
                        else:
                            if expMERmin==0:
                                print()
                            else:
                                Qstacksort(time_diffe_min,expMERmin,expMERmax,wf,exp_src,expMER_flag)
                        
                else:
                     for x in range (0,l):
                         indate = rlines[x]
                         TimeE = datetime.datetime.strptime(indate, "%Y-%m-%d %H:%M:%S")
                         time_diffe = TimeNOW - TimeE
                         time_diffe_sec = time_diffe.total_seconds()
                         if time_diffe_sec < 0:
                             continue
                         time_diffe_min = time_diffe_sec/60
                         if expMER_flag == 0:
                            print()
                         else:
                            if expMERmin==0:
                                print()
                            else:
                                Qstacksort(time_diffe_min,expMERmin,expMERmax,wf,exp_src,expMER_flag)
                return(True)
        #experimental systems (source IDs): 100 infrasound, 200 E-sensors, 300 pulse analysis, 400 microwave scattering
        try:

            if oo_isound ==1:
                logger7.info("checking ............infrasound")
                Isound = open("isound_out.txt", "r",encoding="utf-8", errors="surrogateescape")
                Isound.close()
                ExpMER_import("isound_out",100,wtf_isound)
            else:
                logger7.info("---infrasound is switched off by operator!---")
        except EnvironmentError:
            logger7.warning("No infrasound data found - check connection!")
        
        
        try:
        
            if oo_esens ==1:
                Esens = open("esens_out.txt", "r",encoding="utf-8", errors="surrogateescape")
                Esens.close()
                logger7.info("checking ............E-sensors")
                ExpMER_import("esens_out",200,wtf_esens)
            else:
                logger7.info("---E-sensors switched off by operator!---")
        except EnvironmentError:
            logger7.warning("No E-sensor data found - check connection!")
        
        
        try:
        
            if oo_pulsan ==1:
                Pulsan = open("pulse_out.txt", "r",encoding="utf-8", errors="surrogateescape")
                Pulsan.close()
                logger7.info("checking ............pulse analysis")
                ExpMER_import("pulse_out",300,wtf_pulsan)
            else:
                logger7.info("---pulse analysis switched off by operator!---")
        except EnvironmentError:
            logger7.warning("No pulse analysis data found - check connection!")
        
        try:
        
            if oo_scatter ==1:
                Scatter = open("mwave_out.txt", "r",encoding="utf-8", errors="surrogateescape")
                Scatter.close()
                logger7.info("checking ............microwave scatter analysis")
                ExpMER_import("mwave_out",400,wtf_scatter)
            else:
                logger7.info("---microwave scatter analysis switched off by operator!---")
        except EnvironmentError:
            logger7.warning("No microwave scatter analysis data found - check connection!")
        
        
        eN3h=0
        for x in range(0,len(Qexp_stack3h)):
            eN3h = int (eN3h + Qexp_stack3h[x][-1])
        
        eN1h=0
        for x in range(0,len(Qexp_stack1h)):
            eN1h = int(eN1h + Qexp_stack1h[x][-1])
            
        eN30min=0
        for x in range(0,len(Qexp_stack30)):
            eN30min = int(eN30min + Qexp_stack30[x][-1])
        
        eN15min=0
        for x in range(0,len(Qexp_stack15)):
            eN15min = int(eN15min + Qexp_stack15[x][-1])
        
        logger7.debug("number of experimental MER data considered by system:")
        logger7.debug("within last 180 min: " +str(eN3h))
        logger7.debug("within last 60 min: " +str(eN1h))
        logger7.debug("within last 30 min: " +str(eN30min))
        logger7.debug("within last 15 min: " +str(eN15min))
        logger7.debug("-------------------------------------")
        logger7.debug("-------------------------------------")
        logger7.debug("")

        def EMER_best(N,stack):
            """calculating the key figures for exp. MER"""
            global wemer_min,wemer_avg,wemer_max,EQcode
            if N == 0:
                logger7.info("No exp. MER height data - no calculation possible!")
                logger7.info("**   step skipped   **")
                EQcode = 0
                wemer_min = 0
                wemer_avg = 0
                wemer_max = 0
            else:
                EQcode = 1
                wb = 0.0
                wc = 1.0
                wd = 0.0
                we = 0.0
                for gu in range (0,int(N)):
                    wb = stack[gu][4]*stack[gu][2] + wb
                    wc = stack[gu][4] + wc
                    wd = stack[gu][4]*stack[gu][1] + wd
                    we = stack[gu][4]*stack[gu][3] + we
                    
                wemer_min = wd/wc
                wemer_avg = wb/wc
                wemer_max = we/wc
        
        if oo_exp==0:
            logger7.info("experimental MER systems switched OFF!")
        else:
            if TIMEBASE == 15:
                EMER_best(eN15min,Qexp_stack15)
                if EQcode ==0:
                    logger7.info("\n\n!! no new exp. MER data within selected time frame !!\n\
                ....exp. MER not considered for further computation!\n\n")
                    #winsound.Beep(Freq,Dur2)
                else:
                    saveEMER(TIMEBASE)
            elif TIMEBASE == 30:
                EMER_best(eN30min,Qexp_stack30)
                if EQcode ==0:
                    logger7.info("\n\n!! no new exp. MER data within selected time frame !!\n\
                ....exp. MER not considered for further computation!\n\n")
                    #winsound.Beep(Freq,Dur2)
                else:
                    saveEMER(TIMEBASE)
            elif TIMEBASE == 60:
                EMER_best(eN1h,Qexp_stack1h)
                if EQcode ==0:
                    logger7.info("\n\n!! no new exp. MER data within selected time frame !!\n\
                ....exp. MER not considered for further computation!\n\n")
                    #winsound.Beep(Freq,Dur2)
                else:
                    saveEMER(TIMEBASE)
            else:
                EMER_best(eN3h,Qexp_stack3h)
                if EQcode ==0:
                    logger7.info("\n\n!! no new exp. MER data within selected time frame !!\n\
                ....exp. MER not considered for further computation!\n\n")
                    #winsound.Beep(Freq,Dur2)
                else:
                    saveEMER(180)
        
        # MANUAL MER
        
        
        Qman_stack3h = [[0,0,0,0,0,0,0]]
        Qman_stack1h = [[0,0,0,0,0,0,0]]
        Qman_stack30 = [[0,0,0,0,0,0,0]]
        Qman_stack15 = [[0,0,0,0,0,0,0]]
        
        def Qman_stacksort(timdiff,mmer_min, mmer_max,wf,man_src,man_onoff):
            """sorts data according to up-to-dateness"""
            mmer = (mmer_min+mmer_max)/2
            
            if timdiff<181:
                Qman_stack3h.append([timdiff, mmer_min,mmer,mmer_max,wf,man_src,man_onoff])
                
            if timdiff<61:
                Qman_stack1h.append([timdiff, mmer_min,mmer,mmer_max,wf,man_src,man_onoff])
                
            if timdiff<31:
                Qman_stack30.append([timdiff, mmer_min,mmer,mmer_max,wf,man_src,man_onoff])
                
            if timdiff<16:
                Qman_stack15.append([timdiff, mmer_min,mmer,mmer_max,wf,man_src,man_onoff])
                
            else:
                print("") #...data set older than 180 minutes...

        def manMER_import():
            """imports all manually added MER data"""
#            oo_manMER,wf_manMER,manMER_min,manMER_max = np.loadtxt("fix_MERin.txt",\
#        usecols=(1,2,3,4), unpack=True, delimiter='\t')
#            rlines = []
            with open("fix_MERin.txt", "r",encoding="utf-8", errors="surrogateescape") as fp:
                first_line = fp.readline()
                time_string = first_line[:19]
#                for line in fp:
#                    rlines.append(line[:19])
            fp.close()
            splits = first_line.split("\t")
            oo_manMER = float(splits[1])
            wf_manMER = float(splits[2])
            manMER_min = float(splits[3])
            manMER_max = float(splits[4])
            #oo_manMER, wf_manMER, manMER_min, manMER_max = np.loadtxt(first_line,usecols=(1, 2, 3, 4), unpack=True, delimiter='\t')
            indate = time_string
            # TimeE = datetime.datetime.strptime(indate, "%d-%m-%Y %H:%M:%S")
            TimeE = datetime.datetime.strptime(indate, "%Y-%m-%d %H:%M:%S")
            time_diffe = TimeNOW - TimeE
            time_diffe_sec = time_diffe.total_seconds()
            if time_diffe_sec < 0:
                oo_manMER = 0
            time_diffe_min = time_diffe_sec / 60
            if oo_manMER == 0:
                print()
            else:
                if manMER_min == 0:
                    print()
                else:
                    Qman_stacksort(time_diffe_min, manMER_min, manMER_max, wf_manMER, 900, oo_manMER)

        try:
            Pulsan = open("fix_MERin.txt", "r",encoding="utf-8", errors="surrogateescape")
            Pulsan.close()
            logger7.info("checking ............manual MER data")
            manMER_import()
        except EnvironmentError:
            logger7.info("No manually added MER data found.")
        
        mN3h=0
        for x in range(0,len(Qman_stack3h)):
            mN3h = int (mN3h + Qman_stack3h[x][-1])
        
        mN1h=0
        for x in range(0,len(Qman_stack1h)):
            mN1h = int(mN1h + Qman_stack1h[x][-1])
            
        mN30min=0
        for x in range(0,len(Qman_stack30)):
            mN30min = int(mN30min + Qman_stack30[x][-1])
        
        mN15min=0
        for x in range(0,len(Qman_stack15)):
            mN15min = int(mN15min + Qman_stack15[x][-1])
        
        logger7.debug("number of manually added MER data considered by system:")
        logger7.debug("within last 180 min: " +str(mN3h))
        logger7.debug("within last 60 min: " +str(mN1h))
        logger7.debug("within last 30 min: " +str(mN30min))
        logger7.debug("within last 15 min: " +str(mN15min))
        logger7.debug("-------------------------------------")
        logger7.debug("-------------------------------------")
        logger7.debug("")
        
        
        def MMER_best(N,stack):
            """calculating the key figures for manually added MER"""
            global mwmer_min,mwmer_avg,mwmer_max, MQcode,a_man
            if N == 0:
                logger7.info("No manually added data - no calculation possible!")
                MQcode = 0
                mwmer_min = 0
                mwmer_avg = 0
                mwmer_max = 0
                a_man = 0
            else:
                MQcode = 1
                wb = 0.0
                wc = 1.0
                wd = 0.0
                we = 0.0
                for gu in range (0,int(N)):
                    wb = stack[gu][4]*stack[gu][2] + wb
                    wc = stack[gu][4] + wc
                    wd = stack[gu][4]*stack[gu][1] + wd
                    we = stack[gu][4]*stack[gu][3] + we
                    
                mwmer_min = wd/wc
                mwmer_avg = wb/wc
                mwmer_max = we/wc
                a_man = wc/N
        

        if TIMEBASE == 15:
            MMER_best(mN15min,Qman_stack15)
    
        elif TIMEBASE == 30:
            MMER_best(mN30min,Qman_stack30)
    
        elif TIMEBASE == 60:
            MMER_best(mN1h,Qman_stack1h)
    
        else:
            MMER_best(mN3h,Qman_stack3h)
        
        def FMERstat(mer_stat):
            """ computes the FMER key figures"""
            global skipFMER, Qf_absmin, Qf_absmax, Qfmer_min,Qfmer_max,Qfmer,cur_Qlower,cur_MERwood_avg
            cur_MERwood_avg = float(Mwood[1])
# These lines commented since Deg & Bon model is always used now; also, included Wood0d in the calculation
            # if mer_stat[6] == 0:
            #     if float(Mwood[1]) == 0:
            #         cur_Qlower = min (mer_stat[1],mer_stat[9])
            #     else:
            #         cur_Qlower = min (mer_stat[1],mer_stat[9],float(Mwood[1]))
            # else:
            #     if cur_MERwood_avg == 0:
            #         cur_Qlower = min (mer_stat[1],mer_stat[9],mer_stat[6])
            #     else:
            #         cur_Qlower = min (mer_stat[1],mer_stat[9],float(Mwood[1]),mer_stat[6])

            cur_Qlower = mer_stat[1]

            if ckcode ==0 or oo_con==0:
                if MQcode == 0:
                    if EQcode == 0 or oo_exp ==0:
                        logger7.debug("***No FMER stats possible!***")
                        skipFMER = 1 #all further FMER and CMER processes have to be skipped
                    else:
                        #only experimental MER!
                        Qf_absmin = wemer_min
                        Qf_absmax = wemer_max
                        Qfmer_min = wemer_min
                        Qfmer_max = wemer_max
                        Qfmer = wemer_avg
                        skipFMER = 121
                else:
                    if EQcode == 0 or oo_exp==0:
                        #only manual MER!
                        Qf_absmin = mwmer_min
                        Qf_absmax = mwmer_max
                        Qfmer_min = mwmer_min
                        Qfmer_max = mwmer_max
                        Qfmer = mwmer_avg
                        skipFMER = 112 
                    else:
                        #only experimental and manual MER!
                        Qf_absmin = min(wemer_min,mwmer_min)
                        Qf_absmax = max(wemer_max,mwmer_max)
                        Qfmer_min = min(wemer_min,mwmer_min)
                        Qfmer_max = max(wemer_max,mwmer_max)
                        Qfmer = (wtf_exp*wemer_avg + a_man*mwmer_avg)/(wtf_exp+a_man)
                        skipFMER = 122 
            else:
                if MQcode == 0:
                    if EQcode == 0 or oo_exp==0:
                        #identical to CMER stats
                        Qf_absmin = mer_stat[0]
                        Qf_absmax = mer_stat[4]
                        Qfmer_min = cur_Qlower
                        Qfmer_max = mer_stat[3]
                        Qfmer = mer_stat[7]
                        skipFMER = 211 
                    else:
                        #only experimental MER and CMER!
                        Qmlower = cur_Qlower                
                        Qf_absmin = min(wemer_min,mer_stat[0])
                        Qf_absmax = max(wemer_max,mer_stat[4])
                        Qfmer_min = (wtf_exp*wemer_min + wtf_con*Qmlower)/(wtf_exp+wtf_con)
                        Qfmer_max = (wtf_exp*wemer_max + wtf_con* mer_stat[3])/(wtf_exp+wtf_con)
                        Qfmer = (wtf_exp*wemer_avg + wtf_con*mer_stat[7])/(wtf_exp+wtf_con)
                        skipFMER = 221
                else:
                    if EQcode == 0 or oo_exp==0:
                        #only manual MER and CMER!
                        Qmlower = cur_Qlower               
                        Qf_absmin = min(mwmer_min,mer_stat[0])
                        Qf_absmax = max(mwmer_max,mer_stat[4])
                        Qfmer_min = (a_man*mwmer_min + wtf_con*Qmlower)/(a_man+wtf_con)
                        Qfmer_max = (a_man*mwmer_max + wtf_con* mer_stat[3])/(a_man+wtf_con)
                        Qfmer = (a_man*mwmer_avg + wtf_con*mer_stat[7])/(a_man+wtf_con)
                        skipFMER = 212 
                    else:
                        #all MER
                        Qmlower = cur_Qlower 
                        Qf_absmin = min(mer_stat[0],wemer_min,mwmer_min)
                        Qf_absmax = max(mer_stat[4],wemer_max,mwmer_max)
                        Qfmer_min = (wtf_exp*wemer_min+a_man*mwmer_min + wtf_con*Qmlower)/(wtf_exp+a_man+wtf_con)
                        Qfmer_max = (wtf_exp*wemer_max+a_man*mwmer_max + wtf_con* mer_stat[3])/(wtf_exp+a_man+wtf_con)
                        Qfmer = (wtf_exp*wemer_avg + a_man*mwmer_avg + wtf_con*mer_stat[7])/(wtf_exp+a_man+wtf_con)
                        skipFMER = 222 
        
        if TIMEBASE == 15:
            FMERstat(MER_Stat15)
        
        elif TIMEBASE == 30:
            FMERstat(MER_Stat30)
        
        elif TIMEBASE == 60:
            FMERstat(MER_Stat1h)
        
        else:
            FMERstat(MER_Stat3h)
        
        
        global MERmaxNowiHmin
        
        if skipFMER ==1:
            logger7.info("CAUTION: No data to process FMER!")
            logger7.info("*********************************")
            logger7.info()
        else:        
            if TIMEBASE == 15:
                tibalabel = "15 min"
                MERmaxNowiHmin = min(max(mer_stack15[1][0],mer_stack15[2][0],mer_stack15[3][0]),min(mer_stack15[1][1],mer_stack15[2][1],mer_stack15[3][1]))
                hbe_min = result15_stack[0]
                hbe_max = result15_stack[2] 
                save_mer_logfile(N15min,result15_stack[1],MER_Stat15,mer_stack15[1][1],mer_stack15[2][1],mer_stack15[3][1],mer_stack15[5][1],15)
                save_current_mer(N15min,MER_Stat15,15)    
            
            elif TIMEBASE == 30:
                tibalabel = "30 min"
                MERmaxNowiHmin = min(max(mer_stack30[1][0],mer_stack30[2][0],mer_stack30[3][0]),min(mer_stack30[1][1],mer_stack30[2][1],mer_stack30[3][1]))
                hbe_min = result30_stack[0]
                hbe_max = result30_stack[2] 
                save_mer_logfile(N30min,result30_stack[1],MER_Stat30,mer_stack30[1][1],mer_stack30[2][1],mer_stack30[3][1],mer_stack30[5][1],30)
                save_current_mer(N30min,MER_Stat30,30)

                
            elif TIMEBASE == 60:
                tibalabel = "60 min"
                MERmaxNowiHmin = min(max(mer_stack1h[1][0],mer_stack1h[2][0],mer_stack1h[3][0]),min(mer_stack1h[1][1],mer_stack1h[2][1],mer_stack1h[3][1]))
                hbe_min = result1h_stack[0]
                hbe_max = result1h_stack[2] 
                save_mer_logfile(N1h,result1h_stack[1],MER_Stat1h,mer_stack1h[1][1],mer_stack1h[2][1],mer_stack1h[3][1],mer_stack1h[5][1],60)
                save_current_mer(N1h,MER_Stat1h,60)
                
            else:
                tibalabel = "180 min"
                MERmaxNowiHmin = min(max(mer_stack3h[1][0],mer_stack3h[2][0],mer_stack3h[3][0]),min(mer_stack3h[1][1],mer_stack3h[2][1],mer_stack3h[3][1]))
                hbe_min = result3h_stack[0]
                hbe_max = result3h_stack[2] 
                save_mer_logfile(N3h,result3h_stack[1],MER_Stat3h,mer_stack3h[1][1],mer_stack3h[2][1],mer_stack3h[3][1],mer_stack3h[5][1],180)
                save_current_mer(N3h,MER_Stat3h,180)   
            logger7.info(" Log files recorded. \n ")
            logger7.info("***** step 7 successful *****")
            
            tiPH,bePH,minPH,maxPH = np.loadtxt(out_txt+"_mer_LOG.txt", usecols=(0,2,95,96), unpack=True, delimiter='\t')
            
            
            
            if isinstance(tiPH, list) == True:
                tiPH_end = tiPH[-1]
            else:
                tiPH_end = tiPH
 
            if type(tiPH) is np.ndarray:
                tiPH_end = tiPH[-1]
            else:
                tiPH_end = tiPH

                
            def plot_plh(ti_PH,be_PH,max_PH,min_PH,tb):
                try:
                    mintim=min(ti_PH)
                    maxtim=max(ti_PH)
                    minPH=min(be_PH)                
                    maxPH=max(be_PH)
                except TypeError: 
                    mintim = 0
                    maxtim =ti_PH
                    minPH=0                
                    maxPH=be_PH

                print(">>>> phPlot maxtim: "+str(maxtim))
                print(">>>> phPlot maxPH: "+str(maxPH))
                plt.plot(ti_PH,be_PH,color="blue")
                plt.plot(ti_PH,max_PH,color="red")
                plt.plot(ti_PH,min_PH,color="green")

                fig = figure.Figure()

                ax = plt.subplot(111)
                plt.text(0.5*maxtim, 0.5*maxPH, 'REFIR',fontsize=80, color='gray',ha='center', va='center', alpha=0.09)
                mpl.rcParams['ytick.labelsize'] = 12 
                mpl.rcParams['xtick.labelsize'] = 12
                
                #im = image.imread(path_logo)
                #myaximage = ax.imshow(im, aspect='auto', extent=(0,maxtim,0,maxPH), alpha=0.05, zorder=-1)
#                plt.legend(['current t_base: '+ tb], loc='upper left')
                plt.legend(['Average', 'Maximum', 'Minimum'], loc='lower right',
                           ncol=1, fancybox=True, shadow=True,
                           title="current timebase: " + tibalabel)
                plt.xlabel('time since eruption start [min]')
                plt.ylabel('height a.s.l. [m]')
                plt.title('Plume Height a.s.l. [m]')
                plt.ylim([0,np.amax(be_PH)+2000])
                #plt.xticks

                if PM_PHplot == 1:
                    plt.xlim(0)
                elif PM_PHplot == 2:
                    tiPH_start = tiPH_end-720
                    plt.xlim([tiPH_start,tiPH_end])
                elif PM_PHplot == 3:
                    tiPH_start = tiPH_end-360
                    plt.xlim([tiPH_start,tiPH_end])
                elif PM_PHplot == 4:
                    tiPH_start = tiPH_end-60
                    plt.xlim([tiPH_start,tiPH_end])
                else:
                    tiPH_start = tiPH_end-15
                    plt.xlim([tiPH_start,tiPH_end])
                
                plt.grid()
                plt.savefig(out_txt+"_PH_plot.png",bbox_inches='tight',dpi=300)
                plt.savefig(out_txt+"_PH_plot.svg", format='svg', dpi=1200) #highresolution


                plt.close("all")
                plt.close()
                del gc.garbage[:]
            if PM_PHplot == 0:
                logger9.info("plume height plot: switched OFF!")
            else:
                plot_plh(tiPH,bePH+vent_h,maxPH+vent_h,minPH+vent_h,tibalabel)
            
            tiPH,MERWE,MERww,MERsp,MERma,MERmtg,MERdb,RMER,MIN,MAX,MERavg,MERwood,MERwood0d = \
            np.loadtxt(out_txt+"_mer_LOG.txt", usecols=(0,5,13,14,15,16,17,18,3,7,19,21,183), unpack=True, delimiter='\t')
    
            Qc_lower,Qc_upper = \
            np.loadtxt(out_txt+"_mer_LOG.txt", usecols=(110,6), unpack=True, delimiter='\t')
            
#here FMER mass:
            Qfabs_min,Qfabs_max,Fmer_min,Fmer,Fmer_max = \
            np.loadtxt(out_txt+"_mer_LOG.txt", usecols=(117,118,119,120,121), unpack=True, delimiter='\t')

            
            def plot_MER_wood():

                fig = figure.Figure()
                ax = plt.subplot(111)
                mpl.rcParams['ytick.labelsize'] = 14 
                mpl.rcParams['xtick.labelsize'] = 12                 
                plt.plot(tiPH,Qc_lower,"--",color="Lime", linewidth =3.0)
                plt.plot(tiPH,Qc_upper,"--",color="Gold", linewidth =3.0)
                plt.plot(tiPH,MERww,color="green")
                plt.plot(tiPH,MERsp,color='purple')
                plt.plot(tiPH,MERma,color='dodgerblue')
                plt.plot(tiPH,MERmtg,color='cyan')
                plt.plot(tiPH,MERwood0d,color="grey")
                if plh_correction == 1:
                    logger9.info("*** Deg Bon and Wood0D models are using centerline height ***")
                plt.plot(tiPH,MERdb,color='orange')
                plt.plot(tiPH,MERwood,color='deeppink')
                plt.plot(tiPH,RMER,":",color='blue',linewidth =5.0)
                
                plt.plot(tiPH,MAX,"--",color='grey')
                plt.plot(tiPH,MIN,"--",color='grey')
                
                
                plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
                lgd = plt.legend(['CMER_lower', 'CMER_upper', 'Wilson Walker', 'Sparks', 'Mastin', 'Gudmundsson', \
                                  'Woodhouse0D', 'Deg & Bon', 'PlumeRise', 'CMER', "abs.min/max"], loc='lower right',
                                 bbox_to_anchor \
                                     =(1.6, 0), ncol=1, fancybox=True, shadow=True,
                                 title="current timebase: " + tibalabel)
                
                plt.xlabel('time since eruption start [min]')
                plt.ylabel('mass eruption rate [kg/s]')
                plt.title("First estimate of MER (CMER)")
                
                plt.yscale('log')
                plt.ylim(0)
                ax.grid()
                try:
                    maxX=max(tiPH)                
                    maxY=max(MAX)
                except TypeError: 
                    maxX =tiPH          
                    maxY= MAX

                if PM_MERplot == 1:
                    plt.xlim(0)
                elif PM_MERplot == 2:
                    tiCMER_start = tiPH_end-720
                    plt.xlim([tiCMER_start,tiPH_end])
                    maxX = tiPH_end - tiCMER_start
                elif PM_MERplot == 3:
                    tiCMER_start = tiPH_end-360
                    plt.xlim([tiCMER_start,tiPH_end])
                    maxX = tiPH_end - tiCMER_start
                elif PM_MERplot == 4:
                    tiCMER_start = tiPH_end-60
                    plt.xlim([tiCMER_start,tiPH_end])
                    maxX = tiPH_end - tiCMER_start
                else:
                    tiCMER_start = tiPH_end-15
                    plt.xlim([tiCMER_start,tiPH_end])
                    maxX = tiPH_end - tiCMER_start
                
                plt.text(0.5, 0.5, 'REFIR',fontsize=80, color='gray',ha='center', va='center',transform=ax.transAxes, alpha=0.09)
                plt.savefig(out_txt+"_CMER_plot.png", bbox_extra_artists=(lgd,), bbox_inches='tight', dpi=300)
                plt.savefig(out_txt+"_CMER_plot.svg", format='svg', dpi=1200) #highresolution
                plt.close(fig)
                plt.close("all")

            def plot_MER():

                
               
                fig = figure.Figure()
                ax = plt.subplot(111)
                mpl.rcParams['ytick.labelsize'] = 14 
                mpl.rcParams['xtick.labelsize'] = 12 
                plt.plot(tiPH,Qc_lower,"--",color="Lime", linewidth =3.0)
                plt.plot(tiPH,Qc_upper,"--",color="Gold", linewidth =3.0)
                plt.plot(tiPH,MERww,color="green")
                plt.plot(tiPH,MERsp,color='purple')
                plt.plot(tiPH,MERma,color='dodgerblue')
                plt.plot(tiPH,MERmtg,color='cyan')
                plt.plot(tiPH, MERwood0d, color="grey")

                if plh_correction == 1:
                    print("** DegBon and Wood0D models are using centreline height **" )
                plt.plot(tiPH,MERdb,color='orange')
                plt.plot(tiPH,RMER,":",color='blue',linewidth =5.0)
                
                plt.plot(tiPH,MAX,"--",color='grey')
                plt.plot(tiPH,MIN,"--",color='grey')
                
                
                plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

                lgd = plt.legend(['CMER_lower', 'CMER_upper', 'Wilson Walker', 'Sparks', 'Mastin', 'Gudmundsson', \
                                  'Woodhouse0D', 'Deg & Bon', 'CMER', "abs.min/max"], loc='lower right', bbox_to_anchor \
                                     =(1.6, 0), ncol=1, fancybox=True, shadow=True,
                                 title="current timebase: " + tibalabel)

                plt.xlabel('time since eruption start [min]')
                plt.ylabel('mass eruption rate [kg/s]')
                plt.title("First estimate of MER (CMER)")
                plt.yscale('log')            
                plt.ylim(0)
                ax.grid()
                try:
                    maxX=max(tiPH)                
                    maxY=max(MAX)
                except TypeError: 
                    maxX =tiPH          
                    maxY= MAX
 
                if PM_MERplot == 1:
                    plt.xlim(0)
                elif PM_MERplot == 2:
                    tiCMER_start = tiPH_end-720
                    plt.xlim([tiCMER_start,tiPH_end])
                    maxX = tiPH_end - tiCMER_start
                elif PM_MERplot == 3:
                    tiCMER_start = tiPH_end-360
                    plt.xlim([tiCMER_start,tiPH_end])
                    maxX = tiPH_end - tiCMER_start
                elif PM_MERplot == 4:
                    tiCMER_start = tiPH_end-60
                    plt.xlim([tiCMER_start,tiPH_end])
                    maxX = tiPH_end - tiCMER_start
                else:
                    tiCMER_start = tiPH_end-15
                    plt.xlim([tiCMER_start,tiPH_end])
                    maxX = tiPH_end - tiCMER_start
                plt.text(0.5, 0.5, 'REFIR',fontsize=80, color='gray',ha='center', va='center',transform=ax.transAxes, alpha=0.09)                    
                plt.savefig(out_txt+"_CMER_plot.png", bbox_extra_artists=(lgd,), bbox_inches='tight', dpi=300)
                plt.savefig(out_txt+"_CMER_plot.svg", format='svg', dpi=1200) #highresolution
                plt.close("all")
                plt.close(fig)
                del gc.garbage[:]

            def plot_FMER():
                fig = figure.Figure()
                
                ax = plt.subplot(111)
                mpl.rcParams['ytick.labelsize'] = 14 
                mpl.rcParams['xtick.labelsize'] = 12                 
                plt.plot(tiPH,Fmer_min,color="Lime", linewidth =3.0)
                plt.plot(tiPH,Fmer_max,color="Gold", linewidth =3.0)
                plt.plot(tiPH,Fmer,":",color='red',linewidth =5.0)
                plt.plot(tiPH,Qfabs_max,"--",color='grey')
                plt.plot(tiPH,Qfabs_min,"--",color='grey')

                plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
                lgd=plt.legend(['FMER_min', 'FMER_max',\
                'FMER', "abs.min/max"], loc='lower right', bbox_to_anchor\
                =(1.6, 0), ncol=1, fancybox=True, shadow=True,title="current timebase: " + tibalabel)

                plt.xlabel('time since eruption start [min]')
                plt.ylabel('mass eruption rate [kg/s]')
                plt.title("Best Estimate of MER by FOXI (FMER)")
                
                plt.yscale('log')
                plt.ylim(0)
                ax.grid()
                try:
                    maxX=max(tiPH)                
                    maxY=max(Qfabs_max)
                except TypeError: 
                    maxX =tiPH          
                    maxY=Qfabs_max
                                
                if PM_FMERplot == 1:
                    plt.xlim(0)
                elif PM_FMERplot == 2:
                    tiFMER_start = tiPH_end-720
                    plt.xlim([tiFMER_start,tiPH_end])
                    maxX=abs(tiPH_end-tiFMER_start)
                elif PM_FMERplot == 3:
                    tiFMER_start = tiPH_end-360
                    plt.xlim([tiFMER_start,tiPH_end])
                    maxX=abs(tiPH_end-tiFMER_start)
                elif PM_FMERplot == 4:
                    tiFMER_start = tiPH_end-60
                    plt.xlim([tiFMER_start,tiPH_end])
                    maxX=abs(tiPH_end-tiFMER_start)
                else:
                    tiFMER_start = tiPH_end-15
                    plt.xlim([tiFMER_start,tiPH_end])
                    maxX=abs(tiPH_end-tiFMER_start)
                plt.text(0.5, 0.5, 'REFIR',fontsize=80, color='gray',ha='center', va='center',transform=ax.transAxes, alpha=0.09)  
                
                plt.savefig(out_txt+"_FMER_plot.png", bbox_extra_artists=(lgd,), bbox_inches='tight', dpi=300)
                plt.savefig(out_txt+"_FMER_plot.svg", format='svg', dpi=1200) #highresolution
                plt.close("all")
                plt.close(fig)
                plt.clf()
                plt.cla()
                plt.close()
                del gc.garbage[:]

            if file_wood == 0:
                if PM_MERplot == 0:
                    logger9.info("CMER plot switched OFF!")
                else:
                    plot_MER()
                if PM_FMERplot == 0:
                    logger9.info("FMER plot switched OFF!")
                else:                
                    plot_FMER()
            else:
                if PM_MERplot == 0:
                    logger9.info("CMER plot switched OFF!")
                else:
                    plot_MER_wood()
                if PM_FMERplot == 0:
                    logger9.info("FMER plot switched OFF!")
                else:                
                    plot_FMER()

            
            tiPH,N_mess = \
            np.loadtxt(out_txt+"_mer_LOG.txt", usecols=(0,1), unpack=True, delimiter='\t')
            
            def plot_N():
                """provides the operator an overview of involved data sources"""
            #data gaps and "poorly covered periods" can be identified!    
                
                fig = plt.figure()
                ax = plt.subplot(111)
                ax.bar(tiPH, N_mess, width=5)
                mpl.rcParams['ytick.labelsize'] = 12 
                mpl.rcParams['xtick.labelsize'] = 12                
                
                plt.xlabel('time since eruption start [min]')
                plt.ylabel(' ')
                plt.title("number of data considered per run")
                
                if PM_Nplot == 1:
                    plt.xlim(0)
                elif PM_Nplot == 2:
                    tiN_start = tiPH_end-720
                    plt.xlim([tiN_start,tiPH_end])
                elif PM_Nplot == 3:
                    tiN_start = tiPH_end-360
                    plt.xlim([tiN_start,tiPH_end])
                elif PM_Nplot == 4:
                    tiN_start = tiPH_end-60
                    plt.xlim([tiN_start,tiPH_end])
                else:
                    tiN_start = tiPH_end-15
                    plt.xlim([tiN_start,tiPH_end])
                ax.grid()
                
                #plt.show()
                fig.savefig(out_txt+"_N_plot.png",bbox_inches='tight', dpi=300) 
                fig.savefig(out_txt+"_N_plot.svg", format='svg', dpi=1200) #highresolution
                plt.close("all")
                plt.close(fig)
                del gc.garbage[:]
            if PM_Nplot == 0:
                logger9.info("N plot: switched OFF!")
            else:        
                plot_N()
            
            
            logger9.info("\n MER plots provided. \n ")
            logger9.info("***** step 9 successful *****")
            logger9.info("")

            
            logger8.info("*******************************")
            logger8.info("Now computing erupted mass....")
            logger8.info("*******************************")
            """
            next step: Integration of calculated masses
            
            used MER data:
            MERMIN_hmin >>> absolute minimum                >>>M_MIN_hmin
            
            MERMAX_hmin >>> most likely lower boundary      >>>M_MAXhmin
            MERWE       >>> weighted average                >>>M_MERWE
            R_MER       >>> best estimate (constrained mean)>>>M_RMER
            MERMAX_PLUS >>> most likely upper boundary      >>>M_MAXPLUS
            
            MERMAX_hmax >>> absolute maximum                >>>M_MAX_hmax
            
            """
            
            MAXhmin,MAXPLUS = np.loadtxt(out_txt+"_mer_LOG.txt", usecols=(4,6), unpack=True, delimiter='\t')
            
            
            if isinstance( tiPH, float ):
                t_s =tiPH
            else:
                t_s = [xx * 60 for xx in tiPH.tolist()] #list of times in seconds
            try:
                FILE1 = open(out_txt+"_mass_LOG.txt", "r",encoding="utf-8", errors="surrogateescape")
                M_MIN_hmin = np.trapz(MIN,x=t_s)
                M_MAX_hmax = np.trapz(MAX,x=t_s)
                M_MAXhmin = np.trapz(MAXhmin,x=t_s)
                M_MERWE = np.trapz(MERWE,x=t_s)
                M_RMER = np.trapz(RMER,x=t_s)
                M_MAXPLUS = np.trapz(MAXPLUS,x=t_s)
                M_MERmtg = np.trapz(MERmtg,x=t_s)
                M_MERdb = np.trapz(MERdb,x=t_s)
                M_MERwood0d = np.trapz(MERwood0d,x=t_s)
                M_Qc_lower = np.trapz(Qc_lower,x=t_s)
                M_FABSMIN = np.trapz(Qfabs_min,x=t_s)
                M_FABSMAX = np.trapz(Qfabs_max,x=t_s)
                M_FMERMIN = np.trapz(Fmer_min,x=t_s)
                M_FMER = np.trapz(Fmer,x=t_s)
                M_FMERMAX = np.trapz(Fmer_max,x=t_s)
                FILE1.close()
            except EnvironmentError:  
                M_MIN_hmin = 0
                M_MAX_hmax = 0
                M_MAXhmin = 0
                M_MERWE = 0
                M_RMER = 0
                M_MAXPLUS = 0
                M_MERmtg = 0
                M_MERdb = 0
                M_MERwood0d = 0
                M_Qc_lower = 0
                
                M_FABSMIN = 0
                M_FABSMAX = 0
                M_FMERMIN = 0
                M_FMER = 0
                M_FMERMAX = 0
            def save_totalmass_logfile(M_MIN_hmin,M_MAXhmin,M_MERWE,M_RMER,M_MAXPLUS,M_MAX_hmax,M_MERmtg,M_MERdb,M_MERwood0d,M_FABSMIN,M_FABSMAX,M_FMERMIN,M_FMER,M_FMERMAX):
                """ logs continously statistic summary of MER in a file"""
    
                FILE1 = open(out_txt+"_mass_LOG.txt", "a",encoding="utf-8", errors="surrogateescape")
                
                FILE1.write(str(timin) +"\t"+str(M_MIN_hmin)+"\t"+str(M_MAX_hmax)+"\t"+str(M_MAXhmin)+"\t"\
                +str(M_MERWE)+"\t"+str(M_RMER)+"\t"+str(M_MAXPLUS)\
                +"\t"+str(M_MERmtg)+"\t"+str(M_MERdb)+"\t"+str(M_MERwood0d)+"\t"+str(M_Qc_lower)+\
"\t"+str(M_FABSMIN)+"\t"+str(M_FABSMAX)+"\t"+str(M_FMERMIN)+\
"\t"+str(M_FMER)+"\t"+str(M_FMERMAX)+"\n")
                FILE1.close()
            
            
            save_totalmass_logfile(M_MIN_hmin,M_MAXhmin,M_MERWE,M_RMER,M_MAXPLUS,M_MAX_hmax,M_MERmtg,M_MERdb,M_MERwood0d,M_FABSMIN,M_FABSMAX,M_FMERMIN,M_FMER,M_FMERMAX)
         
            def plot_TotalMass():
                
                with open(out_txt+"_mass_LOG.txt", "r",encoding="utf-8", errors="surrogateescape") as FILE1:
                    tiM,SM_MIN_hmin,SM_MAX_hmax,SM_MAXhmin,SM_MERWE,SM_RMER,SM_MAXPLUS,SM_MERmtg,SM_MERdb,SM_MERwood0d,SM_MQclower = \
                np.loadtxt(FILE1, usecols=(0,1,2,3,4,5,6,7,8,9,10), unpack=True, delimiter='\t')
                
                if run == 1:
                    tiM_end = tiM
                else:
                    if isinstance(tiM, list):
                        tiM_end = tiM[-1]
                    else:
                        tiM_end = tiM
                
                fig = plt.figure()
                ax = plt.subplot(111)
                mpl.rcParams['ytick.labelsize'] = 14 
                mpl.rcParams['xtick.labelsize'] = 12   
                plt.plot(tiM,SM_MQclower,"--",color="Lime", linewidth =3.0)
                plt.plot(tiM,SM_MAXPLUS,"--",color='Gold', linewidth =3.0)
                
        
                plt.plot(tiM,SM_RMER,":",color='red',linewidth =6.0)
                
                
                

                plt.plot(tiM,SM_MAX_hmax,"--",color='grey',linewidth =2.0)
                plt.plot(tiM,SM_MIN_hmin,"--",color='grey',linewidth =2.0)
                
                
                plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
                
                """lgd=plt.legend(['M_CMER_min', 'M_CMER_max', "M_CMER","M_Gudmunds","M_Degr_Bona",\
                'M_C_abs.min/max'], loc='lower right', bbox_to_anchor\
                =(1.6, 0), ncol=1, fancybox=True, shadow=True,title="current timebase: " + tibalabel)"""

                lgd=plt.legend(['M_CMER_min', 'M_CMER_max', "M_CMER",'M_C_abs.min/max'],\
                loc='lower right', bbox_to_anchor=(1.6, 0), ncol=1, fancybox=True,\
                shadow=True,title="current timebase: " + tibalabel)
                
                plt.xlabel('time since eruption start [min]')
                plt.ylabel('total mass erupted [kg]')
                plt.title("First Estimate Of Total Erupted Mass")
                
                plt.ylim(0)
                ax.grid()
                fig.text(0.5, 0.5, 'REFIR',fontsize=80, color='gray',ha='center', va='center', alpha=0.09)
                if PM_TME == 1:
                    plt.xlim(0)
                elif PM_TME == 2:
                    tiM_start = tiM_end-720
                    plt.xlim([tiM_start,tiM_end])
                elif PM_TME == 3:
                    tiM_start = tiM_end-360
                    plt.xlim([tiM_start,tiM_end])
                elif PM_TME == 4:
                    tiM_start = tiM_end-60
                    plt.xlim([tiM_start,tiM_end])
                else:
                    tiM_start = tiM_end-15
                    plt.xlim([tiM_start,tiM_end])
                #plt.show()
                fig.savefig(out_txt+"_Cmass_plot.png", bbox_extra_artists=(lgd,), bbox_inches='tight',dpi=300)
                fig.savefig(out_txt+"_Cmass_plot.svg", format='svg', dpi=1200) #highresolution
                plt.close("all")
                plt.close(fig)
                del gc.garbage[:]
                plt.clf()
                plt.cla()
                plt.close()
            if PM_TME == 0:
                logger8.info("Mass plot (1st est.): switched OFF!")
            else:        
                plot_TotalMass()    
            logger8.info("\n Total mass erupted computed -  first estimate plot provided. \n ")

            def plot_TotalMassFMER():
                with open(out_txt+"_mass_LOG.txt", "r",encoding="utf-8", errors="surrogateescape") as FILE1:
                    tiM,SM_FABSMIN,SM_FABSMAX,SM_FMERMIN,SM_FMER,SM_FMERMAX = \
                np.loadtxt(FILE1, usecols=(0,11,12,13,14,15), unpack=True, delimiter='\t')
                
                if run == 1:
                    tiM_end = tiM
                else:
                    if isinstance(tiM, list):
                        tiM_end = tiM[-1]
                    else:
                        tiM_end = tiM
                fig = plt.figure()
                
                ax = plt.subplot(111)
                mpl.rcParams['ytick.labelsize'] = 14 
                mpl.rcParams['xtick.labelsize'] = 12
                plt.plot(tiM,SM_FMERMIN,color="Lime", linewidth =3.0)
                plt.plot(tiM,SM_FMERMAX,color='Gold', linewidth =3.0)
                
        
                plt.plot(tiM,SM_FMER,":",color='red',linewidth =6.0)
                
                
                plt.plot(tiM,SM_FABSMAX,"--",color='grey',linewidth =2.0)
                plt.plot(tiM,SM_FABSMIN,"--",color='grey',linewidth =2.0)
                
                
                plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
                
                lgd=plt.legend(['M_FMER_min', 'M_FMER_max', "M_FMER",\
                'M_abs.min/max'], loc='lower right', bbox_to_anchor\
                =(1.6, 0), ncol=1, fancybox=True, shadow=True,title="current timebase: " + tibalabel)
                
                
                plt.xlabel('time since eruption start [min]')
                plt.ylabel('total mass erupted [kg]')
                plt.title("FOXI Estimate Of Total Erupted Mass")
                
                plt.ylim(0)
                ax.grid()
                fig.text(0.5, 0.5, 'REFIR',fontsize=80, color='gray',ha='center', va='center', alpha=0.09)
                if PM_FTME == 1:
                    plt.xlim(0)
                elif PM_FTME == 2:
                    tiM_start = tiM_end-720
                    plt.xlim([tiM_start,tiM_end])
                elif PM_FTME == 3:
                    tiM_start = tiM_end-360
                    plt.xlim([tiM_start,tiM_end])
                elif PM_FTME == 4:
                    tiM_start = tiM_end-60
                    plt.xlim([tiM_start,tiM_end])
                else:
                    tiM_start = tiM_end-15
                    plt.xlim([tiM_start,tiM_end])
                #plt.show()
                fig.savefig(out_txt+"_Fmass_plot.png", bbox_extra_artists=(lgd,), bbox_inches='tight',dpi=300)
                fig.savefig(out_txt+"_Fmass_plot.svg", format='svg', dpi=1200) #highresolution
                plt.close("all")
                plt.close(fig)
                del gc.garbage[:]
                plt.clf()
                plt.cla()
                plt.close()
            if PM_FTME == 0:
                logger8.info("Mass plot (FMER est.): switched OFF!")
            else:        
                plot_TotalMassFMER()               
            
            logger8.info("\n Total mass erupted computed -  best estimate plot provided. \n ")           
            logger8.info("***** steps 8 successful *****")
            
            def saveStatus1():
                """updates status files"""
                
                time_nun = TimeNOW.strftime("%m/%d/%Y %H:%M:%S") 
                  
                FILE3 = open(out_txt+"_status1.txt", "w",encoding="utf-8", errors="surrogateescape")
                FILE3.write("PLUME HEIGHT STATUS\n"+\
                "==========================================\n"+\
                scenario+"\n"+"\n"+\
                "<<<<<<<<<<<"+str(time_nun)+">>>>>>>>>>>>\n"+\
                "\n"+\
                "    >>> Plume Height Stats (above vent) <<<        \n"+\
                "------------------------------------------\n"+\
                "time frame:\t" +str(TIMEBASE)+" min\n"+\
                "tracked data N:\t" +str(cur_N)+"\n"+\
                "minimum pl.h.:\t" +str(cur_hbe_min)+" m\n"+\
                "best e. pl.h.:\t" +str(cur_hbe)+" m\n"+\
                "maximum pl.h.:\t" +str(cur_hbe_max)+" m\n"+\
                "\n"+\
                 "==================================================\n")
                FILE3.close()
                    
                FILE4 = open(out_txt+"_status2.txt", "w",encoding="utf-8", errors="surrogateescape")
                    
                if cur_MERMAX_hmin < cur_MERavg:                  
                    FILE4.write("ERUPTION SOURCE PARAMETER STATUS 1\n"+\
                    "==========================================\n"+\
                    "   >>> Overall Mass Eruption Rate Stats <<<             \n"+\
                    "------------------------------------------\n"+\
                    "abs. min MER: \t" +"{:1.1e}".format(cur_MERMIN_hmin)+" kg/s\n"+\
                    "average MER: \t" +"{:1.1e}".format(cur_MERavg)+" kg/s\n"+\
                    "abs. max MER: \t" +"{:1.1e}".format(cur_MaxMERhmax)+" kg/s\n"+\
                    "\n"+\
                    "  >>> Best Estimate of Current MER  <<<             \n"+\
                    "==========================================\n"+\
                    "lower boundary:\t" +"{:1.1e}".format(cur_MERMAX_hmin)+" kg/s\n"+\
                    "\t\t*************\n"+\
                    "best est. MER: \t" +"{:1.1e}".format(cur_MERWE)+" kg/s\n"+\
                    "\t\t*************\n"+\
                    "upper boundary:\t" +"{:1.1e}".format(cur_MERMAX_PLUS)+" kg/s\n"+\
                    "==========================================\n"+\
                    "\n"+\
                    "CAUTION !! \n"+\
                    "All values presented are automatically generated \n"+\
                    "\t >> PRELIMINARY RESULTS << \n"\
                    +"and need to be confirmed by authorized staff!\n")
                    FILE4.close()
                else:
                    FILE4 = open(out_txt+"_status2.txt", "w",encoding="utf-8", errors="surrogateescape")
                    FILE4.write("ERUPTION SOURCE PARAMETER STATUS 1\n"+\
                    "==========================================\n"+\
                    "   >>> Overall Mass Eruption Rate Stats <<<             \n"+\
                    "------------------------------------------\n"+\
                    "abs. min MER: \t" +"{:1.1e}".format(cur_MERMIN_hmin)+" kg/s\n"+\
                    "average MER: \t" +"{:1.1e}".format(cur_MERavg)+" kg/s\n"+\
                    "abs. max MER: \t" +"{:1.1e}".format(cur_MaxMERhmax)+" kg/s\n"+\
                    "\n"+\
                    "  >>> Best Estimate of Current MER  <<<             \n"+\
                    "==========================================\n"+\
                    "lower boundary:\t" +"{:1.1e}".format(MERmaxNowiHmin)+" kg/s\n"+\
                    "\t\t*************\n"+\
                    "best est. MER: \t" +"{:1.1e}".format(cur_MERWE)+" kg/s\n"+\
                    "\t\t*************\n"+\
                    "upper boundary:\t" +"{:1.1e}".format(cur_MERMAX_PLUS)+" kg/s\n"+\
                    "==========================================\n"+\
                    "\n"+\
                    "CAUTION !! \n"+\
                    "All values presented are automatically generated \n"+\
                    "\t >> PRELIMINARY RESULTS << \n"\
                    +"and need to be confirmed by authorized staff!\n")
                    FILE4.close()


                FILE5 = open(out_txt+"_status3.txt", "w",encoding="utf-8", errors="surrogateescape")
                    
                Vol_MIN_hmin = M_MIN_hmin/1000
                Vol_MERWE = M_MERWE/1000
                Vol_MAXPLUS = M_MAXPLUS/1000
                FILE5.write("ERUPTION SOURCE PARAMETER STATUS 2\n"+\
                "=========================================================\n"+\
                    "  >>> Computed Total Erupted Mass <<<   (Approx. Erupted Volume**)\n"+\
                    "---------------------------------------------------------------\n"+\
                    "lower boundary*: \t" +"{:1.1e}".format(M_MIN_hmin)+" kg\t"+"({:1.1e}".format(Vol_MIN_hmin)+" m^3)\n"+\
                    "best estimate m*:\t" +"{:1.1e}".format(M_MERWE)+" kg\t"+"({:1.1e}".format(Vol_MERWE)+" m^3)\n"+\
                    "upper boundary*:\t" +"{:1.1e}".format(M_MAXPLUS)+" kg\t"+"({:1.1e}".format(Vol_MAXPLUS)+" m^3)\n"+\
                    "-----------------------------------------------------------------------------\n"+\
                    "                                          (**assuming bulk dens: 1000 kg/m^3)\n"+\
                    "===========================================================\n"+\
                    "*Note: Mass integrated only over monitored time period, \n"+\
                    " thus displayed numbers might be underestimates!\n"+\
                    "\n"+\
                    "CAUTION !! \n"+\
                    "All values presented are automatically generated \n"+\
                    "\t >> PRELIMINARY RESULTS << \n"\
                    +"and need to be confirmed by authorized staff!\n")
                FILE5.close()
            
                FILE6 = open(out_txt+"_status4.txt", "w",encoding="utf-8", errors="surrogateescape")
                    
                          
                FILE6.write("REFIR MODEL PARAMETERS 1 \n"+\
                "================================================\n"+\
                    "  >>> Input parameters <<<        \n"+\
                    "-----------------------------------------\n"+\
                        "vulkan"+"\t"+str(vulkan)+"\n"+\
                        "vent_h"+"\t"+str(vent_h)+"\n"+\
                        "time_OBS"+"\t"+str(time_OBS)+"\n"+\
                        "Hmin_obs"+"\t"+str(Hmin_obs)+"\n"+\
                        "Hmax_obs"+"\t"+str(Hmax_obs)+"\n"+\
                        "OBS_on"+"\t"+str(OBS_on)+"\n"+\
                        "qf_OBS"+"\t"+str(qf_OBS)+"\n"+\
                        "theta_a0"+"\t"+str(theta_a0)+"\n"+\
                        "P_0"+"\t"+str(P_0)+"\n"+\
                        "theta_0"+"\t"+str(theta_0)+"\n"+\
                        "rho_dre"+"\t"+str(rho_dre)+"\n"+\
                        "alpha"+"\t"+str(alpha)+"\n"+\
                        "beta"+"\t"+str(beta)+"\n"+\
                        "H1"+"\t"+str(H1)+"\n"+\
                        "H2"+"\t"+str(H2)+"\n"+\
                        "tempGrad_1"+"\t"+str(tempGrad_1)+"\n"+\
                        "tempGrad_2"+"\t"+str(tempGrad_2)+"\n"+\
                        "tempGrad_3"+"\t"+str(tempGrad_3)+"\n"+\
                        "Vmax"+"\t"+str(Vmax)+"\n"+\
                        "============================================\n")
                FILE6.close()

                FILE7 = open(out_txt+"_status5.txt", "w",encoding="utf-8", errors="surrogateescape")
                    
                          
                FILE7.write("REFIR MODEL PARAMETERS 2 \n"+\
                "===============================================\n"+\
                "  >>> Stream Data Accuracy I<<<        \n"+\
                "---------------------------------------\n" +\
                "qfak_ISKEF"+"\t"+str(qfak_ISKEF)+"\n"+\
                "qfak_ISEGS"+"\t"+str(qfak_ISEGS)+"\n"+\
                "qfak_Cband3"+"\t"+str(qfak_Cband3)+"\n"+\
                "qfak_Cband4"+"\t"+str(qfak_Cband4)+"\n"+\
                "qfak_Cband5"+"\t"+str(qfak_Cband5)+"\n"+\
                "qfak_Cband6"+"\t"+str(qfak_Cband6)+"\n"+\
                "qfak_ISX1"+"\t"+str(qfak_ISX1)+"\n"+\
                "qfak_ISX2"+"\t"+str(qfak_ISX2)+"\n"+\
                "qfak_Xband3"+"\t"+str(qfak_Xband3)+"\n"+\
                "qfak_Xband4"+"\t"+str(qfak_Xband4)+"\n"+\
                "qfak_Xband5"+"\t"+str(qfak_Xband5)+"\n"+\
                "qfak_Xband6"+"\t"+str(qfak_Xband6)+"\n"+\
                "qfak_GFZ1"+"\t"+str(qfak_GFZ1)+"\n"+\
                "qfak_GFZ2"+"\t"+str(qfak_GFZ2)+"\n"+\
                "qfak_GFZ3"+"\t"+str(qfak_GFZ3)+"\n"+\
                "qfak_Cam4"+"\t"+str(qfak_Cam4)+"\n"+\
                "qfak_Cam5"+"\t"+str(qfak_Cam5)+"\n"+\
                "qfak_Cam6"+"\t"+str(qfak_Cam6)+"\n"+\
                        "==============================================\n")
                FILE7.close()                    

                FILE7b = open(out_txt+"_status6.txt", "w",encoding="utf-8", errors="surrogateescape")
                    
                          
                FILE7b.write("REFIR MODEL PARAMETERS 3 \n"+\
                "===============================================\n"+\
                "  >>> Stream Data Accuracy II<<<        \n"+\
                "            (Uncertainties)             \n" +\
                "---------------------------------------\n" +\
                "unc_ISKEF"+"\t"+str(unc_ISKEF)+"\n"+\
                "unc_ISEGS"+"\t"+str(unc_ISEGS)+"\n"+\
                "unc_Cband3"+"\t"+str(unc_Cband3)+"\n"+\
                "unc_Cband4"+"\t"+str(unc_Cband4)+"\n"+\
                "unc_Cband5"+"\t"+str(unc_Cband5)+"\n"+\
                "unc_Cband6"+"\t"+str(unc_Cband6)+"\n"+\
                "unc_ISX1  "+"\t"+str(unc_ISX1)+"\n"+\
                "unc_ISX2  "+"\t"+str(unc_ISX2)+"\n"+\
                "unc_Xband3"+"\t"+str(unc_Xband3)+"\n"+\
                "unc_Xband4"+"\t"+str(unc_Xband4)+"\n"+\
                "unc_Xband5"+"\t"+str(unc_Xband5)+"\n"+\
                "unc_Xband6"+"\t"+str(unc_Xband6)+"\n"+\
                "==============================================\n")
                FILE7b.close()  

                    
                FILE8 = open(out_txt+"_status7.txt", "w",encoding="utf-8", errors="surrogateescape")
                FILE8.write("REFIR MODEL PARAMETERS 4 \n"+\
                "=========================================\n"+\
                "  >>> Sensor Locations <<<        \n"+\
                "-----------------------------------------\n" +\
                "loc_ISKEF"+"\t"+str(loc_ISKEF)+"\n"+\
                "loc_ISEGS"+"\t"+str(loc_ISEGS)+"\n"+\
                "loc_Cband3"+"\t"+str(loc_Cband3)+"\n"+\
                "loc_Cband4"+"\t"+str(loc_Cband4)+"\n"+\
                "loc_Cband5"+"\t"+str(loc_Cband5)+"\n"+\
                "loc_Cband6"+"\t"+str(loc_Cband6)+"\n"+\
                "loc_ISX1  "+"\t"+str(loc_ISX1)+"\n"+\
                "loc_ISX2  "+"\t"+str(loc_ISX2)+"\n"+\
                "loc_Xband3"+"\t"+str(loc_Xband3)+"\n"+\
                "loc_Xband4"+"\t"+str(loc_Xband4)+"\n"+\
                "loc_Xband5"+"\t"+str(loc_Xband5)+"\n"+\
                "loc_Xband6"+"\t"+str(loc_Xband6)+"\n"+\
                "============================================\n")
                FILE8.close()                    

                FILE9 = open(out_txt+"_status8.txt", "w",encoding="utf-8", errors="surrogateescape")
                FILE9.write("REFIR MODEL PARAMETERS 5 \n"+\
                "=================================================\n"+\
                "  >>> Sensor Settings I (Auto-stream sources) <<< \n"+\
                " --------------------------------------------------\n" +\
                "ISKEF_on"+"\t"+str(ISKEF_on)+"\n"+\
                "ISEGS_on"+"\t"+str(ISEGS_on)+"\n"+\
                "Cband3_on"+"\t"+str(Cband3_on)+"\n"+\
                "Cband4_on"+"\t"+str(Cband4_on)+"\n"+\
                "Cband5_on"+"\t"+str(Cband5_on)+"\n"+\
                "Cband6_on"+"\t"+str(Cband6_on)+"\n"+\
                "ISX1_on"+"\t"+str(ISX1_on)+"\n"+\
                "ISX2_on"+"\t"+str(ISX2_on)+"\n"+\
                "Xband3_on"+"\t"+str(Xband3_on)+"\n"+\
                "Xband4_on"+"\t"+str(Xband4_on)+"\n"+\
                "Xband5_on"+"\t"+str(Xband5_on)+"\n"+\
                "Xband6_on"+"\t"+str(Xband6_on)+"\n"+\
                "GFZ1_on "+"\t"+str(GFZ1_on)+"\n"+\
                "GFZ2_on "+"\t"+str(GFZ2_on)+"\n"+\
                "GFZ3_on "+"\t"+str(GFZ3_on)+"\n"+\
                "Cam4_on "+"\t"+str(Cam4_on)+"\n"+\
                "Cam5_on "+"\t"+str(Cam5_on)+"\n"+\
                "Cam6_on "+"\t"+str(Cam6_on)+"\n"+\
                "=============================================\n")
                FILE9.close()  

                FILE9b = open(out_txt+"_status9.txt", "w",encoding="utf-8", errors="surrogateescape")
                FILE9b.write("REFIR MODEL PARAMETERS 6 \n"+\
                "=================================================\n"+\
                "  >>> Sensor Settings II (Manual input channels) <<< \n"+\
                " --------------------------------------------------\n" +\
                "ISKEFm_on"+"\t"+str(ISKEFm_on)+"\n"+\
                "ISEGSm_on"+"\t"+str(ISEGSm_on)+"\n"+\
                "Cband3m_on"+"\t"+str(Cband3m_on)+"\n"+\
                "Cband4m_on"+"\t"+str(Cband4m_on)+"\n"+\
                "Cband5m_on"+"\t"+str(Cband5m_on)+"\n"+\
                "Cband6m_on"+"\t"+str(Cband6m_on)+"\n"+\
                "ISX1m_on"+"\t"+str(ISX1m_on)+"\n"+\
                "ISX2m_on"+"\t"+str(ISX2m_on)+"\n"+\
                "Xband3m_on"+"\t"+str(Xband3m_on)+"\n"+\
                "Xband4m_on"+"\t"+str(Xband4m_on)+"\n"+\
                "Xband5m_on"+"\t"+str(Xband5m_on)+"\n"+\
                "Xband6m_on"+"\t"+str(Xband6m_on)+"\n"+\
                "=============================================\n")
                FILE9b.close() 

                FILE10 = open(out_txt+"_status10.txt", "w",encoding="utf-8", errors="surrogateescape")
                FILE10.write("REFIR MODEL PARAMETERS 7 \n"+\
                "==============================================================\n"+\
                "  >>> Radar Sensor Calibration <<<        \n"+\
                "----------------------------------------------------------\n" +\
                "cal_ISKEF_a"+"\t"+str(cal_ISKEF_a)+"\n"+\
                "cal_ISKEF_b"+"\t"+str(cal_ISKEF_b)+"\n"+\
                "cal_ISEGS_a"+"\t"+str(cal_ISEGS_a)+"\n"+\
                "cal_ISEGS_b"+"\t"+str(cal_ISEGS_b)+"\n"+\
                "cal_Cband3a"+"\t"+str(cal_Cband3a)+"\n"+\
                "cal_Cband3b"+"\t"+str(cal_Cband3b)+"\n"+\
                "cal_Cband4a"+"\t"+str(cal_Cband4a)+"\n"+\
                "cal_Cband4b"+"\t"+str(cal_Cband4b)+"\n"+\
                "cal_Cband5a"+"\t"+str(cal_Cband5a)+"\n"+\
                "cal_Cband5b"+"\t"+str(cal_Cband5b)+"\n"+\
                "cal_Cband6a"+"\t"+str(cal_Cband6a)+"\n"+\
                "cal_Cband6b"+"\t"+str(cal_Cband6b)+"\n"+\
                "cal_ISX1_a"+"\t"+str(cal_ISX1_a)+"\n"+\
                "cal_ISX1_b"+"\t"+str(cal_ISX1_b)+"\n"+\
                "cal_ISX2_a"+"\t"+str(cal_ISX2_a)+"\n"+\
                "cal_ISX2_b"+"\t"+str(cal_ISX2_b)+"\n"+\
                "cal_Xband3a"+"\t"+str(cal_Xband3a)+"\n"+\
                "cal_Xband3b"+"\t"+str(cal_Xband3b)+"\n"+\
                "cal_Xband4a"+"\t"+str(cal_Xband4a)+"\n"+\
                "cal_Xband4b"+"\t"+str(cal_Xband4b)+"\n"+\
                "cal_Xband5a"+"\t"+str(cal_Xband5a)+"\n"+\
                "cal_Xband5b"+"\t"+str(cal_Xband5b)+"\n"+\
                "cal_Xband6a"+"\t"+str(cal_Xband6a)+"\n"+\
                "cal_Xband6b"+"\t"+str(cal_Xband6b)+"\n"+\
                "==============================================================\n")
                FILE10.close()  

                FILE11 = open(out_txt+"_status11.txt", "w",encoding="utf-8", errors="surrogateescape")
                FILE11.write("REFIR MODEL PARAMETERS 8 \n"+\
                "==============================================\n"+\
                "  >>> Model settings <<<        \n"+\
                "----------------------------------------------\n" +\
                "wtf_wil"+"\t"+str(wtf_wil)+"\n"+\
                "wtf_spa"+"\t"+str(wtf_spa)+"\n"+\
                "wtf_mas"+"\t"+str(wtf_mas)+"\n"+\
                "wtf_mtg"+"\t"+str(wtf_mtg)+"\n"+\
                "wtf_deg"+"\t"+str(wtf_deg)+"\n"+ \
                "wtf_wood0d" + "\t" + str(wtf_wood0d) + "\n" + \
                "ki"+"\t"+str(ki)+"\n"+\
                "timebase"+"\t"+str(timebase)+"\n"+\
                "oo_exp"+"\t"+str(oo_exp)+"\n"+\
                "oo_con"+"\t"+str(oo_con)+"\n"+\
                "wtf_exp"+"\t"+str(wtf_exp)+"\n"+\
                "wtf_con"+"\t"+str(wtf_con)+"\n"+\
                "oo_manual"+"\t"+str(oo_manual)+"\n"+\
                "wtf_manual"+"\t"+str(wtf_manual)+"\n"+\
                "min_manMER"+"\t"+str(min_manMER)+"\n"+\
                "max_manMER"+"\t"+str(max_manMER)+"\n"+\
                "oo_wood "+"\t"+str(oo_wood)+"\n"+\
                "oo_5MER "+"\t"+str(oo_5MER)+"\n"+\
                "wtf_wood "+"\t"+str(wtf_wood)+"\n"+\
                "wtf_5MER"+"\t"+str(wtf_5MER)+"\n"+\
                "oo_isound"+"\t"+str(oo_isound)+"\n"+\
                "wtf_isound"+"\t"+str(wtf_isound)+"\n"+\
                "oo_esens"+"\t"+str(oo_esens)+"\n"+\
                "wtf_esens"+"\t"+str(wtf_esens)+"\n"+\
                "oo_pulsan"+"\t"+str(oo_pulsan)+"\n"+\
                "wtf_pulsan"+"\t"+str(wtf_pulsan)+"\n"+\
                "oo_scatter"+"\t"+str(oo_scatter)+"\n"+\
                "wtf_scatter"+"\t"+str(wtf_scatter)+"\n"+\
                "analysis"+"\t"+str(analysis)+"\n"+\
                "=============================================\n")
                FILE11.close()  
                
                FILE12 = open(out_txt+"_status12.txt", "w",encoding="utf-8", errors="surrogateescape")
                FILE12.write("REFIR MODEL PARAMETERS 9 \n"+\
                "=============================================\n"+\
                "--------------output settings------------\n"+\
                "PM_Nplot" +"\t"+str(PM_Nplot)+"\n"+\
                "PM_PHplot" +"\t"+str(PM_PHplot)+"\n"+\
                "PM_MERplot"+"\t"+str(PM_MERplot)+"\n"+\
                "PM_TME  "+"\t"+str(PM_TME)+"\n"+\
                "PM_FMERplot" +"\t"+str(PM_FMERplot)+"\n"+\
                "PM_FTME"+"\t"+str(PM_FTME)+"\n"+\
                "StatusR_oo"+"\t"+str(StatusR_oo)+"\n"+\
                "--------------plume diameter------------\n"+\
                "Min_DiaOBS"+"\t"+str(Min_DiaOBS)+"\n"+\
                "Max_DiaOBS"+"\t"+str(Max_DiaOBS)+"\n"+\
                "------------------------------------------"+\
                "TIMEBASE" +"\t"+str(TIMEBASE)+"\n"+\
                "------------------------------------------\n"+\
                "Configuration file dates from: " + str(time_update)+"\n"+\
                "===============================================\n"+\
                    "FOXI vers.: "+FOXIversion+"\tcontact:_________ \n"+\
                    "operator: "+operator+"\t\t\t _____________ \n"+\
                    "\t \t \t\tphone: _____________\n"+\
                    "\t \t \t\t ___________________\n"+\
                    "\t \t \t\t _________________ \n\n")
                FILE12.close()  
            saveStatus1()
            def saveStatusReport():
                """updates status report"""
                
                time_nun = TimeNOW.strftime("%m/%d/%Y %H:%M:%S") 
                if cur_MERMAX_hmin < cur_MERavg:
                        
                    FILE3 = open(out_txt+"_STATUS_REPORT.txt", "w",encoding="utf-8", errors="surrogateescape")
                    FILE3.write("ERUPTION SOURCE PARAMETER STATUS REPORT\n"+\
                    "==========================================\n"+\
                    "- - - - - output from Refir 18.1c - - - - - \n"+\
                    scenario+"\n"+"\n"+\
                    "<<<<<<<<<<<"+str(time_nun)+">>>>>>>>>>>>\n"+\
                    "\n"+\
                    "    >>> Plume Height Stats (a.v.) <<<           \n"+\
                    "------------------------------------------\n"+\
                    "time frame:\t" +str(TIMEBASE)+" min\n"+\
                    "tracked data N:\t" +str(cur_N)+"\n"+\
                    "minimum pl.h.:\t" +str(cur_hbe_min)+" m\n"+\
                    "best e. pl.h.:\t" +str(cur_hbe)+" m\n"+\
                    "maximum pl.h.:\t" +str(cur_hbe_max)+" m\n"+\
                    "\n"+\
                    "   >>> Mass Eruption Rate Stats <<<             \n"+\
                    "------------------------------------------\n"+\
                    "abs. min MER: \t" +"{:1.2e}".format(cur_MERMIN_hmin)+" kg/s\n"+\
                    "average MER: \t" +"{:1.2e}".format(cur_MERavg)+" kg/s\n"+\
                    "abs. max MER: \t" +"{:1.2e}".format(cur_MaxMERhmax)+" kg/s\n"+\
                    "\n"+\
                    "  >>> Best Estimate of Current MER  <<<             \n"+\
                    "==========================================\n"+\
                    "lower boundary:\t" +"{:1.2e}".format(cur_MERMAX_hmin)+" kg/s\n"+\
                    "\t\t*************\n"+\
                    "best est. MER: \t" +"{:1.2e}".format(cur_MERWE)+" kg/s\n"+\
                    "\t\t*************\n"+\
                    "upper boundary:\t" +"{:1.2e}".format(cur_MERMAX_PLUS)+" kg/s\n"+\
                    "==========================================\n"+\
                    "\n"+\
                    "  >>> Computed Total Erupted Mass <<<        \n"+\
                    "------------------------------------------\n"+\
                    "lower boundary: \t" +"{:1.2e}".format(M_MIN_hmin)+" kg\n"+\
                    "best e. total mass*:\t" +"{:1.2e}".format(M_MERWE)+" kg\n"+\
                    "upper boundary*:\t" +"{:1.2e}".format(M_MAXPLUS)+" kg\n"+\
                    "--------------------------------------------------------------\n"+\
                    "\n"+\
                    "==============================================================\n"+\
                    "*Note: Mass integrated only over monitored time period, \n"+\
                    " thus displayed numbers might be underestimates!\n"+\
                    "\n"+\
                    "CAUTION !! \n"+\
                    "All values presented are automatically generated \n"+\
                    "\t >> PRELIMINARY RESULTS << \n"\
                    +"and need to be confirmed by authorized staff!\n"
                    "==============================================================\n"+\
                    "FOXI vers.: "+FOXIversion+"\tcontact:Tobi Duerig \n"+\
                    "operator: "+operator+"\t\t\ttobi@hi.is \n"+\
                    "\t \t \t\tphone: +354 7838609\n"+\
                    "\t \t \t\tInstitute of Earth Sciences\n"
                    "\t \t \t\tUniversity of Iceland\n"
                    "\n")
                    FILE3.close()
                  
                else:
                                        
                    FILE3 = open(out_txt+"_STATUS_REPORT.txt", "w",encoding="utf-8", errors="surrogateescape")
                    FILE3.write("ERUPTION SOURCE PARAMETER STATUS REPORT\n"+\
                    "==========================================\n"+\
                    "- - - - - output from Refir 18.1c - - - - - \n"+\
                    scenario+"\n"+"\n"+\
                    "<<<<<<<<<<<"+str(time_nun)+">>>>>>>>>>>>\n"+\
                    "\n"+\
                    "    >>> Plume Height Stats (a.v.)<<<             \n"+\
                    "------------------------------------------\n"+\
                    "time frame:\t" +str(TIMEBASE)+" min\n"+\
                    "tracked data N:\t" +str(cur_N)+"\n"+\
                    "minimum pl.h.:\t" +str(cur_hbe_min)+" m\n"+\
                    "best e. pl.h.:\t" +str(cur_hbe)+" m\n"+\
                    "maximum pl.h.:\t" +str(cur_hbe_max)+" m\n"+\
                    "\n"+\
                    "   >>> Mass Eruption Rate Stats <<<             \n"+\
                    "------------------------------------------\n"+\
                    "abs. min MER: \t" +"{:1.2e}".format(cur_MERMIN_hmin)+" kg/s\n"+\
                    "average MER: \t" +"{:1.2e}".format(cur_MERavg)+" kg/s\n"+\
                    "abs. max MER: \t" +"{:1.2e}".format(cur_MaxMERhmax)+" kg/s\n"+\
                    "\n"+\
                    "  >>> Best Estimate of Current MER  <<<             \n"+\
                    "==========================================\n"+\
                    "lower boundary:\t" +"{:1.2e}".format(MERmaxNowiHmin)+" kg/s\n"+\
                    "\t\t*************\n"+\
                    "best est. MER: \t" +"{:1.2e}".format(cur_MERWE)+" kg/s\n"+\
                    "\t\t*************\n"+\
                    "upper boundary:\t" +"{:1.2e}".format(cur_MERMAX_PLUS)+" kg/s\n"+\
                    "==========================================\n"+\
                    "\n"+\
                    "  >>> Computed Total Erupted Mass <<<        \n"+\
                    "------------------------------------------\n"+\
                    "lower boundary: \t" +"{:1.2e}".format(M_MIN_hmin)+" kg\n"+\
                    "best e. total mass*:\t" +"{:1.2e}".format(M_MERWE)+" kg\n"+\
                    "upper boundary*:\t" +"{:1.2e}".format(M_MAXPLUS)+" kg\n"+\
                    "--------------------------------------------------------------\n"+\
                    "\n"+\
                    "==============================================================\n"+\
                    "*Note: Mass integrated only over monitored time period, \n"+\
                    " thus displayed numbers might be underestimates!\n"+\
                    "\n"+\
                    "CAUTION !! \n"+\
                    "All values presented are automatically generated \n"+\
                    "\t >> PRELIMINARY RESULTS << \n"\
                    +"and need to be confirmed by authorized staff!\n"
                    "==============================================================\n"+\
                    "FOXI vers.: "+FOXIversion+"\tcontact:Tobi Duerig \n"+\
                    "operator: "+operator+"\t\t\ttobi@hi.is \n"+\
                    "\t \t \t\tphone: +354 7838609\n"+\
                    "\t \t \t\tInstitute of Earth Sciences\n"
                    "\t \t \t\tUniversity of Iceland\n"
                    "\n")
                    FILE3.close()
            if StatusR_oo == 0:
                 logger9.info("status report: switched OFF!")
            else:
                saveStatusReport()       
                logger9.info(".........status report updated!")
            
        logger9.info("***** step 9 successful *****")
    mpl.pyplot.close("all") 
    logger10.info(":::::::::::::::::::::::::::::::::::::::::::::::::")
    logger10.info("SYSTEM UPDATE:")
    logger10.info("\n run No. " + str(run)+" successful\n")
    logger10.info("ALL CLEAR!")
    logger10.info(".......................")
    logger10.info(".......................")
    logger10.info("waiting for new run....")
    logger10.debug("******************************************************")
    """global Cband1_stack,Cband2_stack,Cband3_stack,Cband4_stack,Cband5_stack,Cband6_stack
    global Xband1_stack,Xband2_stack,Xband3_stack,Xband4_stack,Xband5_stack,Xband6_stack
    global Cam1_stack,Cam2_stack,Cam3_stack,Cam4_stack,Cam5_stack,Cam6_stack,air_stack,ground_stack,other_stack
    global Cband1_t_stack,Cband2_t_stack,Cband3_t_stack,Cband4_t_stack,Cband5_t_stack,Cband6_t_stack
    global Xband1_t_stack,Xband2_t_stack,Xband3_t_stack,Xband4_t_stack,Xband5_t_stack,Xband6_t_stack
    global Cam1_t_stack,Cam2_t_stack,Cam3_t_stack,Cam4_t_stack,Cam5_t_stack,Cam6_t_stack,air_t_stack,ground_t_stack,other_t_stack"""
    Cband1_stack,Cband2_stack,Cband3_stack,Cband4_stack,Cband5_stack,Cband6_stack = [],[],[],[],[],[]
    Xband1_stack,Xband2_stack,Xband3_stack,Xband4_stack,Xband5_stack,Xband6_stack = [],[],[],[],[],[]
    Cam1_stack,Cam2_stack,Cam3_stack,Cam4_stack,Cam5_stack,Cam6_stack,air_stack,ground_stack,other_stack = [],[],[],[],[],[],[],[],[]
    Cband1_t_stack,Cband2_t_stack,Cband3_t_stack,Cband4_t_stack,Cband5_t_stack,Cband6_t_stack = [],[],[],[],[],[]
    Xband1_t_stack,Xband2_t_stack,Xband3_t_stack,Xband4_t_stack,Xband5_t_stack,Xband6_t_stack = [],[],[],[],[],[]
    Cam1_t_stack,Cam2_t_stack,Cam3_t_stack,Cam4_t_stack,Cam5_t_stack,Cam6_t_stack,air_t_stack,ground_t_stack,other_t_stack= [],[],[],[],[],[],[],[],[]
    def waitingProc():
        # Check if the stop signal from FIX
        configfile = open("fix_config.txt", "r",encoding="utf-8", errors="surrogateescape")
        configlines = configfile.readlines()
        configfile.close()
        exit_param = int(configlines[168])
        if exit_param == 1:
            refir_end()

        time.sleep(27)#adjust so that with time of run a resulting time of 300s is obtained
        waittime = int(270-verz)
        print ("...next run in "+str(waittime)+" seconds")
        waittime1 = waittime%30
        waittime2 = int(waittime - waittime1)
        time.sleep(waittime1)
        for i in range(waittime2,30,-30):
            # Check the stop signal from FIX
            configfile = open("fix_config.txt", "r", encoding="utf-8", errors="surrogateescape")
            configlines = configfile.readlines()
            configfile.close()
            exit_param = int(configlines[168])
            if exit_param == 1:
                refir_end()

            time.sleep(30)
            print ("...next run in "+str(i)+" seconds")
        print(".....")
        time.sleep(18)
        print("Caution! New run in prepare!")
        #winsound.Beep(Freq,Dur2)
        for ai in range(10,0,-1):
            time.sleep(1)
            #winsound.Beep(Freq,Dur)
            print (str(ai)+" seconds")
        #winsound.Beep(Freq,Dur2)

    del gc.garbage[:]
    gc.collect()
    logger.debug('gc garbage: %r', gc.garbage)
    logger.manager.loggerDict.clear()
    logger1.manager.loggerDict.clear()
    logger2.manager.loggerDict.clear()
    logger3.manager.loggerDict.clear()
    logger4.manager.loggerDict.clear()
    logger5.manager.loggerDict.clear()
    logger6.manager.loggerDict.clear()
    logger7.manager.loggerDict.clear()
    logger8.manager.loggerDict.clear()
    logger9.manager.loggerDict.clear()
    logger10.manager.loggerDict.clear()

    TimeOLD = TimeNOW
    if run_type == 1:
        waitingProc()
    else:
        continue