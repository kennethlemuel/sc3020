#include "disk/storage.h"
#include "utils.h"

#include <iostream>
#include <string>

using namespace std;

void task1(Disk *disk /*, BPTree *tree*/, string fileName)
{
    cout << "Running Task 1:" << endl;
}

int main()
{
    size_t diskSize = 1024 * 1024 * 10;
    size_t blockSize = 4096;
    std::cout << "Hello" << std::endl;

    Disk *disk = new Disk(diskSize, blockSize, sizeof(Record));
    disk->initializeDisk();

    std::cout << "Disk size: " << disk->getTotalSize() << " bytes" << std::endl;
    std::cout << "Block size: " << disk->getBlockSize() << " bytes" << std::endl;
    std::cout << "Record size: " << disk->getRecordSize() << " bytes" << std::endl;
    std::cout << "Blocks used: " << disk->getNumBlocks() << std::endl;
    std::cout << "Number of records in one block: " << disk->getNumRecordsInBlock() << std::endl;
    std::cout << "Number of records: " << utils::readRecords("games.txt") /*disk->getNumRecords()*/ << std::endl;
    std::cout << std::endl;

    return 0;
}
