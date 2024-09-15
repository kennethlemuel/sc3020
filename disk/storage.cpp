#include <iostream>
#include <cstdlib>   
#include <fstream>    

using namespace std;

class Disk {
public:
    Disk(size_t totalSize, size_t blockSize);
    ~Disk();

    bool allocateBlock();
    void initializeDisk();

    size_t getTotalSize() const;
    size_t getBlockSize() const;
    size_t getNumBlocks() const;

private:
    unsigned char* startAddress;
    size_t totalSize;
    size_t blockSize;
    size_t usedBlocks;
};

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
        cout << "Error: Not enough space to allocate more blocks." << endl;
        return false;
    }
    usedBlocks++;
    return true;
}

void Disk::initializeDisk() {
    cout << "Initializing disk storage with block size: " << blockSize << " bytes." << endl;
    size_t totalBlocks = totalSize / blockSize;
    cout << "Total blocks that can be allocated: " << totalBlocks << endl;
    
    for (size_t i = 0; i < totalBlocks / 2; i++) {
        if (!allocateBlock()) break;
    }
    cout << usedBlocks << " blocks have been initialized and allocated for disk storage." << endl;
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

int main() {
    size_t diskSize = 1024 * 1024 * 10;
    size_t blockSize = 4096;

    Disk disk(diskSize, blockSize);
    disk.initializeDisk();

    cout << "Disk size: " << disk.getTotalSize() << " bytes" << endl;
    cout << "Block size: " << disk.getBlockSize() << " bytes" << endl;
    cout << "Blocks used: " << disk.getNumBlocks() << endl;

    return 0;
}
