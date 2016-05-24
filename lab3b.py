import os,sys
import csv


total_inodes = 0
total_blocks = 0
block_size = 0
blocks_pgroup = 0
inodes_pgroup = 0
groups = 0

class BlockTreeNode:
    def __init__(self, blocknum):
        self.blocknum = blocknum
        self.children = []

def traverse_block_tree(output_file, block_dict, inodenum, entrynum, current_node, indirect_blocknum=0):
    global blocks_pgroup
    global groups

    blocknum = 0
    children = []
    if indirect_blocknum:
        blocknum = current_node[1].blocknum
        children = current_node[1].children
    else:
        blocknum = current_node.blocknum
        children = current_node.children
    
    if blocknum == 0 or blocknum > blocks_pgroup * groups:
        output_file.write('INVALID BLOCK < {} > IN INODE < {} > '.format(current_node.blocknum, inodenum))
        if indirect_blocknum:
            output_file.write('INDIRECT BLOCK < {} > '.format(indirect_blocknum))
        output_file.write('ENTRY < {} >\n'.format(current_node.blocknum, inodenum, entrynum))
    for inode in children:
        traverse_block_tree(output_file, block_dict, inodenum, entrynum, inode, blocknum)

class Inode:
    def __init__(self, inodenum, numlinks, block_tree):
        self.inodenum = inodenum
        self.parentinode = 0
        self.refby = []
        self.numlinks = numlinks
        self.block_tree = block_tree

class Block:
    def __init__(self, blocknum, refby):
        self.blocknum = blocknum
        self.refby = []

def main():
    #Open files
    global total_inodes
    global total_blocks
    global block_size
    global blocks_pgroup
    global inodes_pgroup
    global groups

    curr_list = []

    block_freelist_blocknums = []
    inode_freelist_blocknums = []
    block_freelist = []
    inode_freelist = []

    allocated_blocks = {}
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
            groups += 1
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
            block_ptrs = [int(x, 16) for x in num[11:]]
            block_tree = []
            for ptr in block_ptrs:
                if ptr:
                    block_tree.append(BlockTreeNode(ptr))
                else:
                    block_tree.append(BlockTreeNode(-1))
            new_inode = Inode(int(num[0]), int(num[5]), block_tree)
            allocated_inodes.append(new_inode)
            inodes_to_links[int(num[0])] = int(num[5])

    with open('directory.csv', 'rb') as direc:
        reader = csv.reader(direc)
        curr_list = list(reader)
        count_links = 0
        found = False
        for inode in curr_list:
            for allocated_inode in allocated_inodes:
                if(allocated_inode.inodenum == int(inode[4])):
                    allocated_inode.refby.append((int(inode[0]), int(inode[1])))
                    allocated_inode.parentinode = int(inode[0])
                    found = True
            if not found:
                unallocated = Inode(int(inode[4]), -1, [])
                unallocated.parentinode = int(inode[0])
                unallocated.refby.append((int(inode[0]), int(inode[1])))
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


<<<<<<< HEAD
=======
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

                

>>>>>>> d7ccae6c08894341d35dd787ed58b19c663bc143
    with open('indirect.csv', 'rb') as indir:
        reader = csv.reader(indir)
        curr_list = list(reader)

        #Build each inode's indirect block tree
        for inode in allocated_inodes:
            if inode.numlinks != -1:
                #Singly indirect
                if inode.block_tree[12]:
                    for row in curr_list:
                        if int(row[0], 16) == inode.block_tree[12].blocknum:
                            inode.block_tree[12].children.append((int(row[1], 16), BlockTreeNode(int(row[2], 16))))
                #Doubly indirect
                if inode.block_tree[13]:
                    for row in curr_list:
                        if int(row[0], 16) == inode.block_tree[13].blocknum:
                            inode.block_tree[13].children.append((int(row[1], 16), BlockTreeNode(int(row[2], 16))))
                            
                    for child in inode.block_tree[13].children:
                        for row in curr_list:
                            if int(row[0], 16) == child[1].blocknum:
                                child[1].children.append((int(row[1], 16), BlockTreeNode(int(row[2], 16))))
                #Triply indirect
                if inode.block_tree[14]:
                    for row in curr_list:
                        if int(row[0], 16) == inode.block_tree[14].blocknum:
                            inode.block_tree[14].children.append((int(row[1], 16), BlockTreeNode(int(row[2], 16))))
                            
                    for child in inode.block_tree[14].children:
                        for row in curr_list:
                            if int(row[0], 16) == child[1].blocknum:
                                child[1].children.append((int(row[1], 16), BlockTreeNode(int(row[2], 16))))
                                
                        for grandchild in child.children:
                            for row in curr_list:
                                if int(row[0], 16) == grandchild[1].blocknum:
                                    grandchild[1].children.append((int(row[1], 16), BlockTreeNode(int(row[2], 16))))

    curr_list = []

    for inode in allocated_inodes:
        inode.refby = sorted(inode.refby, key = lambda x: x[0])
        if inode.numlinks == -1:
            output.write('UNALLOCATED INODE < {} > REFERENCED BY'.format(inode.inodenum))
            for item in inode.refby:
                output.write(' ')
                output.write('DIRECTORY < {} > ENTRY < {} >'.format(item[0], item[1]))
            output.write("\n")
        elif not inode.refby and inode.inodenum > 10:
            output.write('MISSING INODE < {} > SHOULD BE IN FREE LIST < {} >\n'.format(inode.inodenum, inode_freelist_blocknums[inode.inodenum / inodes_pgroup]))

        if inode.numlinks != -1:
            for index, block_node in enumerate(inode.block_tree):
                traverse_block_tree(output, allocated_blocks, inode.inodenum, index, block_node)

    output.close()

if __name__ == "__main__":
        main()
