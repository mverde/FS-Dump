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

    block_freelist_blocknums = []
    inode_freelist_blocknums = []
    block_freelist = []
    inode_freelist = []

    blocks_allocated = []
    allocated_inodes = []

    with open('super.csv', 'rb') as sup:
        reader = csv.reader(sup)
        curr_list = list(reader)
        total_inodes = int(curr_list[0][1])
        total_blocks = int(curr_list[0][2])
        block_size = int(curr_list[0][3])
        blocks_pgroup = int(curr_list[0][5])
        inodes_pgroup = int(curr_list[0][6])
    
    with open('group.csv', 'rb') as grup:
        reader = csv.reader(grup)
        curr_list = list(reader)
        for group in curr_list:
            block_freelist_blocknums.append(int(group[5]))
            inode_freelist_blocknums.append(int(group[4]))

    with open('bitmap.csv', 'rb') as bit:
        reader = csv.reader(bit)
        curr_list = list(reader)
        i = 0
        for entry in curr_list:
            final_entry = map(int, entry)
            if final_entry[0] == block_freelist_blocknums[i]:
                block_freelist.append(final_entry)
            elif final_entry[0] == inode_freelist_blocknums[i]:
                inode_freelist.append(final_entry)
            else:
                i += 1

    with open('inode.csv', 'rb') as inod:
        reader = csv.reader(inod)
        curr_list = list(reader)
        for num in curr_list:
            allocated_inodes.append(Inode(int(num[0]), int(num[5]), [int(x, 16) for x in num[11:]]))

    with open('directory.csv', 'rb') as direc:
        reader = csv.reader(direc)
        curr_list = list(reader)
        found = False
        for inode in curr_list:
            for allocated_inode in allocated_inodes:
                if(allocated_inode.inodenum == int(inode[4])):
                    allocated_inode.refby[int(inode[0])] = int(inode[1])
                    allocated_inode.parentinode = int(inode[0])
                    found = True
            if not found:
                unallocated = Inode(int(inode[4]), -1, [])
                unallocated.parentinode = int(inode[0])
                unallocated.refby[int(inode[0])] = int(inode[1])
                allocated_inodes.append(unallocated)
            found = False
                

    with open('indirect.csv', 'rb') as indir:
        reader = csv.reader(indir)
        curr_list = list(reader)

    curr_list = []

    output = open('lab3b_check.txt', 'w+')

    for inode in allocated_inodes:
        if inode.numlinks == -1:
            output.write('UNALLOCATED INODE < {} > REFERENCED BY'.format(inode.inodenum))
            for key in inode.refby:
                output.write(' ')
                output.write('DIRECTORY < {} > ENTRY < {} >'.format(key, inode.refby[key]))
            output.write("\n")
        elif not inode.refby and inode.inodenum > 10:
            output.write('MISSING INODE < {} > SHOULD BE IN FREE LIST < {} >\n'.format(inode.inodenum, inode_freelist_blocknums[inode.inodenum / inodes_pgroup]))

    output.close()

if __name__ == "__main__":
        main()
