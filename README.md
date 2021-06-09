Tested Environment
----
* Ubuntu 20.04<br>
* MySQL 5.7<br>
* Python 3.8.5<br>
* c++ 9.3.0<br>
* g++ 9.3.0<br><br>

UDF Installation
----
Take UDF strd as an example. The other 2 UDFs are installed in the same way. Users only need to replace "strd" by the name of the UDF.<br><br>

Step 1: Compile UDF into a sharable library file.<br>
`g++-9 -I/usr/include/mysql -shared -fPIC -o strd.so strd.cpp`<br><br>

Step 2: Insert the .so file into the plugin directory of MySQL.<br>
(Note that the exact plugin directoy may vary for different versions of MySQL.)<br>
`sudo cp strd.so /usr/lib/mysql/plugin/strd.so`<br><br>

Step 3: Install the UDF inside MySQL.<br>
`DROP FUNCTION IF EXISTS strd;`<br>
`CREATE FUNCTION strd RETURNS integer SONAME 'strd.so'`<br><br>

Dataset
----
The data file `real_data.csv` is extracted from hospital database. 
The dataset is in Chinese. 
Users need to translate on their own if they want to run this project in other languages.
It is tested that English is compatible with this project.<br><br>

Interface
----
Two interfaces are available for this project. 
They use different methods to conduct similarity search of electronic medical records (EMRs).<br><br>

`interface_external_search.py`<br>
This interface uses an external executable to conduct similarity search. 
The external executable `dummy_app` is included in the same directory.
However, this executable is complied to only run on Ubuntu system.<br><br>

`interface.py`<br>
This interface calls UDFs through MySQL to conduct similarity search.
Users need to make sure they install the UDFs before they run this version.
