#ifndef CONSTANTS_H
#define CONSTANTS_H

#include <string>
#include <vector>

#define DISK_SIZE 1024 * 1024 * 10
#define BLOCK_SIZE 4096
#define RECORD_SIZE sizeof(Record)
#define FILE_NAME "games.txt"

using namespace std;

typedef struct Record
{
    int GAME_DATE_EST;
    int TEAM_ID_home;
    char PTS_home;
    float FG_PCT_home;
    float FT_PCT_home;
    float FG3_PCT_home;
    char AST_home;
    char REB_home;
    bool HOME_TEAM_WINS;
} Record;

typedef struct Node
{
    bool isLeaf;                           // indicates whether this node is a leaf or internal node
    vector<float> keys;                    // array of records
    vector<Node *> pointers;               // array of pointers to child nodes (for internal nodes)
    vector<vector<Record *> > leafPointers; // array of pointers to records (for leaf nodes)
    Node *nextPointer;                     // pointer to next node (for leaf nodes)

    Node(bool isLeaf)
    {
        this->isLeaf = isLeaf;
    }
} Node;

#endif