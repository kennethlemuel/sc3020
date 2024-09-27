#ifndef STRUCT_H
#define STRUCT_H

#include <string>

// Structure of a record from database
struct Record
{
    std::string GAME_DATE_EST;
    int TEAM_ID_home;
    int PTS_home;
    float FG_PCT_home;
    float FT_PCT_home;
    float FG3_PCT_home;
    int AST_home;
    int REB_home;
    int HOME_TEAM_WINS;
};

#endif