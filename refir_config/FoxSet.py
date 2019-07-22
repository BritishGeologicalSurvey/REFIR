"""
*** FoxSet v19.0 ***                                                                          
- component of REFIR 19.0 -
-Program to                                         set up the instruments for REFIR -
 
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
#tested on 02/05/17

# IMPORTANT NOTE: when working with Windows 7+ and Python 2.7: replace input with raw_input

from __future__ import division
from __future__ import with_statement
from builtins import input
from math import radians, cos, sin, asin, sqrt
import future
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
import math
from copy import deepcopy
import sys
import time
from ftplib import FTP
#import winsound
import locale
from future.standard_library import install_aliases
install_aliases()
import urllib.request
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import os,glob


sm = 0
za = 0
N_sens =[0,0,0]

ID = ["n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a."]
LatS = ["","","","","","","","","","","","","","","","","",""]
LonS = ["","","","","","","","","","","","","","","","","",""]
TypS =["","","","","","","","","","","","","","","","","",""]
FocS =["","","","","","","","","","","","","","","","","",""]
VolcID = ["n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a."]
LatV = ["","","","","","","","","",""]
LonV = ["","","","","","","","","",""]
VolcH= ["","","","","","","","","",""]
DBline =["","","","","","","","","","","","","","","","","","","","","",""]
N_Volc = 0
ID0 = ["n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a.","n.a."]
volc_exist=0
N_en,N_en1,N_en2=0,0,0

def read_sensors0():
    """reads IDs from *.ini files"""
    global ID0,N_en,N_en1,N_en2,volc_exist
    try:
        fn='volcano_list.ini'
        with open (fn,encoding="utf-8", errors="surrogateescape") as f:
                lines =f.readlines()
        f.close()
        #file exists   
        volc_exist=1
    except  EnvironmentError:
        #file does not exist yet
        volc_exist=0

    try:          
        #C-band
        fnCb= 'Cband.ini'
        with open (fnCb,encoding="utf-8", errors="surrogateescape") as f:
            lines =f.readlines()
            Cse = []
            for l in lines:
               Cse.append(l.strip().split("\t"))
        f.close()
        N_en = len(Cse)-1 #number of entries
        print(">>> "+str(N_en))
        if N_en < 1:
            print("\nNo C-band radar sensors assigned yet...\n")
        else:
            for x in range(0,N_en):
                    ID0[x] = str(Cse[x+1][0])
                    
               
    except  EnvironmentError:
        print("No Cband radar sensors assigned yet...\n")

    try:
        #X-band
        fnXb= 'Xband.ini'
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
                    ID0[x+6] = str(Dse[x+1][0])

    except  EnvironmentError:
        print("No Xband radar sensors assigned yet...\n")
    try:
        #Cams
        fnCam= 'Cam.ini'
        with open (fnCam,encoding="utf-8", errors="surrogateescape") as f:
            lines =f.readlines()
            Ase = []
            for l in lines:
               Ase.append(l.strip().split("\t"))
        f.close()
        N_en1 = len(Ase)-1 #number of entries
        if N_en1 < 1:
            print("\nNo webcams assigned yet...\n")
        else:
            for x in range(0,N_en1):
                    ID0[x+12] = str(Ase[x+1][0])

    except  EnvironmentError:
        print("No .ini files assigned yet...\n")

read_sensors0() #ID0: array with sensor IDs [0-5]:Cband, [6-11]:Xband, [12-17]Cam

a=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for i in range(0,18):
    if ID0[i]=="n.a.":
        a[i]=0
    else:
        a[i]=1

def create_volcheader():
    if volc_exist==0:
        FILE1 = open("volcano_list.ini", "w",encoding="utf-8", errors="surrogateescape")
        FILE1.write("ID" +"\t"+"Lat"+"\t"+"Lon"+"\t"+"hvent/m"+"\t"+"default"+"\t"+"full name""\n")
        FILE1.close()
    else:
        yu=0

def volcentry(volc):
    FILE1 = open("volcano_list.ini", "a",encoding="utf-8", errors="surrogateescape")
    FILE1.write(str(volc[0]) +"\t"+str(volc[1]) +"\t"+str(volc[2]) +"\t"+str(volc[3]) +"\t"+str(volc[4]) +"\t"+str(volc[5]) +"\n")
    FILE1.close()

def icelandvolc_default():
    global volc_exist
    print("... setting up default Iceland volcanoes!")
    volc_exist=0
    create_volcheader()
    volc = ["372020",63.6283,-19.625, 1666,1,"Eyjafjallajökull"]
    volcentry(volc)
    volc = ["372030",63.633,-19.116, 1512,1,"Katla"]
    volcentry(volc)
    volc = ["372070",63.992,-19.667, 1491,1,"Hekla"]
    volcentry(volc)
    volc = ["373010",64.417,-17.333, 1725,1,"Grímsvötn"]
    volcentry(volc)
    volc = ["372010",63.417,-20.35, 279,1,"Vestmannaeyjar"]
    volcentry(volc)
    volc = ["373030",64.667,-17.5, 2009,1,"Bárðarbunga"]
    volcentry(volc)
    volc = ["373050",64.65,-16.667, 1929,1,"Kverkfjöll"]
    volcentry(volc)
    volc = ["374010",64.00,-16.65, 2119,1,"Öræfajökull"]
    volcentry(volc)
    volc = ["373060",65.05,-16.783, 1516,1,"Askja"]
    volcentry(volc)
    volc = ["ovaent",65.00,-17.00, 99,1,"Óvæntfjöll"]
    volcentry(volc)
    N_volc = 10
    print("\nDefault Icelandic volcano list was generated!")
    print("Check in file \"volcano_list.ini\" if all data are correct and modify accordingly!")
    #raw_input("\n....confirm by any key! ")
    name = input('\n....confirm by any key! ')
    assert isinstance(name, str)    # native str on Py2 and Py3

def newvolc_setup():
    import pandas as pd
    import numpy as np
    from pandas import ExcelFile
    global volc_exist
    volc_exist = 0
    print("... setting up volcanoes of interest!")
    print("Up to 10 volcanoes can be added to the list")
    df = pd.read_excel('SI_volcanoes_list.xlsx', sheetname='volcanoes')
    nrow = df.shape[0]
    i = 0
    z = 0
    global volc, N_volc
    volc=[0,0,0,0,0,""]
    vrun = 0
    create_volcheader()
    while z!=2 :
        lencheck = 0
        vrun = vrun + 1
        print("----------------")
        print("Volcano No. "+ str(vrun)+": \n")
        # volc[5] = input("Name of volcano .. ")
        # assert isinstance(volc[5], str)
        volc[0] = input("Specify Smithsonian Institute ID for the volcano: ")
        row=0
        while True:
            volc[4] = 0
            if df['SMITHSONIAN_ID'][row] == np.int64(volc[0]):
            #if df['VOLCANO_ID'][row] == volc[0]:
                volc[1] = df['LATITUDE'][row]
                volc[2] = df['LONGITUDE'][row]
                volc[3] = df['ELEVATION_m'][row]
                volc[5] = df['VOLCANO_NAME'][row]
                volcentry(volc)
                break
            else:
                row += 1
                if row >= nrow:
                    print('ID not found')
                    break

        print("Data saved!")
        print("-------------")
        if vrun == 10:
            N_volc = 10
            print ("\nList completed!")
            print("Check in file \"volcano_list.ini\" if all data are correct and modify accordingly!")
            #raw_input("\n....confirm by any key! ")
            name = input('\n....confirm by any key! ')
            assert isinstance(name, str)    # native str on Py2 and Py3            
        else:
            print("\nWant to add another volcano of interest?")
            print("[1]: yes")
            print("[2]: no")
            another = input(".. ")
            an = int (another)
            if an == 1:
                z = 0
            else:
                z = 2
                N_volc = vrun
                print ("\nList completed!")
                print("Check in file \"volcano_list.ini\" if all data are correct and modify accordingly!")
                #raw_input("\n....confirm by any key! ")
                name = input('\n....confirm by any key! ')
                assert isinstance(name, str)    # native str on Py2 and Py3                     

def create_sensorheadersC():
    
    FILE1 = open("Cband.ini", "w",encoding="utf-8", errors="surrogateescape")
    FILE1.write("ID" +"\t"+"lat"+"\t"+"lon"+"\t"+"type"+"\t"+"focus"+"\t"+"bwidth"+"\t"+"file"+"\t"+"www"+"\t"+"IP"+"\t"+"directory"+"\n")
    FILE1.close()

def create_sensorheadersX():
    FILE1 = open("Xband.ini", "w")
    FILE1.write("ID" +"\t"+"lat"+"\t"+"lon"+"\t"+"type"+"\t"+"focus"+"\t"+"bewidth"+"\t"+"file"+"\t"+"www"+"\t"+"IP"+"\t"+"directory"+"\n")
    FILE1.close()

def create_sensorheadersCam():
    FILE1 = open("Cam.ini", "w",encoding="utf-8", errors="surrogateescape")
    FILE1.write("ID" +"\t"+"lat"+"\t"+"lon"+"\t"+"type"+"\t"+"focus"+"\t"+"bwidth"+"\t"+"file"+"\t"+"www"+"\t"+"IP"+"\t"+"directory"+"\n")
    FILE1.close()

def create_sensorheaders():
    create_sensorheadersC()
    create_sensorheadersX()
    create_sensorheadersCam()

def C_entry(sens):
    FILE1 = open("Cband.ini", "a",encoding="utf-8", errors="surrogateescape")
    FILE1.write(str(sens[0]) +"\t"+str(sens[1]) +"\t"+str(sens[2]) +"\t"+str(sens[3]) +"\t"+str(sens[4]) +"\t"+str(sens[5]) +"\t"+str(sens[6]) +"\t"+str(sens[7]) +"\t"+str(sens[8])+"\t"+str(sens[9])+"\n")
    FILE1.close()

def X_entry(sens):
    FILE1 = open("Xband.ini", "a",encoding="utf-8", errors="surrogateescape")
    FILE1.write(str(sens[0]) +"\t"+str(sens[1]) +"\t"+str(sens[2]) +"\t"+str(sens[3]) +"\t"+str(sens[4]) +"\t"+str(sens[5])+"\t"+str(sens[6]) +"\t"+str(sens[7]) +"\t"+str(sens[8]) +"\t"+str(sens[9]) +"\n")
    FILE1.close()

def Cam_entry(sens):
    FILE1 = open("Cam.ini", "a",encoding="utf-8", errors="surrogateescape")
    FILE1.write(str(sens[0]) +"\t"+str(sens[1]) +"\t"+str(sens[2]) +"\t"+str(sens[3]) +"\t"+str(sens[4]) +"\t"+str(sens[5])+"\t"+str(sens[6]) +"\t"+str(sens[7]) +"\t"+str(sens[8]) +"\t"+str(sens[9])+"\n")
    FILE1.close()

def latest_xradar_location():
    global lat_isx1,lon_isx1,lat_isx2,lon_isx2
    content = urllib.request.urlopen("http://brunnur.vedur.is/radar/status/")
    nlines = 0
    radars_status = []
    readable_lines = []
    for line in content:
        nlines += 1
        radars_status.append(line.decode("utf-8"))
        readable_lines.append(radars_status[nlines - 1].split(" "))
        try:
            if readable_lines[nlines - 1][1] == "isx1":
                lat_isx1 = float(readable_lines[nlines - 1][5])
                lon_isx1 = float(readable_lines[nlines - 1][6])
            elif readable_lines[nlines - 1][1] == "isx2":
                lat_isx2 = float(readable_lines[nlines - 1][5])
                lon_isx2 = float(readable_lines[nlines - 1][6])
                break
        except:
            continue

def icelandsensors_default():
    global N_sens
    latest_xradar_location()
    print("... setting up default Iceland sensors!")
    create_sensorheaders()
    sens = ["ISKEF",64.026383,-22.635833,1,99,0.9,"radar_iskef","http://brunnur.vedur.is/radar/vespa","",""]
    C_entry(sens)
    sens = ["ISEGS",65.027944,-15.038186,1,99,1.0,"radar_isegs","http://brunnur.vedur.is/radar/vespa","",""]
    C_entry(sens)
    sens = ["ISX1",lat_isx1,lon_isx1,2,99,1.25,"radar_isx1","http://brunnur.vedur.is/radar/vespa","",""]
    X_entry(sens)
    sens = ["ISX2",lat_isx2,lon_isx2,2,99,1.25,"radar_isx2","http://brunnur.vedur.is/radar/vespa","",""]
    X_entry(sens)
    sens = ["CAM1",64.09,-19.83,3,2,99,"gfzcam1","","199.204.44.194","/pub/linux/kernel"]
    Cam_entry(sens)    
    sens = ["CAM2",64.03,-19.56,3,2,99,"gfzcam2","","199.204.44.194","/pub/linux/kernel"]
    Cam_entry(sens)  
    sens = ["CAM3",63.93,-19.67,3,2,99,"gfzcam3","","199.204.44.194","/pub/linux/kernel"]
    Cam_entry(sens)        
    N_sens = [2,2,3]
    print("\n***Default Icelandic sensor lists were generated!***")
    print("Check in .ini files if all data are correct and modify accordingly!")
    #raw_input("\n....confirm by any key! ")
    name = input('\n....confirm by any key! ')
    assert isinstance(name, str)    # native str on Py2 and Py3
    generate_volc_database()

def Cband_new():
    crun = 0
    print("... setting up C-band radar stations!")
    print("Up to 6 sensors can be added")
    z = 0
    slots_full=0
    global N_sens
    sens=["",0,0,0,0,0,"","","",""]
    if a[0]==0:
        create_sensorheadersC()
    else:
        if a[1]==0:
            crun=1
        else:
            if a[2]==0:
                crun=2
            else:
                if a[3]==0:
                    crun=3
                else:        
                    if a[4]==0:
                        crun=4
                    else:
                        crun=5
                        slots_full=1
    if slots_full==1:
        print("Already 6 sensors assigned!\n Erase entry before adding new sensor!")
    else:                           
        while z!=2 :
            lencheck = 0
            crun = crun + 1
            print("----------------")
            print("C-Band radar no. "+ str(crun)+": \n")
            while lencheck!=1:
                sens[0]= input("Specify code for sensor (6 characters max!): ")
                assert isinstance(sens[0], str)
                if len(sens[0]) <7:
                    lencheck = 1
                else:
                    print("Maximum of 6 characters, please!") 
                    lencheck = 0
            lat = input("Specify Latitude (e.g. 63.3) .. ")
            sens[1] = float(lat)
            lon = input("Specify Longitude (e.g. -17.5) .. " )
            sens[2] = float(lon)
            sens[3] = 1
            sens[4] = 99 
            sens[5] = input("Specify beam width (in °, e.g. 1.0) .. " )
                
            sens[6]= input("Specify file name (e.g. \"radar_iskef\") ")
            assert isinstance(sens[6], str)
            sens[7]= input("Specify url (e.g. \"www.uni.hi.is/test\")!\n[z] if not applicable!\n")
            assert isinstance(sens[7], str)
            if sens[7] =="z":
                sens[7]=""
                sens[8]= input("Specify IP address of FTP server (e.g. \"143.143.120.0\") \n")
                assert isinstance(sens[8], str)
                sens[9]= input("Specify directory on FTP server (e.g. \"/pub/linux/kernel\") \n")
                assert isinstance(sens[9], str)
            else:
                sens[8]=""
                sens[9]=""
            C_entry(sens)
            print("data saved!")
            print("-------------")
            if crun == 6:
                N_sens[0] = 6
                print ("\nlist completed!")
                print("Check in file \"Cband.ini\" if all data are correct and modify accordingly!")
                name = input('\n....confirm by any key! ')
                assert isinstance(name, str)    # native str on Py2 and Py3            
            else:
                print("Want to add another C-band radar station?")
                print("[1]: yes")
                print("[2]: no")
                another = input(".. ")
                an = int(another)
                if an == 1:
                    z = 0
                else:
                    z = 2
                    N_sens[0] = crun
                    print ("\nlist completed!")
                    print("Check in file \"Cband.ini\" if all data are correct and modify accordingly!")
                    name = input('\n....confirm by any key! ')
                    assert isinstance(name, str)    # native str on Py2 and Py3 
    
def Xband_new():
    crun = 0
    print("... setting up X-band radar stations!")
    print("Up to 6 sensors can be added")
    z = 0
    slots_full = 0
    global N_sens
    sens=["",0,0,0,0,0,"","","",""]
    if a[6]==0:
        create_sensorheadersX()
    else:
        if a[7]==0:
            crun=1
        else:
            if a[8]==0:
                crun=2
            else:
                if a[9]==0:
                    crun=3
                else:        
                    if a[10]==0:
                        crun=4
                    else:
                        crun=5
                        slots_full=1
    if slots_full==1:
        print("Already 6 sensors assigned!\n Erase entry before adding new sensor!")
    else:                           
        while z!=2 :
            lencheck = 0
            crun = crun + 1
            print("----------------")
            print("X-Band radar no. "+ str(crun)+": \n")
            while lencheck!=1:
                sens[0]= input("Specify code for sensor (6 characters max!): ")
                assert isinstance(sens[0], str)
                if len(sens[0]) <7:
                    lencheck = 1
                else:
                    print("Maximum of 6 characters, please!") 
                    lencheck = 0
            lat = input("Specify Latitude (e.g. 63.3) .. ")
            sens[1] = float(lat)
            lon = input("Specify Longitude (e.g. -17.5) .. ")
            sens[2] = float(lon)
            sens[3] = 2
            sens[4] = 99  
            sens[5] = input("Specify beam width in °, e.g. 1.0) .. " )
            sens[6]= input("Specify file name (e.g. \"radar_isx1\") \n")
            assert isinstance(sens[6], str)
            sens[7]= input("Specify url (e.g. \"www.uni.hi.is/test\")!\n[z] if not applicable!\n")
            assert isinstance(sens[7], str)
            if sens[7] =="z":
                sens[7]=""
                sens[8]= input("Specify IP address of FTP server (e.g. \"143.143.120.0\")\n")
                assert isinstance(sens[8], str)
                sens[9]= input("Specify directory on FTP server (e.g. \"/pub/linux/kernel\")\n")
                assert isinstance(sens[9], str)
            else:
                sens[8]=""
                sens[9]=""
            X_entry(sens)
            print("data saved!")
            print("-------------")
            if crun == 6:
                N_sens[1] = 6
                print ("list completed!")
                print("Check in file \"Xband.ini\" if all data are correct and modify accordingly!")
                name = input('\n....confirm by any key! ')
                assert isinstance(name, str)    # native str on Py2 and Py3            
            else:
                print("Want to add another X-band radar station?")
                print("[1]: yes")
                print("[2]: no")
                another = input(".. ")
                an = int(another)
                if an == 1:
                    z = 0
                else:
                    z = 2
                    N_sens[1] = crun
                    print ("\nList completed!")
                    print("Check in file \"Xband.ini\" if all data are correct and modify accordingly!")
                    name = input('\n....confirm by any key! ')
                    assert isinstance(name, str)    # native str on Py2 and Py3     

def Cam_new():
    crun = 0
    print("... setting up plume auto-tracking webcams!")
    print("Up to 6 cameras can be added")
    z = 0
    slots_full = 0
    global N_sens
    sens=["",0,0,0,0,0,"","","",""]
    if a[12]==0:
        create_sensorheadersCam()
    else:
        if a[13]==0:
            crun=1
        else:
            if a[14]==0:
                crun=2
            else:
                if a[15]==0:
                    crun=3
                else:        
                    if a[16]==0:
                        crun=4
                    else:
                        crun=5
                        slots_full=1
    if slots_full==1:
        print("Already 6 sensors assigned!\n Erase entry before adding new sensor!")
    else: 
        while z!=2 :
            lencheck = 0
            crun = crun + 1
            print("----------------")
            print("Camera no. "+ str(crun)+": \n")
            while lencheck!=1:
                sens[0]= input("Specify ID code for camera (6 characters max!): ")
                assert isinstance(sens[0], str)
                if len(sens[0]) <7:
                    lencheck = 1
                else:
                    print("Maximum of 6 characters, please!") 
                    lencheck = 0
            lat = input("Specify Latitude (e.g. 63.3) .. ")
            sens[1] = float(lat)
            lon = input("Specify Longitude (e.g. -17.5) .. ")
            sens[2] = float(lon)
            sens[3] = 3
            try:
                fn='volcano_list.ini'
                with open (fn,encoding="utf-8", errors="surrogateescape") as f:
                    lines =f.readlines()
                    vulk = []
                    for l in lines:
                        vulk.append(l.strip().split("\t"))
                f.close()
            except EnvironmentError: 
                print("No volcano defined!")
                init_setup()
            
            print("On which volcano is this camera focussed?")
            N_volc = len(vulk)-1
            for x in range(0,N_volc):
                print("["+str(x)+"]: "+ str(vulk[x+1][5]))          
            sens[4] = input("... ")
            sens[5] = 99
            sens[6]= input("Specify file name (e.g. \"cam1\") \n")
            assert isinstance(sens[6], str)
            sens[7]= input("Specify url (e.g. \"www.uni.hi.is/test\")!\n[z] if not applicable!\n")
            assert isinstance(sens[7], str)
            if sens[7] =="z":
                sens[7]=""
                sens[8]= input("Specify IP address of FTP server (e.g. \"143.143.120.0\")\n")
                assert isinstance(sens[8], str)
                sens[9]= input("Specify directory on FTP server (e.g. \"/pub/linux/kernel\")\n")
                assert isinstance(sens[9], str)
            else:
                sens[8]=" "
                sens[9]=" "
            Cam_entry(sens)
            print("data saved!")
            print("-------------")
            if crun == 6:
                N_sens[1] = 6
                print ("list completed!")
                print("Check in file \"Cam.ini\" if all data are correct and modify accordingly!")
                name = input('\n....confirm by any key! ')
                assert isinstance(name, str)    # native str on Py2 and Py3            
            else:
                print("Want to add another plume auto-tracking webcam?")
                print("[1]: yes")
                print("[2]: no")
                another = input(".. ")
                an = int(another)
                if an == 1:
                    z = 0
                else:
                    z = 2
                    N_sens[1] = crun
                    print ("List completed!")
                    print("Check in file \"Cam.ini\" if all data are correct and modify accordingly!")
                    name = input('\n....confirm by any key! ')
                    assert isinstance(name, str)    # native str on Py2 and Py3

def newsensors_setup_menu():
    global sm
    try:
        fn='Cband.ini'
        with open (fn,encoding="utf-8", errors="surrogateescape") as f:
                lines =f.readlines()
        f.close()
        #file exists   
    except  EnvironmentError:
        #file does not exist yet
        create_sensorheadersC()
        
    try:
        fn='Xband.ini'
        with open (fn,encoding="utf-8", errors="surrogateescape") as f:
                lines =f.readlines()
        f.close()
        #file exists    
    except  EnvironmentError:
        #file does not exist yet
        create_sensorheadersX()
    
    try:
        fn='Cam.ini'
        with open (fn,encoding="utf-8", errors="surrogateescape") as f:
                lines =f.readlines()
        f.close()
        #file exists    
    except  EnvironmentError:
        #file does not exist yet
        create_sensorheadersCam()    
    print("[1] C-band (horizontally scanning) RADAR")
    print("[3] X-band (vertically scanning) RADAR")
    print("[5] Auto-tracking web-cameras")
    print("[0] Continue")
    ib = input('... ')
    assert isinstance(ib, str)    # native str on Py2 and Py3
    ib = int(ib)
    if ib ==1:
        Cband_new()
        sm = 1
    elif ib ==3:
        Xband_new()
        sm = 3
    elif ib ==5:
        Cam_new()
        sm = 5
    else:
        sm = 9

def newsensors_setup():
    global sm
    while sm != 9:
        newsensors_setup_menu()
    print("Sensor setup finished!\n")
    generate_volc_database()

def sensors_setup():
    """Initiates setup procedures for sensors and creates sensors.ini files"""
    print("\n>>STEP2: Setting up auto-stream plume height SENSORS")
    print("[1] Default Icelandic sensor setup")
    print("[3] New setup of sensors/ Add new sensor")
    print("[5] Sensors already defined - skip and continue with STEP3")
    print("[0] Quit without changes")
    ib = input('... ')
    assert isinstance(ib, str)    # native str on Py2 and Py3
    ic = int(ib)
    if ic ==1:
        icelandsensors_default()
    elif ic ==3:
        newsensors_setup()    
    elif ic ==5:
        generate_volc_database()
    else:
        print()
        sys.exit()

def init_setup():
    global za
    print("\n>>STEP1: Defining the VOLCANOES of interest\n")
    print("[1] Default Icelandic setup")
    print("[3] New setup")
    print("[5] Volcanoes already defined - move on to setup sensors (STEP2)")
    print("[7] Volcanoes and sensors already defined - move on to STEP3")
    print("[0] Quit without change")
    ia = input("... ") 
    assert isinstance(ia, str)    # native str on Py2 and Py3
    ia = int(ia)
    if ia ==1:
        icelandvolc_default()
        sensors_setup()
        za = 1
    elif ia ==3:
        try:
            ini_files = os.listdir('.')
            for item in ini_files:
                if item.endswith('.ini'):
                    os.remove(item)
        except:
            print('No .ini files from a previous configuration found')
        newvolc_setup()
        sensors_setup()
        za = 1
    elif ia ==5:
        sensors_setup()
        za = 1
    elif ia == 7:
        generate_volc_database()
        za = 1
    elif ia == 0:
        print("Skipped!\n")
        za = 1
        sys.exit()
        
    else:
        print()        

def read_volcanoes():
    """reads IDs and GPS coordinates from volcano_list.ini file"""
    global VolcID,LatV,LonV,VolcH,N_Volc
    fn='volcano_list.ini'
    try:
        with open (fn,encoding="utf-8", errors="surrogateescape") as f:
            lines =f.readlines()
            vulk = []
            for l in lines:
               vulk.append(l.strip().split("\t"))
        f.close()
        N_et = len(vulk)-1 #number of entries
        for x in range(0,N_et):
                VolcID[x] = str(vulk[x+1][0])
                LatV[x] = float(vulk[x+1][1])
                LonV[x] = float(vulk[x+1][2])
                VolcH[x] = int(float(vulk[x+1][3]))            
        N_Volc = N_et
    except  EnvironmentError:
        print("Error - File \"volcano_list.ini\" not found!\n")
        sys.exit()

def read_sensors():
    """reads IDs and GPS coordinates from *.ini files"""
    global ID,LatS,LonS,TypS,FocS
    try:
        #C-band
        with open ("Cband.ini",encoding="utf-8", errors="surrogateescape") as f:
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
                    LatS[x] = float(Cse[x+1][1])
                    LonS[x] = float(Cse[x+1][2])
                    TypS[x] = int(Cse[x+1][3])            
                    FocS[x] = int(Cse[x+1][4])
        #X-band
        with open ("Xband.ini",encoding="utf-8", errors="surrogateescape") as f:
            lines =f.readlines()
            Cse = []
            for l in lines:
               Cse.append(l.strip().split("\t"))
        f.close()
        N_en = len(Cse)-1 #number of entries
        if N_en < 1:
            print("\nNo X-band radar sensors assigned!\n")
        else:
            for x in range(0,N_en):
                    ID[x+6] = str(Cse[x+1][0])
                    LatS[x+6] = float(Cse[x+1][1])
                    LonS[x+6] = float(Cse[x+1][2])
                    TypS[x+6] = int(Cse[x+1][3])            
                    FocS[x+6] = int(Cse[x+1][4])
        #Cams
        with open ("Cam.ini",encoding="utf-8", errors="surrogateescape") as f:
            lines =f.readlines()
            Cse = []
            for l in lines:
               Cse.append(l.strip().split("\t"))
        f.close()
        N_en = len(Cse)-1 #number of entries
        if N_en < 1:
            print("\nNo webcams assigned!\n")
        else:
            for x in range(0,N_en):
                    ID[x+12] = str(Cse[x+1][0])
                    LatS[x+12] = float(Cse[x+1][1])
                    LonS[x+12] = float(Cse[x+1][2])
                    TypS[x+12] = int(Cse[x+1][3])            
                    FocS[x+12] = int(Cse[x+1][4])            
    except  EnvironmentError:
        print("Warning - \".ini\" sensor file not found!\n")
        #sys.exit()

def create_vdbheader():
    """generates header of volc_database.ini file"""
    FILE1 = open("volc_database.ini", "w",encoding="utf-8", errors="surrogateescape")
    FILE1.write("Note: This data base was automatically generated by FoxSet!\n")
    FILE1.write("ID"+"\t"+"Lat"+"\t"+"Lon"+"\t"+"hvent/m"+"\t")
    FILE1.write(str(ID[0])+"\t"+str(ID[1])+"\t"+str(ID[2])+"\t"+str(ID[3])+"\t"+str(ID[4])+"\t"+str(ID[5])+"\t")
    FILE1.write(str(ID[6])+"\t"+str(ID[7])+"\t"+str(ID[8])+"\t"+str(ID[9])+"\t"+str(ID[10])+"\t"+str(ID[11])+"\t")
    FILE1.write(str(ID[12])+"\t"+str(ID[13])+"\t"+str(ID[14])+"\t"+str(ID[15])+"\t"+str(ID[16])+"\t"+str(ID[17])+"\n")
    FILE1.close()

def create_vdbline(dbline):
    """generates line within volc_database.ini file"""
    FILE1 = open("volc_database.ini", "a",encoding="utf-8", errors="surrogateescape")
    FILE1.write(str(dbline[0])+"\t"+str(dbline[1])+"\t"+str(dbline[2])+"\t"+str(dbline[3])+"\t"+str(dbline[4])+"\t"+str(dbline[5])+"\t")
    FILE1.write(str(dbline[6])+"\t"+str(dbline[7])+"\t"+str(dbline[8])+"\t"+str(dbline[9])+"\t"+str(dbline[10])+"\t"+str(dbline[11])+"\t")
    FILE1.write(str(dbline[12])+"\t"+str(dbline[13])+"\t"+str(dbline[14])+"\t"+str(dbline[15])+"\t"+str(dbline[16])+"\t"+str(dbline[17])+"\t")
    FILE1.write(str(dbline[18])+"\t"+str(dbline[19])+"\t"+str(dbline[20])+"\t"+str(dbline[21])+"\n")
    FILE1.close()

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers.
    return c * r

def dist_attribution():
    global DBline
    for x in range (0,N_Volc):
        DBline[0] = VolcID[x]
        DBline[1] = LatV[x]
        DBline[2] = LonV[x]
        DBline[3] = VolcH[x]
        for y in range(0,18):
            if ID[y] == "n.a.":
                DBline[y+4] = 9999
            else:
                if TypS[y] ==3:
                    #webcam
                    if FocS[y]==x:
                        #in focus!
                        DBline[y+4]=int(haversine(float(LatV[x]),float(LonV[x]),float(LatS[y]),float(LonS[y])))
                        if float(LonS[y])< float(LonV[x]):
                            #western sector
                            DBline[y+4] = DBline[y+4] * (-1)
                        else:
                            DBline[y+4] = abs(DBline[y+4])
                    else:
                        #not in focus of cams
                        DBline[y+4] = -999
                else:
                    DBline[y+4]=int(haversine(float(LatV[x]),float(LonV[x]),float(LatS[y]),float(LonS[y])))
                    if float(LonS[y])< float(LonV[x]):
                        #western sector
                        DBline[y+4] = DBline[y+4] * (-1)
                    else:
                        DBline[y+4] = abs(DBline[y+4])
        create_vdbline(DBline)
    print("volc_database.ini file generated!" )

def generate_volc_database():
    """Generates volc_database.ini file"""
    print("\n>>STEP3: Automatical generation of volc_database.ini file")
    read_volcanoes()
    read_sensors()
    create_vdbheader()
    dist_attribution()
    print("\n*** Setup operation successful! ***")

while za != 1:
    init_setup()



