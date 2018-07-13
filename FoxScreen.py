# -*- coding: utf-8 -*-
"""
*** FoxScreen v18.1 ***   
- component of REFIR 18.1 -
-program which displays the output of REFIR on the screen -
 
Copyright (C) 2018 Tobias Dürig
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

Contact: tobi@hi.is

RLZ170318M
"""
import datetime

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
from PIL import Image, ImageTk
print("******* FOX SCREEN **********")
print("         v18.1      ")
print("")
outxt = input("name of data set: ")

bgpath ="background5.jpg"

path = outxt + "_PH_plot.png" 
path2 = outxt + "_APH_plot.png"
path3 = outxt +  "_PHSec_plot.png"
path_def = path
path_map1 = "map1.png"
path_map2 = "map2.png"
Npath = outxt + "_N_plot.png"
Npath2 =outxt + "_SRC_stat.png" 
Npath3 =outxt + "_SRCtotal_stat.png"
Npath_def=Npath

statpath = outxt+"_status1.txt"
statpath_def =statpath
statpath2 = outxt+"_status2.txt"
statpath3 = outxt+"_status3.txt"
statpath4 = outxt+"_status4.txt"
statpath5 = outxt+"_status5.txt"
statpath6 = outxt+"_status6.txt"
statpath7 = outxt+"_status7.txt"
statpath8 = outxt+"_status8.txt"
statpath9 = outxt+"_status9.txt"
statpath10 = outxt+"_status10.txt"
statpath11 = outxt+"_status11.txt"
statpath12 = outxt+"_status12.txt"
statpath_def2 =statpath4

merpath = outxt + "_CMER_plot.png" 
merpath2 = outxt + "_FMER_plot.png"
merpath_def = merpath

masspath = outxt + "_Cmass_plot.png" 
masspath2 = outxt + "_Fmass_plot.png"
masspath_def = masspath
def switch_results():
    """switches result monitor"""
    global statpath, statpath2, statpath3,statpath4,statpath5,statpath6,statpath7,statpath8,statpath9,statpath10
    global statpath_def
    if statpath == statpath_def:
        statpath = statpath2
    elif statpath == statpath2:
        statpath = statpath3
    else:
        statpath = statpath_def
    #update_image()


def switch_status():
    """switches status monitor"""
    global statpath, statpath2, statpath3,statpath4,statpath5,statpath6,statpath7,statpath8,statpath9,statpath10,statpath11,statpath12
    global statpath_def
    if statpath == statpath_def2:
        statpath = statpath5
    elif statpath == statpath5:
        statpath = statpath6
    elif statpath == statpath6:
        statpath = statpath7
    elif statpath == statpath7:
        statpath = statpath8
    elif statpath == statpath8:
        statpath = statpath9
    elif statpath == statpath9:
        statpath = statpath10
    elif statpath == statpath10:
        statpath = statpath11
    elif statpath == statpath11:
        statpath = statpath12
    else:
        statpath = statpath_def2
    #update_image() 

def switch_MER():
    """switches plume height indicator to sector view"""
    global merpath, merpath2
    global merpath_def
    if merpath == merpath_def:
        merpath = merpath2
    else:
        merpath = merpath_def
    #update_image() 

def switch_mass():
    """switches plume height indicator to sector view"""
    global masspath, masspath2
    global masspath_def
    if masspath == masspath_def:
        masspath = masspath2
    else:
        masspath = masspath_def
    #update_image() 

def switch_plh_src():
    """switches plume height indicator to sector view"""
    global path, path2, path3
    global path_def
    if path == path_def:
        path = path2
    elif path == path2:
        path = path3
    else:
        path = path_def
    #update_image() 
    
    
def switch_map():
    """switches map view"""
    global path_map1, path_map2
    global path_map_def
    if path_map1 == "map1.png":
        path_map_def = "map1.png"
        path_map1 = "map2.png"
    else:
        path_map1 = path_map_def
    #update_image() 
    

def switch_Nplot():
    """switches source stats"""
    global Npath, Npath2, Npath3
    global Npath_def
    if Npath == Npath_def:
        Npath = Npath2
    elif Npath == Npath2:
        Npath = Npath3
    else:
        Npath = Npath_def
    #update_image() 
blankscreen = "\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"+\
"\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\n"


u=99
v=0
def update_image():
     global u,v
     global blankscreen
     v= 1    
     frame0 = tk.LabelFrame(root, text="Map", width=480, height=320, bd=5)
     frame1 = tk.LabelFrame(root, text="Plumeheight monitor", width=400, height=320, bd=5) 
     frame2 = tk.LabelFrame(root, text="Source stats", width=440, height=320, bd=5)
     try:
         im0 = Image.open(path_map1)
         im0 = im0.resize((480, 320), Image.ANTIALIAS)
         tkimage0 = ImageTk.PhotoImage(im0)
         label0.tkimage0=tkimage0     ## keep in instance of label
         label0.config(image=label0.tkimage0)
     except EnvironmentError:     
         u = 0
    
     try:
         im1 = Image.open(path)
         im1 = im1.resize((400, 320), Image.ANTIALIAS)
         tkimage1 = ImageTk.PhotoImage(im1)
         label1.tkimage1=tkimage1     ## keep in instance of label
         label1.config(image=label1.tkimage1)
     except EnvironmentError:     
         u = 1

     try:
         im2 = Image.open(Npath)
         im2 = im2.resize((440, 320), Image.ANTIALIAS)
         tkimage2 = ImageTk.PhotoImage(im2)
         label2.tkimage2=tkimage2     ## keep in instance of label
         label2.config(image=label2.tkimage2)
     except EnvironmentError:     
         u = 2

     try:
         im3 = Image.open(merpath)
         im3 = im3.resize((480, 320), Image.ANTIALIAS)
         tkimage3 = ImageTk.PhotoImage(im3)
         label3.tkimage3=tkimage3     ## keep in instance of label
         label3.config(image=label3.tkimage3)
     except EnvironmentError:     
         u = 3
     try:
         im5 = Image.open(masspath)
         im5 = im5.resize((480, 320), Image.ANTIALIAS)
         tkimage5 = ImageTk.PhotoImage(im5)
         label5.tkimage5=tkimage5     ## keep in instance of label
         label5.config(image=label5.tkimage5)
     except EnvironmentError:     
         u = 5
         
     try:
         file = open(statpath)
         data = file.read()
         file.close()
         Results = tk.Label(frame4, text = blankscreen, font = "Helvetica 10", fg = "lime",bg="black")
         Results.grid(row = 1, column = 1)
         Results = tk.Label(frame4, text = data, font = "Helvetica 10", fg = "white",bg="black")
         Results.grid(row = 1, column = 1)
     except EnvironmentError:     
         u = 4     

     root.after(1500, update_image) 





root = tk.Tk()
root.geometry("1480x1080")
root.title("Output FoxShow")
root.configure(background='black')


frame0 = tk.LabelFrame(root, text="Map",font = "Helvetica 12", width=480, height=320,fg="lime",bg="black", bd=5)
try:
    im0 = Image.open(path_map1)
    im0 = im0.resize((480, 320), Image.ANTIALIAS)
    tkimage0 = ImageTk.PhotoImage(im0)
    label0 =  tk.Label(frame0, image=tkimage0)
    label0.pack()
except EnvironmentError:     
    print("WARNING: No map available!")
try:    
    frame1 = tk.LabelFrame(root, text="Plumeheight monitor",font = "Helvetica 12", width=400, height=320,fg="lime",bg="black", bd=5)
    im1 = Image.open(path)
    im1 = im1.resize((400, 320), Image.ANTIALIAS)
    tkimage1 = ImageTk.PhotoImage(im1)
    label1 =  tk.Label(frame1, image=tkimage1)
    label1.pack()
except EnvironmentError:     
    print("WARNING: No REFIR results available!")
try:    
    frame2 = tk.LabelFrame(root, text="Source stats monitor",font = "Helvetica 12", width=400, height=320,fg="lime",bg="black", bd=5)
    im2 = Image.open(Npath)
    im2 = im2.resize((440, 320), Image.ANTIALIAS)
    tkimage2 = ImageTk.PhotoImage(im2)
    label2 =  tk.Label(frame2, image=tkimage2)
    label2.pack()
except EnvironmentError:     
    print("WARNING: No REFIR results available!")





try:    
    frame3 = tk.LabelFrame(root, text="Mass Eruption Rate",font = "Helvetica 12", width=400, height=320,fg="lime",bg="black", bd=5)
    im3 = Image.open(merpath)
    im3 = im3.resize((480, 320), Image.ANTIALIAS)
    tkimage3 = ImageTk.PhotoImage(im3)
    label3 =  tk.Label(frame3, image=tkimage3)
    label3.pack()
except EnvironmentError:     
    print("WARNING: No REFIR results available!")



try:
    frame4 = tk.LabelFrame(root, text="REFIR Status Monitor",font = "Helvetica 12", width=400, height=320,fg="lime",bg="black", bd=5)
    file = open(statpath)
    data = file.read()
    file.close()
    Results = tk.Label(frame4, text = data, font = "Helvetica 10", fg = "white",bg="black")
    Results.grid(row = 1, column = 1)
except EnvironmentError:     
    print("WARNING: No REFIR results available!")
    

try:    
    frame5 = tk.LabelFrame(root, text="Erupted Mass",font = "Helvetica 12", width=480, height=320,fg="lime",bg="black", bd=5)
    im5 = Image.open(masspath)
    im5 = im5.resize((480, 320), Image.ANTIALIAS)
    tkimage5 = ImageTk.PhotoImage(im5)
    label5 =  tk.Label(frame5, image=tkimage5)
    label5.pack()
except EnvironmentError:     
    print("WARNING: No REFIR results available!")

v = 0

frameb=tk.LabelFrame(root, text="",fg="lime",bg="dark green")
tk.Button(root, text = "Switch Map View",font = "Helvetica 11", fg="lime",bg="dark green",highlightbackground="black",\
    width =22, height=1,bd=3, command = switch_map).grid(row=1, column=0,sticky=tk.N)

tk.Button(root, text = "Switch Plumeheight View",font = "Helvetica 11", fg="lime",bg="dark green",highlightbackground="black",\
    width =22, height=1, command = switch_plh_src).grid(row=1, column=1,sticky=tk.N)

tk.Label(root, text= "R3F1R",font = "Helvetica 11",fg="lime",bg="dark green").grid(row=2, column=3)

tk.Button(root, text = "Switch Source Stats",font = "Helvetica 11", fg="lime",bg="dark green",highlightbackground="black",\
    width =22, height=1, command = switch_Nplot).grid(row=1, column=2,sticky=tk.N)

tk.Button(root, text = "Switch MER Plots",font = "Helvetica 11", fg="lime",bg="dark green",highlightbackground="black",\
    width =22, height=1, command = switch_MER).grid(row=3, column=0,sticky=tk.S)

b1=tk.Button(frameb, text = "REFIR Results",font = "Helvetica 11", fg="lime",bg="dark green",highlightbackground="black",\
    width =16, height=1, command = switch_results)
b2=tk.Button(frameb, text = "REFIR Parameters",font = "Helvetica 11", fg="lime",bg="dark green",highlightbackground="black",\
    width =16, height=1, command = switch_status)

tk.Button(root, text = "Switch Erupted Mass Plots",font = "Helvetica 11", fg="lime",bg="dark green",highlightbackground="black",\
    width =22, height=1, command = switch_mass).grid(row=3, column=1,sticky=tk.S)

frameb.grid(row=3, column=2)
b1.grid(row=0, column=0)
b2.grid(row=0, column=1)
frame0.grid(row=0, column=0)
frame1.grid(row=0, column=1)
frame2.grid(row=0, column=2)

frame3.grid(row=5, column=0,sticky=tk.N)
frame4.grid(row=5, column=2)
frame5.grid(row=5, column=1,sticky=tk.N)
root.after(1500, update_image)
root.mainloop()


