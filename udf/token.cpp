#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <algorithm>
#include <bits/stdc++.h>

using namespace std;

int main()
{

string query = "a b,,,,,c^d,,,,,e f^g,,,,,h,,,,,i";
string delimiter = ",,,,,";
size_t query_pos = 0;
string query_token;


for (int i = 0; i < 4; i++){
        query_pos = query.find(delimiter);
        query_token = query.substr(0, query_pos);
        stringstream query_ss(query_token);
        while(query_ss.good()) {
            string substr;
            getline(query_ss, substr, ' ');
            stringstream sub_query_ss(substr);
            while(sub_query_ss.good()) {
                string subsubstr;
                getline(sub_query_ss, subsubstr, '^');
                cout << subsubstr <<endl;
            }
        }
        query.erase(0, query_pos + delimiter.length());

    }
    cout << query << endl;


}