#ifndef STRUCT_H
#define STRUCT_H

// Structure of a record from database
struct Record{
    unsigned int GAME_DATE_EST;
    unsigned int TEAM_ID_home;
    unsigned int PTS_home;
    float FG_PCT_home;
    float FT_PCT_home;
    float FG3_PCT_home;
    unsigned int AST_home;
    unsigned int REB_home;
    unsigned int HOME_TEAM_WINS;
};

#endif