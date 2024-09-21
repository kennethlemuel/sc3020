#include "storage.h"
#include <iostream>
#include <cstdlib>

Disk::Disk(size_t totalSize, size_t blockSize, size_t recordSize) {
    startAddress = (unsigned char*)malloc(totalSize);
    this->totalSize = totalSize;
    this->blockSize = blockSize;
    this->recordSize = recordSize;
    usedBlocks = 0;
    usedBlockMemory = 0;
    numRecords = 0;
}

Disk::~Disk() {
    free(startAddress);
}

// Allocate new block after checking for sufficient available memory
bool Disk::allocateBlock() {
    if ((usedBlocks + 1) * blockSize > totalSize) {
        std::cout << "Error: Not enough space to allocate more blocks." << std::endl;
        return false;
    }
    usedBlocks++;
    usedBlockMemory = 0;
    numRecordsInBlock = 0;
    return true;
}

// Initialize disk
void Disk::initializeDisk() {
    std::cout << "Initializing disk storage with block size: " << blockSize << " bytes." << std::endl;
    size_t totalBlocks = totalSize / blockSize;
    std::cout << "Total blocks that can be allocated: " << totalBlocks << std::endl;

    /*for (size_t i = 0; i < totalBlocks / 2; i++) {
        if (!allocateBlock()) break;
    }*/
    std::cout << usedBlocks << " blocks have been initialized and allocated for disk storage." << std::endl;
}

// Store a record
bool Disk::storeRecord(Record record){ 
    // If not enough memory in current block, add new block to store record
    if (usedBlockMemory + recordSize > blockSize){
        if (!allocateBlock())
            return false;
    }
    // Else, update current block
    usedBlockMemory += recordSize;
    numRecords++;
    numRecordsInBlock++; 
    return true;
};

// Get total memory size
size_t Disk::getTotalSize() const {
    return totalSize;
}

// Get block size
size_t Disk::getBlockSize() const {
    return blockSize;
}

// Get number of blocks used
size_t Disk::getNumBlocks() const {
    return usedBlocks;
}

// Get record size
size_t Disk::getRecordSize() const {
    return recordSize;
}

// Get number of records stored
size_t Disk::getNumRecords() const {
    return numRecords;
}

// Get number of records stored in current block
size_t Disk::getNumRecordsInBlock() const{
    return numRecordsInBlock;
}
