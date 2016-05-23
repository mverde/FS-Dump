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

    inodes_to_links = {}

    output = open('lab3b_check.txt', 'w+')
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
            inodes_to_links[int(num[0])] = int(num[5])

    with open('directory.csv', 'rb') as direc:
        reader = csv.reader(direc)
        curr_list = list(reader)
        count_links = 0
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
        for inode, numlink in inodes_to_links.items():
            if( numlink != 0):
                for i in curr_list:
                    if ( int(i[4]) == int(inode)):
                        count_links = count_links + 1
                if (count_links != numlink):
                    output.write("LINKCOUNT < {} > IS < {} > SHOULD BE < {} >".format(inode, numlink, count_links))
                    output.write("\n")
            count_links = 0

        medium_list = []

        for i in curr_list:
            if (i[5] != '.' and i[5] != '..'):
                medium_list.append( (i[0], i[4]) )

        parents_to_children={} #dictionary of parent inodes to a list of their children
        for key, val in medium_list:
            parents_to_children.setdefault(key, []).append(val)

        child_in_list = False
        corrent_parent = 0
        for row in curr_list:
            if(row[5] == ".."):
                #check to see that this inode is in the list of of inodes for their given parent
                #parent r[0], current inode row[4]
                #look for parent of parent
                #make sure row[0] is in list of parents_to_children[ [row[4] ]
                if(row[4] in parents_to_children):
                    for val in parents_to_children[ row[4] ]:
                        if (row[0] == val):
                            child_in_list = True
                        elif (row[4] == '2' and row[0] == '2'):
                            child_in_list = True
                    if(child_in_list == False):
                        #find correct val
                        correct_val = ''
                        for key in parents_to_children:
                            for val in parents_to_children[key]:
                                if ( val == row[0]):
                                    correct_val = key
                        output.write("INCORRECT ENTRY IN < {} > NAME <  {} > LINK TO < {} > SHOULD BE < {} >".format(row[0], row[5], row[4], correct_val))
                        output.write("\n")
                    child_in_list = False
                else:
                    correct_val = ''
                    for key in parents_to_children:
                        for val in parents_to_children[key]:
                            if ( val == row[0] ):
                                correct_val = key
                    output.write("INCORRECT ENTRY IN < {} > NAME <  {} > LINK TO < {} > SHOULD BE < {} >".format(row[0], row[5], row[4], correct_val))
                    output.write("\n")
            elif (row[5] == "."):
                if(row[4] != row[0]):
                    output.write("INCORRECT ENTRY IN < {} > NAME <  {} > LINK TO < {} > SHOULD BE < {} >".format(row[0], row[5], row[4], row[0]))
                    output.write("\n")

                

    with open('indirect.csv', 'rb') as indir:
        reader = csv.reader(indir)
        curr_list = list(reader)

    curr_list = []

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
