# C++ Compiler command
CXX = g++

# C++ Compiler options
CXXFLAGS = -O3 -std=gnu++11

all: KPsolvers

KPsolvers: Combo Expknap Minknap Dynprog Basearch Kpchoice

Combo_Explicit: ./src/combo_explicit.c ./src/handler.cpp
	$(CXX) $(CXXFLAGS) -c -o ./obj/combo_explicit.o ./src/combo_explicit.c \
	
	$(CXX) $(CXXFLAGS) -c -D COMBO_EXPLICIT -o ./obj/handler_combo_explicit.o ./src/handler.cpp \
	
	$(CXX) $(CXXFLAGS) -o ./bin/comboEXsolve ./obj/combo_explicit.o ./obj/handler_combo_explicit.o \

Comboplus: ./src/comboplus.c ./src/handler.cpp
	$(CXX) $(CXXFLAGS) -c -o ./obj/comboplus.o ./src/comboplus.c \
	
	$(CXX) $(CXXFLAGS) -c -D COMBOPLUS -o ./obj/handler_comboplus.o ./src/handler.cpp \
	
	$(CXX) $(CXXFLAGS) -o ./bin/comboplussolve ./obj/comboplus.o ./obj/handler_comboplus.o \


Combo: ./src/combo.c ./src/handler.cpp
	$(CXX) $(CXXFLAGS) -c -o ./obj/combo.o ./src/combo.c \
	
	$(CXX) $(CXXFLAGS) -c -D COMBO -o ./obj/handler_combo.o ./src/handler.cpp \
	
	$(CXX) $(CXXFLAGS) -o ./bin/combosolve ./obj/combo.o ./obj/handler_combo.o \


Expknap: ./src/expknap.c ./src/handler.cpp
	$(CXX) $(CXXFLAGS) -c -o ./obj/expknap.o ./src/expknap.c \
	
	$(CXX) $(CXXFLAGS) -c -D EXPKNAP -o ./obj/handler_expknap.o ./src/handler.cpp \
	
	$(CXX) $(CXXFLAGS) -o ./bin/expsolve ./obj/expknap.o ./obj/handler_expknap.o \

Minknap: ./src/minknap.c ./src/handler.cpp
	$(CXX) $(CXXFLAGS) -c -o ./obj/minknap.o ./src/minknap.c \

	$(CXX) $(CXXFLAGS) -c -D MINKNAP -o ./obj/handler_minknap.o ./src/handler.cpp \
	
	$(CXX) $(CXXFLAGS) -o ./bin/minsolve ./obj/minknap.o ./obj/handler_minknap.o \
	
Dynprog: ./src/dynprog.cpp ./src/handler.cpp
	$(CXX) $(CXXFLAGS) -c -o ./obj/dynprog.o ./src/dynprog.cpp \

	$(CXX) $(CXXFLAGS) -c -D DYNPROG -o ./obj/handler_dynprog.o ./src/handler.cpp \
	
	$(CXX) $(CXXFLAGS) -o ./bin/dynsolve ./obj/dynprog.o ./obj/handler_dynprog.o \

Basearch: ./src/dynprog.cpp ./src/handler.cpp
	$(CXX) $(CXXFLAGS) -c -o ./obj/basearch.o ./src/basearch.cpp \

	$(CXX) $(CXXFLAGS) -c -D BASEARCH -o ./obj/handler_basearch.o ./src/handler.cpp \
	
	$(CXX) $(CXXFLAGS) -o ./bin/basearch ./obj/basearch.o ./obj/handler_basearch.o \

	
Kpchoice: ./src/kpchoice.cpp ./src/handler.cpp
	$(CXX) $(CXXFLAGS) -c -o ./obj/kpchoice.o ./src/kpchoice.cpp \

	$(CXX) $(CXXFLAGS) -c -D KPCHOICE -o ./obj/handler_kpchoice.o ./src/handler.cpp \
	
	$(CXX) $(CXXFLAGS) -o ./bin/kpchoice ./obj/kpchoice.o ./obj/handler_kpchoice.o \
	
clean:
	rm -f ./bin/* ./obj/*.o