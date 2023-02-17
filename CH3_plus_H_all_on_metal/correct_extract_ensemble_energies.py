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
        count = 0
        newlines = []
with open('Ag2O_C2H4-1.csv','w+') as g:
    g.writelines(newlines)
