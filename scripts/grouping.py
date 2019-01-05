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
print args.directory
print args.prefix
pattern=args.directory+"/"+args.prefix+"*[0-9].csv"
print pattern
matches=glob.glob(pattern)
matches.sort()
for name in matches: 
    if not os.path.isfile(name): next
    print "Processing:",name
    particle=[]
    perimeter=[]
    area=[]
    header=True
    with open(name,'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if header: 
                print row
                header=False
            else:
                a=float(row[1])
                if args.minimum is None or a > float(args.minimum):
                  if args.maximum is None or a < float(args.maximum):
                    particle.append(int(row[0]))    
                    area.append(float(row[1]))    
                    perimeter.append(float(row[2])) 
    print len(particle)            
    sorted_index=sorted(range(len(area)), key=lambda k: area[k])
    file_stub="sorted_minA-%s_maxA-%s_" % (args.minimum,args.maximum)
    
    output_csv_filename=os.path.join(args.output,file_stub+os.path.basename(name))
    output_graph_filename=os.path.join(args.output,file_stub+os.path.splitext(os.path.basename(name))[0])
    print output_csv_filename
    print output_graph_filename
    size=float(args.symbolsize)
    with open(output_csv_filename,'wb') as f:
        writer = csv.writer(f, delimiter=',',  quoting=csv.QUOTE_ALL)
        writer.writerow(['PARTICLE','AREA','PER','CUMULATIVE AREA FRACTION','CUMULATIVE PER FRACTION'])
        cArea=0.0
        cPer=0.0
        cAreaF=[]
        cPerF=[]
        sorted_a=[]
        sorted_p=[]
        p=[]
        for i in sorted_index:
            cArea+=area[i]
            cAreaF.append(area[i]/cArea)
            cPer+=perimeter[i]
            cPerF.append(perimeter[i]/cPer)
            p.append(particle[i])
            sorted_p.append(perimeter[i])
            sorted_a.append(area[i])
        for P,Area,Per,CAF,CPF in zip(p,sorted_a,sorted_p,cAreaF,cPerF):
            writer.writerow([P,Area,Per,CAF,CPF])
        fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
        ax.scatter(cAreaF,cPerF,s=size,marker='o',linewidth=1)
        fig.savefig(output_graph_filename+".png")   # save the figure to file
        fig.savefig(output_graph_filename+".pdf")   # save the figure to file
        plt.close(fig)

#print area[i],perimeter[i]
exit(0)    
