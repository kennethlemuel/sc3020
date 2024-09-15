#include "storage.h"
#include <iostream>
#include <cstdlib>

Disk::Disk(size_t totalSize, size_t blockSize) {
    startAddress = (unsigned char*)malloc(totalSize);
    this->totalSize = totalSize;
    this->blockSize = blockSize;
    usedBlocks = 0;
}

Disk::~Disk() {
    free(startAddress);
}

bool Disk::allocateBlock() {
    if ((usedBlocks + 1) * blockSize > totalSize) {
        std::cout << "Error: Not enough space to allocate more blocks." << std::endl;
        return false;
    }
    usedBlocks++;
    return true;
}

void Disk::initializeDisk() {
    std::cout << "Initializing disk storage with block size: " << blockSize << " bytes." << std::endl;
    size_t totalBlocks = totalSize / blockSize;
    std::cout << "Total blocks that can be allocated: " << totalBlocks << std::endl;

    for (size_t i = 0; i < totalBlocks / 2; i++) {
        if (!allocateBlock()) break;
    }
    std::cout << usedBlocks << " blocks have been initialized and allocated for disk storage." << std::endl;
}

size_t Disk::getTotalSize() const {
    return totalSize;
}

size_t Disk::getBlockSize() const {
    return blockSize;
}

size_t Disk::getNumBlocks() const {
    return usedBlocks;
}
