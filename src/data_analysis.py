
# coding: utf-8

# In[2]:

#
# data analysis: total energy
#


# In[1]:

import os
import numpy as np
import shutil


# In[56]:

# return total energy
# the format of the last line of OSZICAR is:
# 3 F= -.10192617E+02 E0= -.10192615E+02  d E =-.224873E-03
# ['3','F=','-.10192617E+02','E0=','-.10192615E+02','d','E', '=-.224873E-03']
# return -.101926E+02 (10.1926)
#
# this function can be called after checking whether it is a finished job or not
#
def obt_TotEnergy(oszicar_file):
    oszicar = open(oszicar_file,'r')
    oszicar_cont = oszicar.readlines()
    oszicar.close()
    return float(oszicar_cont[-1].split()[4])
#read_OSZICAR('OSZICAR')


# In[58]:

def obt_NumOfAtoms(poscar_file):
    poscar = open(poscar_file,'r')
    poscar_cont = oszicar.readlines()
    poscar.close()
    num_of_atom=poscar_cont[6].split()
    if len(num_of_atom)==1:
        return int(num_of_atom[0])
    else:
        return sum([int(char) for char in num_of_atom])


# In[62]:

#
# calculate energy per atom for a cerntain system
#
def energy_per_atom(oszicar_file,poscar_file):
    return obt_TotEnergy(oszicar_file)/obt_NumOfAtoms(poscar_file)


# In[60]:

#num_of_atom=['2','2']
#sum([int(char) for char in num_of_atom])


# In[54]:

# return band gap from DOSCAR
#
# The idea is first get Fermi level from vasp
#
# this script can obtain Fermi level
def read_FermiLev(vasprun_xml):
    vasprun_out = open(vasprun_xml,'r')
    for line in vasprun_out:
        if 'efermi' in line:
            return float(line.split()[2])
            break
    vasprun_out.close()

def read_dos(doscar,fermi_level):
    doscar_out = open(doscar,'r')
    count = 0
    small_number = 0.000001
    gap_value = 0.
    VBM = fermi_level
    CBM = fermi_level
    conti_zero = []
    for line in doscar_out:
        count =  count + 1
        if count > 6:
            val_list = [float(line.split()[i]) for i in range(3)]
            #print(val_list)
            if val_list[1]<small_number:
                conti_zero.append(val_list[0])
                #print(val_list)
                #break
            else:
                if len(conti_zero)>=2 and conti_zero[0]<=fermi_level and conti_zero[-1]>fermi_level:
                    gap_value = (conti_zero[-1]-conti_zero[0])/len(conti_zero)*(len(conti_zero)+1)
                    VBM = conti_zero[0]-(conti_zero[-1]-conti_zero[0])/len(conti_zero)
                    CBM = conti_zero[-1]+(conti_zero[-1]-conti_zero[0])/len(conti_zero)
                    #print(conti_zero)
                    break
                #elif conti_zero[0]>fermi_level:
                #    break
                else:
                    conti_zero=[]
    doscar_out.close()
    return [gap_value,VBM,CBM]   
#print(read_vasprun('vasprun.xml'))
#read_dos('DOSCAR',read_vasprun('vasprun.xml'))


# In[63]:

#band_gap = {}
#total_energy = {}
band_gap = open('band_gap.dat','w')
tot_energy = open('energy.dat','w')


# In[64]:

# loop over all the folders to get the band gap values:
#
folder_dir = '/home/zhuzhen/2D_structure'

folder_lev_one = os.listdir(folder_dir)
for lev_one_name in folder_lev_one:
    lev_two_path=os.path.join(folder_dir,lev_one_name)
    folder_lev_two = os.listdir(lev_two_path)
    for lev_two_name in folder_lev_two:
        lev_three_path = os.path.join(lev_two_path,lev_two_name)
        DOS_path = lev_three_path + '/DOS'
        # read Fermi level and obtain gap value
        fermi_level = read_FermiLev(DOS_path+'/vasprun_xml')
        gap_value = read_dos(DOS_path+'/DOSCAR',fermi_level)
        # obtain total energy
        energy = energy_per_atom(DOS_path+'/OSZICAR',DOS_path+'/POSCAR')
        #band_gap[lev_two_name]=gap_value
        #total_energy[lev_two_name]=energy
        band_gap.writelines(lev_one_name+' '+lev_two_name+' '+str(gap_value)+'\n')
        tot_energy.writelines(lev_one_name+' '+lev_two_name+' '+str(gap_value)+'\n')
band_gap.close()
tot_energy.close()


# In[ ]:



