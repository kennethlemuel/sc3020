#include <vector>
#include <fstream>
#include <iostream>
#include <sstream>
#include "disk/storage.h"
#include "struct.h"

int readFileIntoDisk(std::string fileName, Disk* disk, size_t bufferSize = 100) {
    std::ifstream inputFile(fileName);
    if (!inputFile.is_open()) {
        std::cerr << "Error: Could not open file " << fileName << std::endl;
        return 0;
    }

    std::vector<Record> recordBuffer;
    recordBuffer.reserve(bufferSize);  // Reserve space in the vector to avoid resizing

    std::string line;
    int numOfRecords = 0;
    getline(inputFile, line);  // Skip the header

    while (getline(inputFile, line)) {
        std::stringstream ss(line);
        std::string GAME_DATE_EST, TEAM_ID_home, PTS_home, FG_PCT_home, FT_PCT_home, FG3_PCT_home, AST_home, REB_home, HOME_TEAM_WINS;

        getline(ss, GAME_DATE_EST, '\t');
        getline(ss, TEAM_ID_home, '\t');
        getline(ss, PTS_home, '\t');
        getline(ss, FG_PCT_home, '\t');
        getline(ss, FT_PCT_home, '\t');
        getline(ss, FG3_PCT_home, '\t');
        getline(ss, AST_home, '\t');
        getline(ss, REB_home, '\t');
        getline(ss, HOME_TEAM_WINS, '\t');

        if (PTS_home == "")
            continue;

        Record record = {
            stof(FG_PCT_home),
            stof(FT_PCT_home),
            stof(FG3_PCT_home),
            stoul(TEAM_ID_home),
            static_cast<char>(stoi(PTS_home)),
            static_cast<char>(stoi(AST_home)),
            static_cast<char>(stoi(REB_home)),
            HOME_TEAM_WINS == "1" ? true : false
        };


        recordBuffer.push_back(record);
        numOfRecords++;


        if (recordBuffer.size() == bufferSize) {
            for (const Record& r : recordBuffer) {
                disk->writeRecord(r);
            }
            recordBuffer.clear(); 
        }
    }

    if (!recordBuffer.empty()) {
        for (const Record& r : recordBuffer) {
            disk->writeRecord(r);
        }
    }

    inputFile.close();
    return numOfRecords;
}
