import datetime
import os
cwd = os.getcwd()
refir_folder = os.path.split(cwd)[0]
fix_obsin_file = os.path.join(refir_folder,'fix_OBSin.txt')
files = os.listdir()
text_files = []
for file in files:
    if file.endswith('.txt'):
        text_files.append(file)
webcam_file = max(text_files,key=os.path.getctime)
file_records = []
time_obs = []
plume_height_avg = []
plume_height_max = []
plume_height_min = []
notes = []
with open(webcam_file,'r',encoding='UTF-8') as input_file:
    next(input_file)
    for line in input_file:
        file_records.append(line)
for record in file_records:
    line_splitted = record.split('  ')
    time_obs.append(line_splitted[0].split(' ')[0])
    plume_height_avg.append(line_splitted[0].split(' ')[1])
    plume_height_min.append(line_splitted[0].split(' ')[2])
    plume_height_max.append(line_splitted[0].split(' ')[3])
    notes.append(line_splitted[2].split('\n')[0])
with open(fix_obsin_file,'a+',encoding='UTF-8') as refir_manual:
    n_obs = 0
    for time in time_obs:
        time_temp = datetime.datetime.strptime(time,'%Y-%m-%d_%H:%M:%S')
        time_obs_final = datetime.datetime.strftime(time_temp,'%m %d %Y %H:%M:%S')
        time_now = datetime.datetime.strftime(datetime.datetime.utcnow(),'%m %d %Y %H:%M:%S')
        uncertainty = float(plume_height_max[n_obs]) - float(plume_height_avg[n_obs])
        refir_manual.write(time_obs_final + '\t' + '1' + '\t' + '800' + '\t' + plume_height_min[n_obs]
                           + '\t' + plume_height_avg[n_obs] + '\t'  + plume_height_max[n_obs] + '\t' + str(uncertainty) + '\t4\t1\t9\t0.0\t0.0\t' + notes[n_obs] + '\n')
        n_obs += 1
