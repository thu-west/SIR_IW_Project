#include <mysql.h>
#include <mysql_com.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <algorithm>
#include <bits/stdc++.h>
#include <math.h>
#include <iostream>
using namespace std;

extern "C"
{
my_bool strd_init(UDF_INIT* initid, UDF_ARGS* args, char* message);
void strd_deinit(UDF_INIT* initid);
long long strd(UDF_INIT *initid, UDF_ARGS *args, char *result, unsigned long *length, char *is_null, char *error);
}

my_bool strd_init(UDF_INIT* initid, UDF_ARGS* args, char* message)
{
    if (args->arg_count != 3)  
    {    
        strcpy(message,"wrong number of arguments: strd() requires three arguments");    
        return 1;  
    }

    if (args->arg_type[0] != STRING_RESULT || args->arg_type[1] != STRING_RESULT || args->arg_type[2] != STRING_RESULT)  
    {    
        strcpy(message,"wrong argument type of arguments: strd() requires string");    
        return 1;  
    }

    return 0;
}

void strd_deinit(UDF_INIT* initid)
{    
}

// Function to return the
// intersection set of s1 and s2
set<string> intersection(set<string> s1, set<string> s2)
{
    set<string> intersect;
  
    // Find the intersection of the two sets
    set_intersection(s1.begin(), s1.end(), s2.begin(), s2.end(),
                     inserter(intersect, intersect.begin()));
  
    return intersect;
}
  
// Function to return the Jaccard index of two sets
double jaccard_index(set<string> s1, set<string> s2)
{
    // Sizes of both the sets
    double size_s1 = s1.size();
    double size_s2 = s2.size();
  
    // Get the intersection set
    set<string> intersect = intersection(s1, s2);
  
    // Size of the intersection set
    double size_in = intersect.size();
  
    // Calculate the Jaccard index
    // using the formula
    double jaccard_in = size_in / (size_s1 + size_s2 - size_in);
  
    // Return the Jaccard index
    return jaccard_in;
}
  
// Function to return the Jaccard distance
double jaccard_distance(double jaccardIndex)
{
    // Calculate the Jaccard distance
    // using the formula
    double jaccard_dist = 1 - jaccardIndex;
  
    // Return the Jaccard distance
    return jaccard_dist;
}


long long strd(UDF_INIT *initid, UDF_ARGS *args, char *result, unsigned long *length, char *is_null, char *error)
{ 
    std::string query((char*)(args->args[0]));
    std::string comp((char*)(args->args[1]));
    std::string weight((char*)(args->args[2]));
    
    string delimiter = ",,,,,";
    size_t query_pos = 0;
    size_t comp_pos = 0;
    size_t weight_pos = 0;
    string query_token;
    string comp_token;
    string weight_token;
    float text_distance = 0;

    for (int i = 0; i < 5; i++){
        set<string> s1;
        set<string> s2;

        query_pos = query.find(delimiter);
        query_token = query.substr(0, query_pos);
        if (query_token.empty()) continue; // ignore null string
        stringstream query_ss(query_token);
        while(query_ss.good()) {
            string substr;
            getline(query_ss, substr, ' ');
            stringstream sub_query_ss(substr);
            while(sub_query_ss.good()) {
                string subsubstr;
                getline(sub_query_ss, subsubstr, '^');
                s1.insert(subsubstr);
            }
        }
        query.erase(0, query_pos + delimiter.length());

        comp_pos = comp.find(delimiter);
        comp_token = comp.substr(0, comp_pos);
        stringstream comp_ss(comp_token);
        while(comp_ss.good()) {
            string substr;
            getline(comp_ss, substr, ' ');
            stringstream sub_comp_ss(substr);
            while(sub_comp_ss.good()) {
                string subsubstr;
                getline(sub_comp_ss, subsubstr, '^');
                s2.insert(subsubstr);
            }
        }
        comp.erase(0, comp_pos + delimiter.length());

        weight_pos = weight.find(delimiter);
        weight_token = weight.substr(0, weight_pos);
        float w = std::stod(weight_token);
        weight.erase(0, weight_pos + delimiter.length());

        double jaccardIndex = jaccard_index(s1, s2);
        text_distance = text_distance + (w * jaccard_distance(jaccardIndex));
    }
  
    // make the range of the distance (0,10)
    text_distance = text_distance * 10;
    
    return text_distance;
}