#include "disk/storage.h"
#include "disk_io.h"
#include <iostream>

int main() {
    size_t diskSize = 1024 * 1024 * 10;
    size_t blockSize = 4096;

    Disk disk(diskSize, blockSize);
    disk.initializeDisk();
    int recordsLoaded = readFileIntoDisk("games.txt", &disk); 

    std::cout << "Disk size: " << disk.getTotalSize() << " bytes" << std::endl;
    std::cout << "Block size: " << disk.getBlockSize() << " bytes" << std::endl;
    std::cout << "Blocks used: " << disk.getNumBlocks() << std::endl;
    std::cout << "Number of records: " << recordsLoaded << std::endl;
    
    return 0;
}
