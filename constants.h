#ifndef CONSTANTS_H
#define CONSTANTS_H

#include <string>
#include <vector>

#define DISK_SIZE 1024 * 1024 * 10
#define BLOCK_SIZE 4096
#define RECORD_SIZE sizeof(Record)
#define FILE_NAME "games.txt"

using namespace std;

// Structure of a record from database
typedef struct Record
{
    string GAME_DATE_EST;
    int TEAM_ID_home;
    int PTS_home;
    float FG_PCT_home;
    float FT_PCT_home;
    float FG3_PCT_home;
    int AST_home;
    int REB_home;
    int HOME_TEAM_WINS;
} Record;

typedef struct Node
{
    bool isLeaf;
    vector<float> keys;
    vector<Node *> ptrs;              // pointers to blocks
    vector<vector<Record *>> records; // pointers to records (only for leaf nodes)
    Node *nextNodePtr;                // pointer to next node (only for leaf nodes)

    Node(bool isLeaf)
    {
        this->isLeaf = isLeaf;
    }
} Node;

#endif