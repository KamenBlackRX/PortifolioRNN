#include <iostream>
#include <stdio.h>
#include <string>
#include <sys/sysinfo.h>

using namespace std;

class CallDB
{
    public:
        /* Call Default constructor*/
        CallDB();
        
        CallDB(string Host, string port);
        
        ~CallDB();

        template<typename T>
        void CountCPU(T* response);

    private:

};

CallDB::CallDB()
{

}

CallDB::CallDB(string Host, string port)
{

}

CallDB::~CallDB()
{

}


template<typename T>
void CallDB::CountCPU(T* response)
{
    if(response == type(std::string))
    {
        // Mesure amount of physical CPUs
         printf("This system has %d processors configured and "
        "%d processors available.\n",
        get_nprocs_conf(), get_nprocs());
        *response = string(get_nprocs);

    }
    else if (response == type(int))
    {

    }
    else
    {

    }

}


int main (int argc, char** argv)
{
    CallDB *db = new CallDB();
    std::string cpu;
    
    db->CountCPU<std::string>(&cpu);
    system("pause");
    return 0;
}