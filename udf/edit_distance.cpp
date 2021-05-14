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

// Utility function to find minimum of three numbers
int min(int x, int y, int z) { 
    return min(min(x, y), z); 
}

int editDist(string str1, string str2, int m, int n)
{
    // If first string is empty, the only option is to
    // insert all characters of second string into first
    if (m == 0)
        return n;
 
    // If second string is empty, the only option is to
    // remove all characters of first string
    if (n == 0)
        return m;
 
    // If last characters of two strings are same, nothing
    // much to do. Ignore last characters and get count for
    // remaining strings.
    if (str1[m - 1] == str2[n - 1])
        return editDist(str1, str2, m - 1, n - 1);
 
    // If last characters are not same, consider all three
    // operations on last character of first string,
    // recursively compute minimum cost for all three
    // operations and take minimum of three values.
    return 1
           + min(editDist(str1, str2, m, n - 1), // Insert
                 editDist(str1, str2, m - 1, n), // Remove
                 editDist(str1, str2, m - 1,
                          n - 1) // Replace
             );
}

long long dis(UDF_INIT *initid, UDF_ARGS *args, char *result, unsigned long *length, char *is_null, char *error)
{
    std::string str1((char*)(args->args[0]));
    std::string str2((char*)(args->args[1]));
    
    return editDist(str1, str2, str1.length(), str2.length());
}