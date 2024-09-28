#include "disk/storage.h"
<<<<<<< Updated upstream
=======
#include "utils.h"
#include "bptree/bp_tree.h"

>>>>>>> Stashed changes
#include <iostream>

<<<<<<< Updated upstream
int main() {
    size_t diskSize = 1024 * 1024 * 10;
    size_t blockSize = 4096;

    Disk disk(diskSize, blockSize);
    disk.initializeDisk();

    std::cout << "Disk size: " << disk.getTotalSize() << " bytes" << std::endl;
    std::cout << "Block size: " << disk.getBlockSize() << " bytes" << std::endl;
    std::cout << "Blocks used: " << disk.getNumBlocks() << std::endl;
=======
using namespace std;

void task1(Disk *disk, BPTree *bp_tree, string fileName)
{
    cout << "Running Task 1:" << endl;
    cout << "Size of a record: " << sizeof(Record) << " bytes" << endl;
    cout << "Number of records: " << utils::readRecords(fileName, disk, bp_tree) << endl;
    cout << "Number of records stored in a block: " << floor(disk->getBlockSize() / sizeof(Record)) << endl;
    cout << "Number of blocks used for storing data: " << disk->getNumBlocks() << endl;
    cout << endl;
}

int main()
{
    cout << "Hello" << endl;

    Disk *disk = new Disk(DISK_SIZE, BLOCK_SIZE, sizeof(Record));
    disk->initializeDisk();
    BPTree *bp_tree = new BPTree(400);

    task1(disk, bp_tree, FILE_NAME);

    cout << "Disk size: " << disk->getTotalSize() << " bytes" << endl;
    cout << "Block size: " << disk->getBlockSize() << " bytes" << endl;
    cout << "Record size: " << disk->getRecordSize() << " bytes" << endl;
    cout << "Blocks used: " << disk->getNumBlocks() << endl;
    cout << "Number of records in last block: " << disk->getNumRecordsInBlock() << endl;
    cout << endl;
>>>>>>> Stashed changes

    return 0;
}
