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
        refby = {}

def main():
    #Open files

    inode_freelist = []
    block_freelist = []
    curr_list = []
    total_inodes = 0
    total_blocks = 0
    block_size = 0
    blocks_pgroup = 0
    inodes_pgroup = 0

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
        indicator = 0
        curr_block = bitmapcsv[0][0]
        for entry in curr_list:
            if entry[0] != curr_block:
                curr_block = entry[0]
                indicator += 1
            if indicator % 2 == 0:
                block_freelist += entry
            else:
                inode_freelist += entry

    with open('inode.csv', 'rb') as inod:
        reader = csv.reader(inod)
        curr_list = list(reader)
        allocated_inodes = []
        for num in inodecsv:
            allocated_inodes.append(Inode(num[0], num[5], num[11:]))

    with open('directory.csv', 'rb') as direc:
        reader = csv.reader(direc)
        curr_list = list(reader)

    with open('indirect.csv', 'rb') as indir:
        reader = csv.reader(indir)
        curr_list = list(reader)

    curr_list = []

    output = open('lab3b_check.txt', 'r+b')    

    
if __name__ == "__main__":
        main()
