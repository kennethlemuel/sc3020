#include "disk/storage.h"
#include "utils.h"

#include <iostream>
#include <string>
#include <math.h>

using namespace std;

void task1(Disk *disk /*, BPTree *tree*/, string fileName)
{
    cout << "Running Task 1:" << endl;
    cout << "Size of a record: " << sizeof(Record) << " bytes" << endl;
    cout << "Number of records: " << utils::readRecords(fileName, disk) << endl;
    cout << "Number of records stored in a block: " << floor(disk->getBlockSize() / sizeof(Record)) << endl;
    cout << "Number of blocks used for storing data: " << disk->getNumBlocks() << endl;
    cout << endl;
}

int main()
{
    size_t diskSize = 1024 * 1024 * 10;
    size_t blockSize = 4096;
    cout << "Hello" << endl;

    Disk *disk = new Disk(diskSize, blockSize, sizeof(Record));
    disk->initializeDisk();

    task1(disk, "games.txt");

    cout << "Disk size: " << disk->getTotalSize() << " bytes" << endl;
    cout << "Block size: " << disk->getBlockSize() << " bytes" << endl;
    cout << "Record size: " << disk->getRecordSize() << " bytes" << endl;
    cout << "Blocks used: " << disk->getNumBlocks() << endl;
    cout << "Number of records in last block: " << disk->getNumRecordsInBlock() << endl;
    cout << endl;

    return 0;
}
