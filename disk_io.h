#ifndef UTILS_H
#define UTILS_H

#include "disk/storage.h"
#include "struct.h"

#include <vector>
#include <fstream>
#include <iostream>
#include <sstream>


int readFileIntoDisk(std::string fileName, Disk* disk, size_t bufferSize = 100) {
    std::ifstream inputFile(fileName);
    if (!inputFile.is_open()) {
        std::cerr << "Error: Could not open file " << fileName << std::endl;
        return 0;
    }

    std::vector<Record> recordBuffer;
    recordBuffer.reserve(bufferSize);  

    std::string line;
    int numOfRecords = 0;
    getline(inputFile, line);  // Skip the header

    // Insert each line of the file into a record
    while (getline(inputFile, line)) {
        std::stringstream ss(line);
        std::string GAME_DATE_EST, TEAM_ID_home_str, PTS_home_str, FG_PCT_home_str, FT_PCT_home_str, FG3_PCT_home_str, AST_home_str, REB_home_str, HOME_TEAM_WINS_str;

        getline(ss, GAME_DATE_EST, '\t');
        getline(ss, TEAM_ID_home_str, '\t');
        getline(ss, PTS_home_str, '\t');
        getline(ss, FG_PCT_home_str, '\t');
        getline(ss, FT_PCT_home_str, '\t');
        getline(ss, FG3_PCT_home_str, '\t');
        getline(ss, AST_home_str, '\t');
        getline(ss, REB_home_str, '\t');
        getline(ss, HOME_TEAM_WINS_str, '\t');

        // Type change from string to respective types
        unsigned int TEAM_ID_home = std::stoi(TEAM_ID_home_str);
        unsigned int PTS_home = std::stoi(PTS_home_str);
        float FG_PCT_home = std::stof(FG_PCT_home_str);
        float FT_PCT_home = std::stof(FT_PCT_home_str);
        float FG3_PCT_home = std::stof(FG3_PCT_home_str);
        unsigned int AST_home = std::stoi(AST_home_str);
        unsigned int REB_home = std::stoi(REB_home_str);
        unsigned int HOME_TEAM_WINS = std::stoi(HOME_TEAM_WINS_str);

        Record record = {
            GAME_DATE_EST, TEAM_ID_home, PTS_home, FG_PCT_home, FT_PCT_home, 
            FG3_PCT_home, AST_home, REB_home, HOME_TEAM_WINS
        };


        recordBuffer.push_back(record);
        numOfRecords++;


        if (recordBuffer.size() == bufferSize) {
            for (const Record& r : recordBuffer) {
                disk->storeRecord(r);
            }
            recordBuffer.clear(); 
        }
    }

    if (!recordBuffer.empty()) {
        for (const Record& r : recordBuffer) {
            disk->storeRecord(r);
        }
    }

    inputFile.close();
    return numOfRecords;
}

#endif