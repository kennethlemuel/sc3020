#include <iostream>
#include <cstdlib>   
#include <vector>   

using namespace std;

struct Record {
    string game_date;
    int team_id_home;
    int pts_home;
    float fg_pct_home;
    float ft_pct_home;
    float fg3_pct_home;
    int ast_home;
    int reb_home;
    bool home_team_wins;
};


class Disk {
public:
    Disk(size_t size, size_t blkSize, size_t recordSize);  
    ~Disk();                                               

    bool allocateBlock();                                  
    Record* writeRecord(const Record& record);             

    size_t getBlkMaxRecords() const;                       
    size_t getNumBlks() const;                             
    size_t getTotalRecords() const;                        

private:
    unsigned char* startAddress;                           
    size_t size;                                           
    size_t blkSize;                                        
    size_t recordSize;                                     
    size_t numUsedBlks;                                    
    size_t curBlkUsedMem;                                  
    size_t totalRecords;                                   
};

Disk::Disk(size_t size, size_t blkSize, size_t recordSize) {
    startAddress = (unsigned char*)malloc(size);  
    this->size = size;
    this->blkSize = blkSize;
    this->recordSize = recordSize;
    numUsedBlks = 0;
    curBlkUsedMem = 0;
    totalRecords = 0;
}

Disk::~Disk() {
    free(startAddress);  
}

bool Disk::allocateBlock() {
    if ((numUsedBlks + 1) * blkSize > size) {  
        cout << "Disk full: Cannot allocate more blocks!" << endl;
        return false;
    }
    numUsedBlks++;      
    curBlkUsedMem = 0;  
    return true;
}