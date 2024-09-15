#ifndef STORAGE_H
#define STORAGE_H

#include <cstddef> 

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

#endif
