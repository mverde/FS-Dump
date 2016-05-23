import os,sys
import csv

def main():
    #Open files

    with open('super.csv', 'rb') as sup:
        reader = csv.reader(sup)
        supercsv = list(reader)
    
    with open('group.csv', 'rb') as grup:
        reader = csv.reader(grup)
        groupcsv = list(reader)

    with open('bitmap.csv', 'rb') as bit:
        reader = csv.reader(bit)
        bitmapcsv = list(reader)

    with open('inode.csv', 'rb') as inod:
        reader = csv.reader(inod)
        inodecsv = list(reader)

    with open('directory.csv', 'rb') as direc:
        reader = csv.reader(direc)
        directorycsv = list(reader)

    with open('indirect.csv', 'rb') as indir:
        reader = csv.reader(indir)
        indirectcsv = list(reader)

        
if __name__ == "__main__":
        main()
