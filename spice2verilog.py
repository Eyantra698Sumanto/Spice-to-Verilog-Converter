import os
import sys

kicadFile = "/home/sumanto/Desktop/spice_verilog_mapper/circuit"
#projpath = "/home/sumanto/Desktop/spice_verilog_mapper/"
kicadFile = sys.argv[1]
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
parsedcontent=[]
for contentlist in contentlines:
	if "sky130" in contentlist:
	# if len(contentlist)>1 and ( contentlist[0:1]=='U' or contentlist[0:1]=='X') and not 'plot_' in contentlist :
		#print(contentlist)
		netnames=contentlist.split()
		net = ' '.join(map(str,netnames[1:-1]))
		netnames[-1]=netnames[-1].replace("sky130",'')
		#net=net.replace(netnames[-1],'')
		#net=net.replace('BI_','')
		#net=net.replace('BO_','')
		net2=[]
		for j in net.split():
			#print(j)
			secondpart=j
			if '_' in j:
				secondpart=j.split('_')[1]
			if secondpart in net2:
				continue
			if net.count(secondpart)-1>0:
				l="["+str(net.count(secondpart)-1)+":0"+"] "+secondpart
			else:
				l=secondpart
			
			net2.append(secondpart)
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
	parsedcontent.append('''`include "'''+j+'''.v"''')
parsedcontent.append("module "+filename+"("+', '.join(inputlist+realinputlist+outputlist+realoutputlist)+");")
if inputlist:
	parsedcontent.append("input "+', '.join(inputlist)+";")
if realinputlist:
	parsedcontent.append("input real "+', '.join(inputlist)+";")
if outputlist:
	parsedcontent.append("output "+', '.join(outputlist)+";")
if realoutputlist:
	parsedcontent.append("output real "+', '.join(realoutputlist)+";")
if wirelist:
	parsedcontent.append("wire "+', '.join(wirelist)+";")
if realwirelist:
	parsedcontent.append("wire real"+', '.join(realwirelist)+";")
for j in uutlist:
	parsedcontent.append(j)
parsedcontent.append("endmodule;")
for j in parsedcontent:
	print(j)
	parsedfile.write(j+"\n")
