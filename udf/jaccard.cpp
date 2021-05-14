#include <mysql.h>
#include <mysql_com.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <algorithm>
#include <bits/stdc++.h>
using namespace std;

extern "C"
{
my_bool dis_init(UDF_INIT* initid, UDF_ARGS* args, char* message);
void dis_deinit(UDF_INIT* initid);
long long dis(UDF_INIT *initid, UDF_ARGS *args, char *result, unsigned long *length, char *is_null, char *error);
}

my_bool dis_init(UDF_INIT* initid, UDF_ARGS* args, char* message)
{
    if (args->arg_count != 2)  
    {    
        strcpy(message,"wrong number of arguments: dis() requires two arguments");    
        return 1;  
    }

    if (args->arg_type[0] != STRING_RESULT || args->arg_type[1] != STRING_RESULT)  
    {    
        strcpy(message,"wrong argument type of arguments: dis() requires string");    
        return 1;  
    }

    return 0;
}

void dis_deinit(UDF_INIT* initid)
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
    double jaccard_in = size_in
                        / (size_s1 + size_s2 - size_in);
  
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

long long dis(UDF_INIT *initid, UDF_ARGS *args, char *result, unsigned long *length, char *is_null, char *error)
{ 
    // Elements of the 1st set
    set<string> s1;
    s1.insert("1");
    s1.insert("2");
    s1.insert("3");
    s1.insert("4");
    s1.insert("5");
  
    // Elements of the 2nd set
    set<string> s2;
    s2.insert("4");
    s2.insert("5");
    s2.insert("6");
  
    double jaccardIndex = jaccard_index(s1, s2);
  
    return jaccard_distance(jaccardIndex)*100;
}