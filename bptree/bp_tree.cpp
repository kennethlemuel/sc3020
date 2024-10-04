#include "bp_tree.h"

#include <iostream>
#include <queue>
#include <algorithm>

using namespace std;

// constructor
BPTree::BPTree(int nodeSize)
{
    root = nullptr;
    depth = 0;
    noOfNodes = 0;
    nodeSize = nodeSize;
    maxKeys = (nodeSize - sizeof(float *)) / (sizeof(float) + sizeof(float *));
    numNodesAcc = 0;
}

BPTree::~BPTree() {}

void BPTree::printNode(Node *node)
{
    cout << "(";
    for (float key : node->keys)
        cout << key << " ";
    cout << ")\n";
}

// Search Functions

Node *BPTree::searchNode(float key)
{
    int index;
    Node *currentNode = getRoot();

    // If root node does not exist, return nullptr
    if (currentNode == nullptr)
    {
        return nullptr;
    }

    numNodesAcc++;

    // While the node is not a leaf node:
    //      1) We decide which pointer to follow based on target key and the keys maintained in the node
    //      2) Follow the pointer and arrive at a new node
    while (!currentNode->isLeaf)
    {
        index = upper_bound(currentNode->keys.begin(), currentNode->keys.end(), key) - currentNode->keys.begin();
        currentNode = currentNode->pointers.at(index);
        numNodesAcc++;
    }
    return currentNode;
}

vector<Record *> *BPTree::searchRecord(float key)
{
    int index;
    Node *currentNode = searchNode(key);

    // searchNode is used to traverse the tree to the correct leaf node
    // When a leaf node is reached, we search for the corresponding index using lower_bound
    // If the index returns the correct key, the pointer to the index is returned

    index = lower_bound(currentNode->keys.begin(), currentNode->keys.end(), key) - currentNode->keys.begin();

    if (index < currentNode->keys.size() && currentNode->keys.at(index) == key)
    {
        return &(currentNode->leafPointers.at(index));
    }

    return nullptr;
}

// Insert Functions

void BPTree::insertNode(float key, Record *recordPointer)
{
    Node *currentNode = getRoot();
    int index;

    // If root node does not exist, create a new root node and push the record in root node
    if (currentNode == nullptr)
    {
        root = new Node(true);
        noOfNodes++;
        depth++;
        root->keys.push_back(key);
        root->leafPointers.push_back(vector<Record *>(1, recordPointer));
        root->nextPointer = nullptr;
        return;
    }

    // If the key exists in the tree, it is added into the vector of records containing the same key as it
    vector<Record *> *recordVector = searchRecord(key);
    if (recordVector != nullptr)
    {
        recordVector->push_back(recordPointer);
        return;
    }

    // If root node exists but key does not exists in tree, we traverse the tree until we reach a leaf node
    // We will keep track of the list of parent nodes traversed to reach the leaf node
    vector<Node *> parentNodes(1, nullptr);

    while (!currentNode->isLeaf)
    {
        parentNodes.push_back(currentNode);
        index = upper_bound(currentNode->keys.begin(), currentNode->keys.end(), key) - currentNode->keys.begin();
        currentNode = currentNode->pointers.at(index);
    }

    // After reaching a leaf node, record insertion is split into multiple cases

    // Case 1: The leaf node is not fully filled
    index = upper_bound(currentNode->keys.begin(), currentNode->keys.end(), key) - currentNode->keys.begin();
    currentNode->keys.insert(currentNode->keys.begin() + index, key);
    currentNode->leafPointers.insert(currentNode->leafPointers.begin() + index, vector<Record *>(1, recordPointer));

    // Case 2: The leaf node is full
    // Parent node is adjusted accordingly
    // However, if parent node is full too, the process is repeated recursively
    if (currentNode->keys.size() > maxKeys)
    {
        // Leaf node is split into two using the splitLeafNode helper function
        Node *newNode = splitLeafNode(currentNode);
        Node *parentNode = parentNodes.back();
        parentNodes.pop_back();
        key = newNode->keys.front();

        // If parent node is full as a result, it is also split into two
        while (parentNode != nullptr && parentNode->keys.size() == maxKeys)
        {
            index = upper_bound(parentNode->keys.begin(), parentNode->keys.end(), key) - parentNode->keys.begin();
            parentNode->keys.insert(parentNode->keys.begin() + index, key);
            parentNode->pointers.insert(parentNode->pointers.begin() + index + 1, newNode);

            newNode = splitInternalNode(parentNode, &key);
            currentNode = parentNode;

            parentNode = parentNodes.back();
            parentNodes.pop_back();
        }

        // Create a new root node if the original root node is split. Otherwise, update parent node accordingly
        if (parentNode == nullptr)
        {
            parentNode = new Node(false);
            noOfNodes++;
            parentNode->keys.push_back(key);
            parentNode->pointers.push_back(currentNode);
            parentNode->pointers.push_back(newNode);
            root = parentNode;
            depth++;
            return;
        }
        else
        {
            index = upper_bound(parentNode->keys.begin(), parentNode->keys.end(), key) - parentNode->keys.begin();
            parentNode->keys.insert(parentNode->keys.begin() + index, key);
            parentNode->pointers.insert(parentNode->pointers.begin() + index + 1, newNode);
        }
    }
}

Node *BPTree::splitLeafNode(Node *currentNode)
{
    int i;
    Node *newNode = new Node(true);
    noOfNodes++;

    // Transfer half of the records stored in current node to new node
    for (i = 0; i < (maxKeys + 1) / 2; i++)
    {
        newNode->keys.insert(newNode->keys.begin(), currentNode->keys.back());
        currentNode->keys.pop_back();
        newNode->leafPointers.insert(newNode->leafPointers.begin(), currentNode->leafPointers.back());
        currentNode->leafPointers.pop_back();
    }

    // Pointers are adjusted such that current node points to new node and new node points to the original node that current node is pointing at
    newNode->nextPointer = currentNode->nextPointer;
    currentNode->nextPointer = newNode;

    return newNode;
}

Node *BPTree::splitInternalNode(Node *currentNode, float *key)
{
    int i;
    Node *newNode = new Node(false);
    noOfNodes++;

    // Transfer half of the records stored in current node to new node
    for (int i = 0; i < maxKeys / 2; i++)
    {
        newNode->keys.insert(newNode->keys.begin(), currentNode->keys.back());
        currentNode->keys.pop_back();
        newNode->pointers.insert(newNode->pointers.begin(), currentNode->pointers.back());
        currentNode->pointers.pop_back();
    }
    // Move the last pointer from the current node to the split node
    newNode->pointers.insert(newNode->pointers.begin(), currentNode->pointers.back());
    currentNode->pointers.pop_back();
    // Update the key that separates the current node and the split node
    *key = currentNode->keys.back();
    currentNode->keys.pop_back();

    return newNode;
}