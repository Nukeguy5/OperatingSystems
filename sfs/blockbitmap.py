
import numpy as np

class BlockBitMap:

    FREE = 0
    USED = 1
    BAD = 99
    NOFREE = -99

    def __init__(self, arraysize, blockNumber):
        self.blockNumber = blockNumber
        self.arraysize = arraysize
        self.blockBitMap = np.zeros(shape=(arraysize, 1), dtype='int8')

    def init(self, nblocks):

        # Mark correct blocks as FREE
        for i in range(nblocks):
            self.blockBitMap[i] = BlockBitMap.FREE
        
        # Mark blocks over the number of blocks as BAD
        for i in range(nblocks, self.arraysize):
            self.blockBitMap[i] = BlockBitMap.BAD
    
    def setFree(self, offset):
        self.blockBitMap[offset] = BlockBitMap.FREE
    
    def setUsed(self, offset):
        self.blockBitMap[offset] = BlockBitMap.USED

    def findFree(self):
        free_blocks = []
        for i in range(self.arraysize):
            status = self.blockBitMap[i, 0]
            if status == BlockBitMap.FREE:
                free_blocks.append(i)
            else:
                continue
        
        return free_blocks

    # TODO: Figure out if this is formatting and disk creation's job
    def saveToDisk(self):
        format_arr = np.zeros(shape=(self.arraysize), dtype='int8')
        for i in range(self.arraysize):
            status = self.blockBitMap[i, 0]
            format_arr[i] = status
        
        return format_arr
        