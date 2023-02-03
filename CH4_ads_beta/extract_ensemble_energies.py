with open('OUTCAR') as f:
    content = f.readlines()

output = False
count=0
newlines = []
for line in content:
    line = line.strip()
    if output == True and count <2000:
	newlines.append(line + '\n')
	count +=1
    if 'ensemble' in line:
	output = True
with open('BEEF_vdw_ensemble_energies.csv','w+') as g:
    g.writelines(newlines)
