#ifndef B_PLUS_TREE_H
#define B_PLUS_TREE_H

#include "../constants.h"
using namespace std;

class BPTree
{
private:
    Node *root;
    int depth;       // current number of layers in the tree
    int noOfNodes;   // current number of nodes in the tree
    int maxKeys;     // maximum number of keys in one node
    size_t nodeSize; // size of one node
    int numNodesAcc; // number of nodes accessed during operations

public:
    BPTree(int blkSize);
    ~BPTree();

    Node *getRoot() { return root; }
    int getDepth() { return depth; }
    int getNumNodes() { return noOfNodes; }
    int getMaxKeys() { return maxKeys; }
    int getNumNodesAcc() { return numNodesAcc; }

    // Insert Functions
    void insertNode(float key, Record *recordPointer);

    Node *splitLeafNode(Node *currNode);

    Node *splitInternalNode(Node *currNode, float *key);

    // Search Functions
    Node *searchNode(float key);

    vector<Record *> *searchRecord(float key);

    // Miscelleanous
    void printNode(Node *node);

    void resetNumNodesAcc() { numNodesAcc = 0; }
};

#endif