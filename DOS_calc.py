
# coding: utf-8

# In[1]:

import os
import shutil


# In[10]:

# KPOINTS: 24 by 24 by 1
# different INCAR file
#
# rules: first copy, then modify the files, then submit all the jobs


# In[4]:

# modify INCAR file:
# "the path of submission folder + INCAR" should be given as the input
def modify_INCAR(submit_folder):
    incar_open = open(submit_folder+'/INCAR','r+')
    incar_cont = incar_open.readlines()
    incar_cont[1]='ISMEAR = -5\n'
    incar_cont[3]='ICHARG=11\n'
    incar_cont[5]='IBRION=2; ISIF=2; NSW=0\n'
    incar_open.seek(0)
    incar_open.truncate()
    incar_open.write(''.join(incar_cont))
    incar_open.close()


# In[7]:

# copy CHGCAR or INCAR or POSCAR or KPOINT or submit file:
# from_path: /path/CHGCAR
# to_folder: the folder to do calculations
def copy_FILE(from_path,to_folder):
    shutil.copy2(from_path,to_folder)


# In[8]:

def modify_submit(submit_folder):
    f_submit = open(submit_folder+'/submit.sh','r+')
    sub_cont = f_submit.readlines()
    # for guild:
    sub_cont[7]='cd '+submit_folder+'\n'
    # for stampede:
    #sub_cont[-2]='cd '+lev_three_path+'/static'+'\n'
    f_submit.seek(0)
    f_submit.truncate()
    f_submit.write(''.join(sub_cont))
    f_submit.close()


# In[11]:

def modify_KPOINTS(submit_folder):
    k_grid = '24 24 1'
    kpoints_open = open(submit_folder+'/KPOINTS','r+')
    kpoints_cont = kpoints_open.readlines()
    kpoints_cont[3]=k_grid+'\n'
    kpoints_open.seek(0)
    kpoints_open.truncate()
    kpoints_open.write(''.join(kpoints_cont))
    kpoints_open.close()


# In[12]:

def file_empty(file):
    file_open=open(file,'r')
    file_cont=file_open.readlines()
    if len(file_cont)<5:
        return True
    else:
        return False


# In[9]:

#
# the home folder to conduct all the calculations
#
folder_dir = '/home/zhuzhen/2D_structure'


# In[13]:

# DOS_path is the submission folder
folder_lev_one = os.listdir(folder_dir)
for lev_one_name in folder_lev_one:
    lev_two_path=os.path.join(folder_dir,lev_one_name)
    folder_lev_two = os.listdir(lev_two_path)
    for lev_two_name in folder_lev_two:
        lev_three_path = os.path.join(lev_two_path,lev_two_name)
        if 'static' not in os.listdir(lev_three_path):
            print('Static calculation first for %s!'.format(lev_two_name))
            break
        # create folder for DOS calculation under 'static' folder
        static_path = lev_three_path+'/static'
        DOS_path = static+'/DOS'
        os.makedir(DOS_path)
        #
        # copy INCAR file
        #
        copy_FILE(static_path+'/INCAR',DOS_path)
        modify_INCAR(DOS_path)
        #
        # copy POTCAR file
        #
        copy_FILE(static_path+'/POTCAR',DOS_path)
        #
        # copy KPOINTS file
        #
        copy_FILE(static_path+'/KPOINTS',DOS_path)
        modify_KPOINTS(DOS_path)
        #
        # cp CONTCAR file to POSCAR file
        #
        if file_empty(static_path+'/CONTCAR'):
            print('Static calculation not performed correctly for %s!'.format(lev_two_name))
            break
        copy_FILE(static_path+'/CONTCAR',DOS_path+'/POSCAR')
        #
        # copy submit.sh
        #
        copy_FILE(static_path+'/submit.sh',DOS_path)
        modify_submit(DOS_path)
        #
        # copy CHGCAR file
        #
        copy_FILE(static_path+'/CHGCAR',DOS_path)
        os.system('qsub '+DOS_path+'/submit.sh')


# In[ ]:



