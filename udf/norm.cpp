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
my_bool norm_init(UDF_INIT* initid, UDF_ARGS* args, char* message);
void norm_deinit(UDF_INIT* initid);
long long norm(UDF_INIT *initid, UDF_ARGS *args, char *result, unsigned long *length, char *is_null, char *error);
}

my_bool norm_init(UDF_INIT* initid, UDF_ARGS* args, char* message)
{
    if (args->arg_count != 3)  
    {    
        strcpy(message,"wrong number of arguments: norm() requires three arguments");    
        return 1;  
    }

    if (args->arg_type[0] != STRING_RESULT || args->arg_type[1] != STRING_RESULT || args->arg_type[2] != STRING_RESULT)  
    {    
        strcpy(message,"wrong argument type of arguments: norm() requires string");    
        return 1;  
    }

    return 0;
}

void norm_deinit(UDF_INIT* initid)
{    
}

long long norm(UDF_INIT *initid, UDF_ARGS *args, char *result, unsigned long *length, char *is_null, char *error)
{ 
    std::string query((char*)(args->args[0]));
    std::string comp((char*)(args->args[1]));
    std::string weight((char*)(args->args[2]));
    
    string delimiter = ",,,,,";
    size_t pos = 0;
    string token;

    // read query interval value
    pos = query.find(delimiter);
    token = query.substr(0, pos);
    float query_age = std::stod(token);
    query.erase(0, pos + delimiter.length());
    float query_visit = std::stod(query);

    // read compared interval value
    pos = comp.find(delimiter);
    token = comp.substr(0, pos);
    float comp_age = std::stod(token);
    comp.erase(0, pos + delimiter.length());
    float comp_visit = std::stod(comp);
    
    // read range value
    pos = weight.find(delimiter);
    token = weight.substr(0, pos);
    float age_range = std::stod(token);
    weight.erase(0, pos + delimiter.length());

    pos = weight.find(delimiter);
    token = weight.substr(0, pos);
    float visit_range = std::stod(token);
    weight.erase(0, pos + delimiter.length());

    // read weight value
    pos = weight.find(delimiter);
    token = weight.substr(0, pos);
    float age_weight = std::stod(token);
    weight.erase(0, pos + delimiter.length());
    float visit_weight = std::stod(weight);

    // make the range of the distance (0, 10)
    float interval_distance = ((age_weight * abs(query_age - comp_age) / age_range) + \
        (visit_weight * abs(query_visit - comp_visit) / visit_range)) * 10;

    return interval_distance;
}