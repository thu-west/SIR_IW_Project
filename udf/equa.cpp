#include <mysql.h>
#include <mysql_com.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <algorithm>
#include <bits/stdc++.h>
#include <math.h>
using namespace std;

extern "C"
{
my_bool equa_init(UDF_INIT* initid, UDF_ARGS* args, char* message);
void equa_deinit(UDF_INIT* initid);
long long equa(UDF_INIT *initid, UDF_ARGS *args, char *result, unsigned long *length, char *is_null, char *error);
}

my_bool equa_init(UDF_INIT* initid, UDF_ARGS* args, char* message)
{
    if (args->arg_count != 3)  
    {    
        strcpy(message,"wrong number of arguments: equa() requires three arguments");    
        return 1;  
    }

    if (args->arg_type[0] != STRING_RESULT || args->arg_type[1] != STRING_RESULT || args->arg_type[2] != STRING_RESULT)  
    {    
        strcpy(message,"wrong argument type of arguments: equa() requires string");    
        return 1;  
    }

    return 0;
}

void equa_deinit(UDF_INIT* initid)
{    
}

long long equa(UDF_INIT *initid, UDF_ARGS *args, char *result, unsigned long *length, char *is_null, char *error)
{ 
    std::string query((char*)(args->args[0]));
    std::string comp((char*)(args->args[1]));
    std::string weight((char*)(args->args[2]));
    
    string delimiter = ",,,,,";
    size_t pos = 0;
    string token;

    string enum1;
    string enum2;
    string wei;
    int w;
    float distance = 0;

    for (int i = 0; i < 6; i++){
        pos = query.find(delimiter);
        enum1 = query.substr(0, pos);
        query.erase(0, pos + delimiter.length());

        pos = comp.find(delimiter);
        enum2 = comp.substr(0, pos);
        comp.erase(0, pos + delimiter.length());

        pos = weight.find(delimiter);
        wei = weight.substr(0, pos);
        w = std::stod(wei);
        weight.erase(0, pos + delimiter.length());

        if (enum1 != enum2) {
            distance = distance + w;
        };
    }

    // make the range of the distance (0,10)
    float enumeration_distance = distance * 10;

    return enumeration_distance;
}