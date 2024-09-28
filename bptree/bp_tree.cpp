#include "bp_tree.h"

#include <iostream>
#include <queue>

using namespace std;

BPTree::BPTree(int nodeSize)
{
    root = nullptr;
    depth = 0;
    noOfNodes = 0;
    this->nodeSize = nodeSize;
    this->maxKeys = (nodeSize - sizeof(float *)) / (sizeof(float) + sizeof(float *));
    numNodesAcc = 0;
}

BPTree::~BPTree() {}

void BPTree::printNode(Node *node)
{
    cout << "[ ";
    for (float key : node->keys)
        cout << key << " ";
    cout << "]\n";
}

void BPTree::setRoot(Node *r)
{
    this->root = r;
}

void BPTree::printTree()
{
    queue<Node *> q;
    q.push(root);
    while (!q.empty())
    {
        int n = q.size();
        for (int i = 0; i < n; i++)
        {
            Node *node = q.front();
            q.pop();
            printNode(node);
            // if internal node, push child nodes into queue
            if (!node->isLeaf)
            {
                for (Node *child : node->ptrBlk)
                    q.push(child);
            }
        }
        cout << endl;
    }
}