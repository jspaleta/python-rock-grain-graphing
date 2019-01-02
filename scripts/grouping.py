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
                particle.append(int(row[0]))    
                area.append(float(row[1]))    
                perimeter.append(float(row[2])) 
    print len(particle)            
    sorted_index=sorted(range(len(area)), key=lambda k: area[k])
    output_csv_filename=os.path.join(args.output,"sorted_"+os.path.basename(name))
    output_graph_filename=os.path.join(args.output,"sorted_"+os.path.splitext(os.path.basename(name))[0]+".png")
    print output_csv_filename
    print output_graph_filename
    with open(output_csv_filename,'wb') as f:
        writer = csv.writer(f, delimiter=',',  quoting=csv.QUOTE_ALL)
        writer.writerow(['PARTICLE','AREA','PERM','CUMULATIVE AREA','CUMULATIVE PERM'])
        X=0
        Y=0
        x=[]
        y=[]
        sorted_a=[]
        sorted_p=[]
        p=[]
        for i in sorted_index:
            X+=area[i]
            x.append(X)
            Y+=perimeter[i]
            y.append(Y)
            p.append(particle[i])
            sorted_p.append(perimeter[i])
            sorted_a.append(area[i])
        maxY=max(y)
        maxX=max(x)
        print maxX,maxY
        for P,Area,Per,X,Y in zip(p,sorted_a,sorted_p,x,y):
            writer.writerow([P,Area,Per,X/maxX,Y/maxY])
        fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
        ax.scatter(np.sqrt(np.array(x)/maxX),np.array(y)/maxY )
        fig.savefig(output_graph_filename)   # save the figure to file
        plt.close(fig)

#print area[i],perimeter[i]
exit(0)    
