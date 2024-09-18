#ifndef STORAGE_H
#define STORAGE_H

#include "../struct.h"
#include <cstddef> 

class Disk {
public:
    Disk(size_t totalSize, size_t blockSize);
    ~Disk();

    bool allocateBlock();
    void initializeDisk();
    bool storeRecord(Record record);
    Record* writeRecord(Record record);

    size_t getTotalSize() const;
    size_t getBlockSize() const;
    size_t getNumBlocks() const;
    size_t getRecordSize() const;
    size_t getNumRecords() const;
    size_t getNumRecordsInBlock() const;

private:
    unsigned char* startAddress;
    size_t totalSize;
    size_t blockSize;
    size_t usedBlocks; // number of blocks used
    size_t usedBlockMemory; // amount of memory used in current block
    size_t recordSize; 
    size_t numRecords; // number of records
    size_t numRecordsInBlock; // number of records in current block
};

#endif