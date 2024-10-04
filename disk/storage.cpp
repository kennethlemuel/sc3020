#include "storage.h"
#include <iostream>
#include <cstdlib>

Disk::Disk(size_t totalSize, size_t blockSize, size_t recordSize)
{
    startAddress = (unsigned char *)malloc(totalSize);
    this->totalSize = totalSize;
    this->blockSize = blockSize;
    this->recordSize = recordSize;
    usedBlocks = 0;
    usedBlockMemory = 0;
    numRecords = 0;
}

Disk::~Disk()
{
    free(startAddress);
}

// Allocate new block after checking for sufficient available memory
bool Disk::allocateBlock()
{
    if ((usedBlocks + 1) * blockSize > totalSize)
    {
        std::cout << "Error: Not enough space to allocate more blocks." << std::endl;
        return false;
    }
    usedBlocks++;
    usedBlockMemory = 0;
    numRecordsInBlock = 0;
    return true;
}

// Initialize disk
void Disk::initializeDisk()
{
    std::cout << "Initializing disk storage with block size: " << blockSize << " bytes." << std::endl;
    size_t totalBlocks = totalSize / blockSize;
    std::cout << "Total blocks that can be allocated: " << totalBlocks << std::endl;
    cout << endl;
}

// Store a record
Record *Disk::storeRecord(Record record)
{
    // If not enough memory in current block, add new block to store record
    if (usedBlockMemory + recordSize > blockSize)
    {
        if (!allocateBlock())
            return nullptr;
    }
    // Else, update current block
    Record *recordAdd = reinterpret_cast<Record *>(startAddress + usedBlocks * blockSize + usedBlockMemory);
    // Copy the content of the record into the allocated memory location on the disk
    memcpy(recordAdd, &record, sizeof(Record)); // Use memcpy to copy data to disk location

    if (usedBlocks == 0)
    {
        usedBlocks++;
    }
    usedBlockMemory += recordSize;
    numRecords++;
    numRecordsInBlock++;
    return recordAdd;
};

Record *Disk::getRecord(int blockIdx, size_t recordOffset)
{
    // in this function, we use the block index and record offset to determine the address of the corresponding record
    size_t offset = blockIdx * blockSize + recordOffset;
    return reinterpret_cast<Record *>(startAddress + offset);
}

// Get total memory size
size_t Disk::getTotalSize() const
{
    return totalSize;
}

// Get block size
size_t Disk::getBlockSize() const
{
    return blockSize;
}

// Get number of blocks used
size_t Disk::getNumBlocks() const
{
    return usedBlocks;
}

// Get record size
size_t Disk::getRecordSize() const
{
    return recordSize;
}

// Get number of records stored
size_t Disk::getNumRecords() const
{
    return numRecords;
}

// Get number of records stored in current block
size_t Disk::getNumRecordsInBlock() const
{
    return numRecordsInBlock;
}