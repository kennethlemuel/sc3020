#include "disk/storage.h"
#include "utils.h"
#include "bptree/bp_tree.h"

#include <chrono>
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
    cout << "End of Task 1" << endl;
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
    cout << "End of Task 2" << endl;
    cout << endl;
}

void task3(Disk *disk, BPTree *bp_tree)
{
    vector<Record *> result;
    vector<float> keys;
    float lower = 0.5;
    float upper = 0.8;
    int lowerIndexVal, upperIndexVal, accessedLeafNodes = 0;
    bool search = true;
    bp_tree->resetNumNodesAcc();

    chrono::high_resolution_clock::time_point before = chrono::high_resolution_clock::now();
    Node *resultNode = bp_tree->searchNode(lower);
    while (search)
    {
        keys = resultNode->keys;
        lowerIndexVal = lower_bound(keys.begin(), keys.end(), lower) - keys.begin();
        upperIndexVal = lower_bound(keys.begin(), keys.end(), upper) - keys.begin();
        for (int i = lowerIndexVal; i <= upperIndexVal - 1; i++)
        {
            for (int j = 0; j < resultNode->leafPointers[i].size(); j++)
            {
                result.push_back(resultNode->leafPointers[i][j]);
            }
        }
        upperIndexVal = upperIndexVal == keys.size() ? upperIndexVal - 1 : upperIndexVal;
        if (keys.at(upperIndexVal) >= upper)
        {
            search = false;
        }
        else
        {
            resultNode = resultNode->nextPointer;
            if (resultNode == nullptr)
            {
                break;
            }
            accessedLeafNodes++;
        }
    }
    chrono::high_resolution_clock::time_point after = chrono::high_resolution_clock::now();
    chrono::duration<double> timeTaken = chrono::duration_cast<chrono::duration<double>>(after - before);

    float total_FG_PCT_home = 0;

    for (int i = 0; i < result.size(); i++)
    {
        total_FG_PCT_home += result[i]->FG3_PCT_home;
    }
    total_FG_PCT_home /= result.size();

    cout << "Running Task 3:" << endl;
    cout << "Number of index nodes accessed = " << bp_tree->getNumNodesAcc() + accessedLeafNodes << endl;
    cout << "Number of data blocks accessed = " << result.size() << endl;
    cout << "Average FG3_PCT_home = " << total_FG_PCT_home << endl;
    cout << "Running time for retrieval process = " << timeTaken.count() << "s" << endl;
    cout << endl;
}

void task3_bruteForceLinearScan(Disk *disk)
{
    int noOfBlks = disk->getNumBlocks();
    size_t recordSize = sizeof(Record);

    // Init var to keep track of blks and rec accessed
    int noOfBlksAcc = 0;
    int noOfRecAcc = 0;

    // Starting Timer
    chrono::high_resolution_clock::time_point before = chrono::high_resolution_clock::now();

    for (size_t blockIdx = 0; blockIdx < noOfBlks; ++blockIdx)
    {
        // Increment the number of blocks accessed
        noOfBlksAcc++;

        // Loop through each record in the block
        for (size_t recordOffset = 0; recordOffset < disk->getBlockSize(); recordOffset += sizeof(Record))
        {
            // Get the current record
            Record *record = disk->getRecord(blockIdx, recordOffset);

            // Check if the "FG_PCT_home" value of the record is between 0.5 and 0.8 (inclusive)
            if (0.5 <= record->FG_PCT_home && record->FG_PCT_home <= 0.8)
            {
                // Increment the number of records accessed
                noOfRecAcc++;
                // Continue to the next record
                continue;
            }
        }
    }
    // Stop the timer
    chrono::high_resolution_clock::time_point after = chrono::high_resolution_clock::now();
    // Calculate the time taken by the brute force method
    chrono::duration<double> bruteTimeTaken = chrono::duration_cast<chrono::duration<double>>(after - before);

    // Print the number of data blocks accessed
    cout << "Number of data blocks accessed by brute force method = " << noOfBlksAcc << endl;
    // Print the running time of the brute force method
    cout << "Running time for accessed by brute force method = " << bruteTimeTaken.count() << "s" << endl;
    cout << "End of Task 3" << endl;
}

int main()
{
    Disk *disk = new Disk(DISK_SIZE, BLOCK_SIZE, sizeof(Record));
    disk->initializeDisk();
    BPTree *bp_tree = new BPTree(BLOCK_SIZE);

    task1(disk, bp_tree, FILE_NAME);
    task2(bp_tree);
    task3(disk, bp_tree);
    task3_bruteForceLinearScan(disk);

    return 0;
}