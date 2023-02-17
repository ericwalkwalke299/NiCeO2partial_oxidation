#!/usr/bin/env python

'''
	run_BEEF.py
	
	This script will automatically run your BEEF folder. 
	
	Instructions:
	    1) Copy your structure folder from a previous structure into your new
	       structures folder. Make sure your structure folder has the desired name/number for the new structure.
	    2) Place this script in the structure folder you are about to run.
	    3) Delete the POSCAR file in the folder you are running and replace it with your own.
	    4) Run this script in the shell by navigating to the folder where it is located and typing "python run_PBE.py"
	   
	Notes:
	    -Modify line 68 if you want to change the prefix of the slurm job name ("SSZ13-106...").
	    -*****Modify line 70 to be your email address*****
	    -The script automatically checks if the order of atoms b/w POSCAR and
	     POTCAR are the same. If different, it will build the appropriate POTCAR.
	    -The script then submits your job using the sbatch command.
'''

import os

def make_potcar(poscar_atoms):
    filenames = ["/projects/academic/ericwalk/jessecan/POTCARs/POTCAR_" + atom for atom in poscar_atoms]
    with open('POTCAR', 'w') as outfile:
        for file in filenames:
            with open(file) as infile:
                for line in infile:
                    outfile.write(line)

#Open POSCAR file and put its atoms into a list
with open("POSCAR") as poscar:
    lines = poscar.readlines()
    poscar_atoms = lines[5].strip()
    poscar_atoms = poscar_atoms.split()

try:  
    #Open POTCAR file and put its atoms into a list
    with open("POTCAR") as potcar:
        lines = [line for line in potcar.readlines() if "PAW_PBE" in line]
        potcar_atoms = []
        for line in lines:
            line = line.split()
            current_atom = line[line.index("PAW_PBE") + 1]
            if current_atom not in potcar_atoms:
                potcar_atoms.append(current_atom)
    
    #Grab and concatenate POTCAR's in the correct order if order is wrong
    if poscar_atoms != potcar_atoms:
        make_potcar(poscar_atoms)
        
except:
    make_potcar(poscar_atoms)
    


#Get the name of the structure
cwd = os.getcwd()
dirs = cwd.split('/')
structure_num = dirs[-1]

#Modify the name of the slurm job with correct structure number
with open("slurm_run_vasp.sh", 'r') as slurm:
    lines = slurm.readlines()
    for i in range(len(lines)):
            if "job-name" in lines[i]:
                lines[i] = "#SBATCH --job-name=Ni_CeO2_PartialOx-{}-BEEF\n".format(structure_num) #Modify this line if you want to change job name prefix
            elif "mail-user" in lines[i]:
                lines[i] = "#SBATCH --mail-user=scottcoi@buffalo.edu\n" #Modify this line to be your email

with open("slurm_run_vasp.sh", 'w') as slurm:
    slurm.writelines(lines)

#Run the slurm job
os.system("sbatch slurm_run_vasp.sh")