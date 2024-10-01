#include "disk/storage.h"
#include "utils.h"
#include "bptree/bp_tree.h"

#include <iostream>
#include <string>
#include <math.h>

using namespace std;

void task1(Disk *disk, BPTree *bp_tree, string fileName)
{
    cout << "Running Task 1:" << endl;
    cout << "Size of a record: " << sizeof(Record) << " bytes" << endl;
    cout << "Number of records: " << utils::readRecords(fileName, disk, bp_tree) << endl;
    cout << "Number of records stored in a block: " << floor(disk->getBlockSize() / sizeof(Record)) << endl;
    cout << "Number of blocks used for storing data: " << disk->getNumBlocks() << endl;
    bp_tree->printTree();
    cout << endl;
}

void task2(BPTree *bp_tree)
{
    cout << "Running Task 2: " << endl;
    cout << "Parameter N = " << bp_tree->getMaxKeys() << endl;
    cout << "Number of nodes = " << bp_tree->getNumNodes() << endl;
    cout << "Number of levels = " << bp_tree->getDepth() << endl;
    cout << "Content of Root Node: ";
    bp_tree->printNode(bp_tree->getRoot());
    cout << endl;
}

void task3(BPTree *bp_tree)
{
    cout << "Running Task 3:" << endl;
}

int main()
{
    //cout << "Hello" << endl;

    Disk *disk = new Disk(DISK_SIZE, BLOCK_SIZE, sizeof(Record));
    disk->initializeDisk();
    BPTree *bp_tree = new BPTree(400);

    task1(disk, bp_tree, FILE_NAME);
    task2(bp_tree);
    task3(bp_tree);

    cout << "Disk size: " << disk->getTotalSize() << " bytes" << endl;
    cout << "Block size: " << disk->getBlockSize() << " bytes" << endl;
    cout << "Record size: " << disk->getRecordSize() << " bytes" << endl;
    cout << "Blocks used: " << disk->getNumBlocks() << endl;
    cout << "Number of records in last block: " << disk->getNumRecordsInBlock() << endl;
    cout << endl;

    return 0;
}
