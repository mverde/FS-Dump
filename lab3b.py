import os,sys
import csv


class Inode:
    def __init__(self, inodenum, numlinks, ptrlist):
        self.inodenum = inodenum
        self.parentinode = 0
        self.refby = {}
        self.numlinks = numlinks
        self.ptrlist = ptrlist

class Block:
    def __init__(self, blocknum, refby):
        self.blocknum = blocknum
        self.refby = {}

def main():
    #Open files

    curr_list = []
    total_inodes = 0
    total_blocks = 0
    block_size = 0
    blocks_pgroup = 0
    inodes_pgroup = 0

    blocks_allocated = []
    allocated_inodes = []

    with open('super.csv', 'rb') as sup:
        reader = csv.reader(sup)
        curr_list = list(reader)
        total_inodes = curr_list[0][1]
        total_blocks = curr_list[0][2]
        block_size = curr_list[0][3]
        blocks_pgroup = curr_list[0][5]
        inodes_pgroup = curr_list[0][6]
    
    with open('group.csv', 'rb') as grup:
        reader = csv.reader(grup)
        curr_list = list(reader)

    with open('bitmap.csv', 'rb') as bit:
        reader = csv.reader(bit)
        curr_list = list(reader)

    with open('inode.csv', 'rb') as inod:
        reader = csv.reader(inod)
        curr_list = list(reader)
        for num in curr_list:
            allocated_inodes.append(Inode(num[0], num[5], num[11:]))

    with open('directory.csv', 'rb') as direc:
        reader = csv.reader(direc)
        curr_list = list(reader)
        found = False
        for inode in curr_list:
            for allocated_inode in allocated_inodes:
                if(allocated_inode.inodenum == inode[4]):
                    allocated_inode.refby[inode[0]] = inode[1]
                    allocated_inode.parentinode = inode[0]
                    found = True
            if not found:
                unallocated = Inode(inode[4], -1, [])
                unallocated.parentinode = inode[0]
                unallocated.refby[inode[0]] = inode[1]
                allocated_inodes.append(unallocated)
            found = False
                

    with open('indirect.csv', 'rb') as indir:
        reader = csv.reader(indir)
        curr_list = list(reader)

    curr_list = []

    output = open('lab3b_check.txt', 'a+')

    for inode in allocated_inodes:
        if inode.numlinks == -1:
            output.write('UNALLOCATED INODE < {} > REFERENCED BY'.format(inode.inodenum))
            for key in inode.refby:
                output.write(' ')
                output.write('DIRECTORY < {} > ENTRY < {} >'.format(key, inode.refby[key]))
            output.write("\n")

    output.close()

if __name__ == "__main__":
        main()
