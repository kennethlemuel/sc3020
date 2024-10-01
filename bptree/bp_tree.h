#ifndef B_PLUS_TREE_H
#define B_PLUS_TREE_H

#include "../constants.h"

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

    int getMaxKeys() { return maxKeys; }

    int getNumNodes() { return noOfNodes; }

    int getDepth() { return depth; }

    Node *searchNode(float key);

    void setRoot(Node *node);

    void insert(float key, Record *recordPtr);

    std::vector<Record *> *searchRecord(float key);
    // returns a pointer to a vector containing Record pointers

    void printTree();

    Node *splitLeafNode(Node *currNode);

    Node *splitInternalNode(Node *currNode, float *key);

    void deleteKey(float key);

    Node *findParentNode(Node *currNode, Node *childNode);

    void removeInternal(int key, Node *parentNode, Node *nodeToDelete);

    void updateParentKeys(Node *currNode, Node *parentNode, int parentIndex, std::vector<Node *> &parents, std::vector<int> &prevIndexs);

    void printNode(Node *node);

    void resetNumNodesAcc() { this->numNodesAcc = 0; }

    int getNumNodesAcc() { return numNodesAcc; }

    void deleteRecordsBelowThreshold(Node *root, float threshold);
};

#endif