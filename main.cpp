#include "disk/storage.h"
#include <iostream>
#include <string>

int main() {
    size_t diskSize = 1024 * 1024 * 10;
    size_t blockSize = 4096;
    std::cout << "Hello" << std::endl;
    
    Disk disk(diskSize, blockSize, sizeof(Record));
    disk.initializeDisk();

    std::cout << "Disk size: " << disk.getTotalSize() << " bytes" << std::endl;
    std::cout << "Block size: " << disk.getBlockSize() << " bytes" << std::endl;
    std::cout << "Record size: " << disk.getRecordSize() << " bytes" << std::endl;
    std::cout << "Blocks used: " << disk.getNumBlocks() << std::endl;
<<<<<<< Updated upstream
=======
    std::cout << "Number of records in one block: " << disk.getNumRecordsInBlock() << std::endl;
    std::cout << "Number of records: " << disk.getNumRecords() << std::endl;
    std::cout << std::endl;
>>>>>>> Stashed changes

    return 0;
}
