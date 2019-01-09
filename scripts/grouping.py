import argparse
import glob
import os.path
import csv
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-p","--prefix", help="CSV file prefix",default="test_")
parser.add_argument("-d","--directory", help="CSV file directory",default="./")
parser.add_argument("-o","--output", help="directory for output graphs",default="./")
parser.add_argument("-m","--minimum", help="minimum area to consider.",default=None)
parser.add_argument("-M","--maximum", help="maximum area to consider.",default=None)
parser.add_argument("-s","--symbolsize", help="size of symbols",default=10)

args = parser.parse_args()
print(args.directory)
print(args.prefix)
pattern=args.directory+"/"+args.prefix+"*[0-9].csv"
print(pattern)
matches=glob.glob(pattern)
matches.sort()
particle=[]
perimeter=[]
area=[]
filename=[]
for name in matches: 
    if not os.path.isfile(name): next
    print("Processing:",name)
    header=True
    with open(name,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if header: 
                print(row)
                header=False
            else:
                a=float(row[1])
                if args.minimum is None or a > float(args.minimum):
                  if args.maximum is None or a < float(args.maximum):
                    particle.append(int(row[0]))    
                    filename.append(os.path.basename(name))    
                    area.append(float(row[1]))    
                    perimeter.append(float(row[2])) 
print("Total Particles Considered:",len(particle)) 
##
#  TcArea => total cummulative area
#  TcPer => total cummulative perimeter
##
TcArea=sum(area) 
TcPer=sum(perimeter)

# First Lets sort index by area
area_sorted_index=sorted(range(len(area)), key=lambda k: area[k])
# area_sorted_index[0] => particle index of smallest area
# area_soerted_index[-1] => particle index of largest area


# Prepping for secondary sort of perimeter
# Initial area is smallest area
current_area=area[area_sorted_index[0]]
# preload tempory index list with smallest area index
temp_index=[area_sorted_index[0]]

# Final sorted index list starts empty
sorted_index=[]

count=0
# Now lets walk the particle list by index sorted by area 
# starting with the second smallest particle
for i in area_sorted_index[1:]:
    count+=1
    # If still on the same area resort the tempoary index by perimeter
    if area[i]==current_area:
        temp_index.append(i)
        perimeter_sorted_index=sorted(temp_index, key=lambda k: perimeter[k])
    # new area, save previously perimeter sorted index to final index list
    # and prep new area for perimeter sort
    if area[i]!=current_area:
        sorted_index = sorted_index + perimeter_sorted_index
        temp_index=[i]
        perimeter_sorted_index=[i]
        current_area=area[i]
    # final particle: save pervious perimeter sorted index to final index list    
    if i == area_sorted_index[-1]:
        sorted_index = sorted_index + perimeter_sorted_index
file_stub="_sorted_minA-%s_maxA-%s" % (args.minimum,args.maximum)
output_csv_filename=os.path.join(args.output,args.prefix+file_stub+".csv")
output_graph_filename=os.path.join(args.output,args.prefix+file_stub)

print(output_csv_filename)
print(output_graph_filename)
size=float(args.symbolsize)

with open(output_csv_filename,'w') as f:
    writer = csv.writer(f, delimiter=',',  quoting=csv.QUOTE_ALL)
    writer.writerow(["Filename",'PARTICLE','AREA','PER','CUMULATIVE AREA FRACTION','CUMULATIVE PER FRACTION'])
    cArea=0.0
    cPer=0.0
    cAreaF=[]
    cPerF=[]
    sorted_a=[]
    sorted_p=[]
    sorted_f=[]
    p=[]
    for i in sorted_index:
        cArea+=area[i]
        cPer+=perimeter[i]
        ##
        #  cArea => partial cummulative area
        #  cPer => partial cummulative perimeter
        ##
        #cAreaF.append(area[i]/cArea)
        #cPerF.append(perimeter[i]/cPer)
        ##
        #  Dividing by Total area doesnt work!!!!!!
        #  it creates non linear scaling of normalized perimeter to normalized area
        ##
        cAreaF.append(cArea/TcArea)
        cPerF.append(cPer/TcPer)
        p.append(particle[i])
        sorted_p.append(perimeter[i])
        sorted_f.append(filename[i])
        sorted_a.append(area[i])
    for P,fname,Area,Per,CAF,CPF in zip(p,sorted_f,sorted_a,sorted_p,cAreaF,cPerF):
        writer.writerow([fname,P,Area,Per,CAF,CPF])
    fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
    ax.scatter(cAreaF,cPerF,s=size,marker='o',linewidth=1)
    fig.savefig(output_graph_filename+".png")   # save the figure to file
    fig.savefig(output_graph_filename+".pdf")   # save the figure to file
    plt.close(fig)

#print(area[i],perimeter[i])
exit(0)    
