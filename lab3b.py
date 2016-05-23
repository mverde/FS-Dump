import os,sys
import csv


class Inode:
    def __init__(self, inodenum, numlinks, ptrlist):
        self.inodenum = inodenum
        self.parentinode = 0
        self.refby = {}
        self.numlinks = numlinks
        self.ptrlist = ptrlist


def main():
    #Open files

    allocated_inodes = []

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
        for num in inodecsv:
            allocated_inodes.append(Inode(num[0], num[5], num[11:]))

    with open('directory.csv', 'rb') as direc:
        reader = csv.reader(direc)
        directorycsv = list(reader)
        for inode in directorycsv:
            for allocated_inode in allocated_inodes:
                if(allocated_inode.inodenum == inode[4]):
                    allocated_inode.refby[inode[4]] = inode[1]
                    allocated_inode.parentinode = inode[0]
                    print "dir inode: ", inode[4], "entry num: ", inode[1], "parent: ", inode[0]





    with open('indirect.csv', 'rb') as indir:
        reader = csv.reader(indir)
        indirectcsv = list(reader)

        
if __name__ == "__main__":
        main()
