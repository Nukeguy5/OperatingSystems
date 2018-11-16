
import numpy as np
import blocks
from blockbitmap import BlockBitMap
# import struct

class Disk:

    BLOCK_SIZE = 512 # 4096
    BYTEORDER = 'little'
    ENCODING = 'utf8'
    CELLSIZE = 'int32'

    # a row is a block
    @classmethod
    def disk_init(cls, diskname, nblocks=64):
        blank_blocks = np.zeros(shape=(nblocks, Disk.BLOCK_SIZE), dtype=Disk.CELLSIZE)
        
        # Super Block Info
        ninode_blocks = nblocks//10  # Make 10% of blocks inodes
        inode_size = blocks.Inode.size
        ninodes = Disk.BLOCK_SIZE//inode_size * ninode_blocks
        dentry = 0
        dataBitmap_block = 1
        inodeBitmap_block = 2
        dataBlock_start = 3 + ninode_blocks
        inodeBlock_start = 3

        # Initialize super and inode blocks
        sblock = blocks.Superblock.make_block(Disk.BLOCK_SIZE, nblocks, ninode_blocks, ninodes, dentry, dataBitmap_block, inodeBitmap_block, dataBlock_start, inodeBlock_start)
        iblock = blocks.InodeBlock.make_block(Disk.BLOCK_SIZE)

        # Initialize bitmaps
        data_bitmap = BlockBitMap(Disk.BLOCK_SIZE, 1)
        inode_bitmap = BlockBitMap(Disk.BLOCK_SIZE, 2)
        ndata_blocks = nblocks - ninode_blocks - 3  # don't count super block or bitmaps
        data_bitmap.init(ndata_blocks)
        inode_bitmap.init(ninodes)
        inode_bitmap.setBad(0)  # set inode 0 to BAD

        # Write initial blocks to array
        blank_blocks[0] = sblock
        blank_blocks[1] = data_bitmap.saveToDisk()
        blank_blocks[2] = inode_bitmap.saveToDisk()

        for i in range(ninode_blocks):
            i += 3  # don't overwrite superblock or bitmaps
            blank_blocks[i] = iblock

        with open(diskname, 'wb') as f:
            f.write(bytearray(blank_blocks))
            
    @classmethod
    def disk_open(cls, diskname):
        fl = open(diskname, 'rb+')
        return fl

    @classmethod
    def disk_read(cls, open_file, blockNumber):
        start_address = Disk.BLOCK_SIZE * blockNumber * 4  # Multiply by 4 to account for 4 byte cell size
        block_data = np.zeros(shape=(Disk.BLOCK_SIZE), dtype=Disk.CELLSIZE)
        
        open_file.seek(start_address)

        for i in range(Disk.BLOCK_SIZE):
            #  byte_arr = open_file.read(4)
            byte = open_file.read(1)
            block_data[i] = int.from_bytes(byte, Disk.BYTEORDER)
            #  block_data[i] = struct.unpack('i', byte_arr)[0]

        return block_data

    @classmethod
    def disk_write(cls, open_file, blockNumber, data): 
        start_address = Disk.BLOCK_SIZE * blockNumber
        open_file.seek(start_address)
        
        # Check the data type to determine how to convert to binary
        if type(data) == str:
            byte_data = bytearray(data, Disk.ENCODING)
        else:
            byte_data = bytearray(data)
                  
        open_file.write(byte_data[:])

    @classmethod
    def disk_status(cls, ):
        print('The disk is doing GREAT!!')

    @classmethod
    def disk_close(cls, open_file):
        open_file.close()

# disk1 = Disk('qdisk.bin', 6)
# barr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
# # # disk1.disk_write(3, barr)
# # # print(disk1.disk_read(3))


# Disk.disk_init('disk1.bin')
# open_file = Disk.disk_open('disk1.bin')
# print(Disk.disk_read(open_file, 30))
# Disk.disk_write(open_file, 30, barr)
# print(Disk.disk_read(open_file, 30))
# print(Disk.disk_read(open_file, 31))
# print(Disk.disk_read(open_file, 32))
# print(Disk.disk_read(open_file, 33))
# Disk.disk_close(open_file)
