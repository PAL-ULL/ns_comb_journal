// You will need to make some modifications in this code to make it work for you. Search for TODO.

#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>
#include <algorithm>

#ifdef MINKNAP
#include "minknap.h"
#endif

#ifdef EXPKNAP
#include "expknap.h"
#endif

#ifdef COMBO
#include "combo.h"
#endif

#ifdef COMBOPLUS
#include "comboplus.h"
#endif

#ifdef COMBO_EXPLICIT
#include "combo_explicit.h"
#endif

#define MAX_STRING_LEN 30
#define MAX_KP_SIZE 2000
#define MIN_TEST_TIME 0.5
#define CONV_TO_MS 10000

using namespace std;

typedef struct KPinst {
	string *Name;
	string *Type;
	int Capacity;
	int noItems;
	int *Weights;
	int *Values;
};

KPinst* readKP(const char path[])
{
    ifstream myfile;
	myfile.open(path);
	string line;
	string delimiter = " ";
	if (myfile.is_open())
	{
		getline (myfile, line);
		   string *name = new string(line);
		getline (myfile, line);
		   string *type = new string(line);
		getline (myfile, line);
        long cap = strtol(line.c_str(), NULL, 10);
		
		int *w = new int[MAX_KP_SIZE];
		int *v = new int[MAX_KP_SIZE];
		int i = 0;
		
		while (getline (myfile, line))
		{
            sscanf(line.c_str(), "%d %d", &w[i], &v[i]);
			i++;
		}
        
        int *w2 = new int[i];
	    int *v2 = new int[i];
    
        for (int j=0; j<i; j++)
        {
			/*if (w[j] > 1000 || v[j] > 1000) {
				cerr << "Very large data in " << path << "\n";
			}*/
			w2[j] = w[j];
			v2[j] = v[j];
			
        }
		/*if (i > 250) {
			cerr << "Very large N in " << path << "\n";
		}*/
        
        KPinst *kp = new KPinst;
        kp->Name = name;
        kp->Type = type;
        kp->Capacity = cap;
        kp->noItems = i;
        kp->Weights = w2;
        kp->Values = v2;
    
        delete []w;
        delete []v;
    
        myfile.close();
        return kp;
	}
	
	myfile.close();
    return 0;
}


int main(int argc, char *argv[])
{
	/* std::cout << "Have " << argc << " arguments:" << std::endl;
    for (int i = 0; i < argc; ++i) {
        std::cout << argv[i] << std::endl;
    } */

	
#if defined(_WIN32)
	string sep = "\\";
#else 
	string sep = "/";
#endif
    // TODO change these paths as appropriate
	string path = "/data/cephfs/punim0664/KPDataDec";
	string outpath = "/data/cephfs/punim0664/KPSolver/190612/output";
	string listname;
	if (argc > 1) {
		listname = argv[1];
	} else {
		listname = "instlist";
	}
	string listpath = path + sep + listname;
	string outputname = listname;
	std::replace(outputname.begin(), outputname.end(), '/', '$');
	
	string instpath = path + sep + "instances" + sep;
	/*string instpath = path + sep + "PCLO" + sep;*/
	//string instpath = path + sep + "Evolved" + sep;
#ifdef MINKNAP
	string min_outputpath = outpath + sep + "min" + sep + "min_" + outputname;
	ofstream min_outputfile;
	min_outputfile.open(min_outputpath.c_str());
#endif
#ifdef EXPKNAP
	string exp_outputpath = outpath + sep + "exp" + sep + "exp_" + outputname;
	ofstream exp_outputfile;
	exp_outputfile.open(exp_outputpath.c_str());
#endif
#ifdef COMBO
	string com_outputpath = outpath + sep + "combo" + sep + "com_" + outputname;
	ofstream com_outputfile;
	com_outputfile.open(com_outputpath.c_str());
	std::cout << com_outputpath.c_str() << std::endl;
#endif
#ifdef COMBOPLUS
	string com_outputpath = outpath + sep + "comboplus" + sep + "com+_" + outputname;
	ofstream com_outputfile;
	com_outputfile.open(com_outputpath.c_str());
	std::cout << com_outputpath.c_str() << std::endl;
#endif
#ifdef COMBO_EXPLICIT
	string com_outputpath = outpath + sep + "combEX" + sep + "comEX_" + outputname;
	ofstream com_outputfile;
	com_outputfile.open(com_outputpath.c_str());
	std::cout << com_outputpath.c_str() << std::endl;
#endif
 
    ifstream listfile;
	listfile.open(listpath.c_str());
	string fname;
	string fullinstpath;
	
	if (listfile.is_open())
	{	
        while(getline(listfile, fname))
        {           
            KPinst* kp;
            fullinstpath = instpath + fname;
			cout << fullinstpath << "\n";
            
            kp = readKP(fullinstpath.c_str());
			int *x = new int[kp->noItems];
			
			double *timerecord = new double(0);
			
#ifdef MINKNAP			
			int yminknap = minknap_wrap(kp->noItems, kp->Values, kp->Weights, x, kp->Capacity, timerecord);
			cout << fname << "," << *timerecord << "," << yminknap << "\n";
            min_outputfile << fname << "," << *timerecord << "," << yminknap << "\n";
#endif
#ifdef EXPKNAP			
			int yexpknap = expknap_wrap(kp->noItems, kp->Values, kp->Weights, x, kp->Capacity, timerecord);
			cout << fname << "," << *timerecord << "," << yexpknap << "\n";
            exp_outputfile << fname << "," << *timerecord << "," << yexpknap << "\n";
#endif
#ifdef COMBO			
			int ycombo = combo_wrap(kp->noItems, kp->Values, kp->Weights, x, kp->Capacity, timerecord);
			cout << fname << "," << *timerecord << "," << ycombo << "\n";
			com_outputfile << fname << "," << *timerecord << "," << ycombo << "\n";
#endif
#ifdef COMBOPLUS			
			int ycombo = comboplus_wrap(kp->noItems, kp->Values, kp->Weights, x, kp->Capacity, timerecord);
			cout << fname << "," << *timerecord << "," << ycombo << "\n";
			com_outputfile << fname << "," << *timerecord << "," << ycombo << "\n";
#endif
#ifdef COMBO_EXPLICIT		
            int heurcount = 0;
            int surcount = 0;
            int divcount = 0;
			int ycombo = combo_wrap(kp->noItems, kp->Values, kp->Weights, x, kp->Capacity, timerecord, &heurcount, &surcount, &divcount);
			cout << fname << "," << *timerecord << "," << ycombo << "," << heurcount << "," << surcount << "," << divcount << "\n";
			com_outputfile << fname << "," << *timerecord << "," << ycombo << "," << heurcount << "," << surcount << "," << divcount << "\n";
#endif

			
			delete kp->Name, kp->Type, kp->Weights, kp->Values, x, timerecord;
            delete kp;
        }
    } else {
		cout << "Listfile did not open\n" << listpath << "\n";
	}
	
    listfile.close();
	
#ifdef MINKNAP
	min_outputfile.close();
#endif
#ifdef EXPKNAP
	exp_outputfile.close();
#endif
#ifdef COMBO
	com_outputfile.close();
#endif
#ifdef COMBOPLUS
	com_outputfile.close();
#endif
#ifdef COMBO_EXPLICIT
	com_outputfile.close();
#endif
#ifdef DYNPROG	
	dyn_outputfile.close();
#endif
#ifdef BASEARCH	
	bas_outputfile.close();
#endif
#ifdef KPCHOICE	
	kpc_outputfile.close();
#endif

    return 0;
};
