# \
import os
kicadFile = "/home/sumanto/Desktop/spice_verilog_mapper/circuit"
#projpath = "/home/sumanto/Desktop/spice_verilog_mapper/"
#kicadFile = self.clarg1
(projpath, filename) = os.path.split(kicadFile)
#if os.path.isfile(os.path.join(projpath, 'analysis')):
#    print("Analysis file is present")
analysisfile = open(os.path.join(projpath, filename+".cir"))
#analysisfile = open(os.path.join(projpath, 'analysis'))
content = analysisfile.read()
contentlines = content.split("\n")
parsedfile = open(os.path.join(projpath, 'circuitparsed.v'),'w')
parsedfile.write("")
#print("module "+filename)
i=1
inputlist=[]
realinputlist=[]
outputlist=[]
realoutputlist=[]
wirelist=[]
realwirelist=[]
uutlist=[]
filelist=[]
for contentlist in contentlines:
	if "sky130" in contentlist:
		#print(contentlist)
		netnames=contentlist.split()
		net = ' '.join(map(str,netnames[1:-1]))
		netnames[-1]=netnames[-1].replace("sky130",'')
		net=net.replace(netnames[-1],'')
		#net=net.replace('BI_','')
		#net=net.replace('BO_','')
		net2=[]
		for j in net.split():
			
			if j.split('_')[1] in net2:
				continue
			if net.count(j.split('_')[1])-1>0:
				l="["+str(net.count(j.split('_')[1])-1)+":0"+"] "+j.split('_')[1]
			else:
				l=j.split('_')[1]
			
			net2.append(j.split('_')[1])
			if '_I_' in str(j):
				inputlist.append(l)
			if '_IR_' in str(j):
				inputlist.append(l)
			if '_O_' in str(j):
				outputlist.append(l)
			if '_OR_' in str(j):
				realoutputlist.append(l)
			if '_W_' in str(j) and not(l in wirelist):
				wirelist.append(l)
			if '_WR_' in str(j) and not(l in realwirelist):
				realwirelist.append(l)
			
		
		uutlist.append(netnames[-1].replace("sky130",'')+" uut"+str(i)+" ("+', '.join(net2)+');')
		filelist.append(netnames[-1].replace("sky130",''))
		i=i+1
#print(inputlist)
#print(outputlist)
#print(wirelist)
for j in filelist:
	print('''`include "'''+j+'''.v"''')
print("module "+filename+"("+', '.join(inputlist+realinputlist+outputlist+realoutputlist)+");")
if inputlist:
	print("input "+', '.join(inputlist)+";")
if realinputlist:
	print("input real "+', '.join(inputlist)+";")
if outputlist:
	print("output "+', '.join(outputlist)+";")
if realoutputlist:
	print("output real "+', '.join(realoutputlist)+";")
if wirelist:
	print("wire "+', '.join(wirelist)+";")
if realwirelist:
	print("wire real"+', '.join(realwirelist)+";")
for j in uutlist:
	print(j)
print("endmodule;")