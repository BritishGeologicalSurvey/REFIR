REFIR v 20.1
Near-real time estimates of mass eruption rates and plume heights -
 
Copyright (C) 2020 Tobias D�rig[1], Fabio Dioguardi[2]
[1] University of Iceland, Institute of Earth Sciences, Reykjav�k, Iceland. tobi@hi.is
[2] British Geological Survey, The Lyell Centre, Edinburgh, United Kingdom. fabiod@bgs.ac.uk

SETTING DEPENDENCIES UP
=======================
- wgrib2
  Link: http://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/ 
  REFIR assumes the executable is in the system PATH
- grib-tools
  Windows: use chocolatey to install it. https://chocolatey.org/packages/grib-tools
  Linux: Install eccodes
  In both cases, add the binaries folder to the system PATH
- Additional python packages needed
  pandas xlrd future pillow cdsapi pathos gdal utm
- ECMWF client key
  The user needs to register to: https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5
  Once the registration is approved, to get the data follow the instructions here: https://confluence.ecmwf.int/display/WEBAPI/Accessing+ECMWF+data+servers+in+batch
  The user needs to install the personal key in a .ecmwfapirc file, to save in different locations depending on
  the OS. Please read the instructions.

With Conda, it is possible to set a virtual environmnent with all the required dependencies specific for REFIR. This simplifies the 
installation of the different packages and the management of the Python installation in the system.
Instructions for setting the Conda environment:
1) create the environment with all the needed additional packages:
	conda create --name name_of_environment -c conda-forge python=3.8 basemap pandas xlrd future pillow cdsapi pathos gdal utm
2) activate the environment with:
	conda activate name_of_environment
3) install ecmwfapi
	pip install --user https://software.ecmwf.int/wiki/download/attachments/56664858/ecmwf-api-client-python.tgz
4) to exit from the environment:
	conda deactivate

QUICK INSTALLATION GUIDE FOR REFIR
==================================

1. Extract the zip file "REFIR.zip" to a working folder of your choice.

2. After successful extraction, the working folder should contain:
 - the program FIX.py
 - the program FOXI.py
 - the program FoxScreen.py
 - and a subfolder named "refir_config", which contains the program "FoxSet.py" and the default "*,ini" files for the "FutureVolc" setup. 

3. If you want to apply REFIR in another configuration than the default "FutureVolc" setup, just delete all *.ini" files and run "FoxSet.py" for generating new ones.   

4. REFIR is now successfully set up.


QUICK GUIDE FOR INITIALIZING REFIR
===================================

1. When the "*.ini" files have been correctly adjusted, start FIX.py and select the volcano to be monitored.
Remember to close the initial window, to access the main panel of GUI!

2. With FIX.py, select the appropriate settings for REFIR and don't forget to press "confirm" or "update settings" buttons. 

3. If you want to generate a map, click on "Output Control". A window opens which gives you the possibility to specify the output settings. In this window, click on "Show Map".

4. After your initial settings are made, you can start FOXI.py parallelly to FIX.py.
In the initial window specify the time and date of eruption start, and a root name for the output files (e.g. "HEKLA").

4. Click on "Initiate!" and close the initial window. 
FOXI.py starts its first run (and will continue to run automatically every five minutes in the background).

5. To display the output by FOXI.py, start FoxScreen.py.
In the console, specify the root name of the files generated by FOXI (in this example: "HEKLA")

6. A window opens, which gives an operational overview of the current estimates by REFIR
 
At any time the operator can change the settings via FIX, and the display via FoxScreen.


ACKNOWLEDGEMENTS
===================================
Funded by BGS Innovation Flexible Fund.
We thank Luca Merucci (luca.merucci@ingv.it) and Stefano Corradini (stefano.corradini@ingv.it) for their cooperation in developing the satellite_retrieval.py script
