FileFix=open('bus_data-20170928.txt','r')
FileStor=open('sept28.json','w')
Storage=list()
for line in FileFix:
	Newline=line.replace("}]}]","}]}]\n\n")
	Storage.append(Newline)
print(len(Storage))
for ii in Storage:
	FileStor.write(ii)