#ifndef UTILS_H
#define UTILS_H

#include <fstream>
#include <iostream>
#include <sstream>

#include "disk/storage.h"
#include "bptree/bp_tree.h"
#include "date.h"

using namespace std;

namespace utils
{
    int convertDatetoDays(string date)
    {

        char separator;
        int day, month, year;

        istringstream dateStream(date);

        dateStream >> day >> separator >> month >> separator >> year;

        date::year_month_day ymd{date::year(year), date::month(month), date::day(day)};
        return date::sys_days{ymd}.time_since_epoch().count();
    }

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
                convertDatetoDays(GAME_DATE_EST),
                stoi(TEAM_ID_home),
                static_cast<char>(stoi(PTS_home)),
                stof(FG_PCT_home),
                stof(FT_PCT_home),
                stof(FG3_PCT_home),
                static_cast<char>(stoi(AST_home)),
                static_cast<char>(stoi(REB_home)),
                HOME_TEAM_WINS == "1" ? true : false};
            Record *recordPtr = (*disk).storeRecord(record);
            bp_tree->insertNode(record.FG3_PCT_home, recordPtr);
            numRecords++;
        }
        file.close();      // Close the input file
        return numRecords; // Return the total number of records processed
    }
}

#endif