#ifndef UTILS_H
#define UTILS_H

#include <fstream>
#include <iostream>
#include <sstream>

#include "disk/storage.h"
#include "bptree/bp_tree.h"

using namespace std;

namespace utils
{
    int readRecords(string fileName, Disk *disk, BPTree *bp_tree)
    {
        string line;
        int numRecords = 0;

        ifstream file;
        file.open(fileName);

        if (!file.is_open())
        {
            cout << "Error: Unable to open file!" << endl;
            return 0;
        }

        getline(file, line); // discard header
        int i;

        while (getline(file, line))
        {
            istringstream iss(line);
            string GAME_DATE_EST, TEAM_ID_home, PTS_home, FG_PCT_home, FT_PCT_home, FG3_PCT_home, AST_home, REB_home, HOME_TEAM_WINS;
            getline(iss, GAME_DATE_EST, '\t');
            getline(iss, TEAM_ID_home, '\t');
            getline(iss, PTS_home, '\t');
            getline(iss, FG_PCT_home, '\t');
            getline(iss, FT_PCT_home, '\t');
            getline(iss, FG3_PCT_home, '\t');
            getline(iss, AST_home, '\t');
            getline(iss, REB_home, '\t');
            getline(iss, HOME_TEAM_WINS, '\t');

            // Check if the record is relevant (PTS_home field should not be empty)
            if (PTS_home == "")
                continue;

            Record record = {
                GAME_DATE_EST,
                stoi(TEAM_ID_home),
                stoi(PTS_home),
                stof(FG_PCT_home),
                stof(FT_PCT_home),
                stof(FG3_PCT_home),
                stoi(AST_home),
                stoi(REB_home),
                stoi(HOME_TEAM_WINS)};
            Record *recordPtr = (*disk).storeRecord(record);
            bp_tree->insertNode(record.FG3_PCT_home, recordPtr);
            numRecords++;
        }
        file.close();      // Close the input file
        return numRecords; // Return the total number of records processed
    }
}

#endif