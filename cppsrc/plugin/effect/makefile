# default PTRHON_VERSION is 3.6 on Mac, 3.5 in other os
# if you installed other python version, Please specific your Python Version below
PYTHON_VERSION = 3.9
TARGET = cpp_plugin_rapper

CFLAGS = -lm -pthread -O3 -std=c++11 -march=native -Wall -funroll-loops -Wno-unused-result
osname := $(shell uname)
user_name = $(shell whoami)

# Only need to change if you install boost-python from source
BOOST_INC = /Users/$(user_name)/opt/anaconda3/envs/py39/include/boost/
BOOST_LIB = /Users/$(user_name)/opt/anaconda3/envs/py39/lib/ #3.9なのでbrewで入れたやつ

# $(info $$osname is [${osname}])

# if PYTHON_VERSION not set, set default PYTHON_VERSION
ifeq ($(osname), Darwin)
	EXPORT_DYNAMIC_NAME = export_dynamic
	ifeq ($(PYTHON_VERSION), None)
		PYTHON_VERSION = 3.6
	endif
else
	EXPORT_DYNAMIC_NAME = -export-dynamic
	ifeq ($(PYTHON_VERSION), None)
		PYTHON_VERSION = 3.5
	endif
endif	

$(eval REMAINDER := $$$(PYTHON_VERSION))
FIRST := $(subst $(REMAINDER),,$(PYTHON_VERSION))

# set default PYTHON_INCLUDE and LIBPYTHON_PATH for different os
# PYTHON_INCLUDE should be the path contain pyconfig.h
# LIBPYTHON_PATH should be the path contain libpython3.6 or libpython3.5 or libpython2.7 or whichever your python version
ifeq ($(osname), Darwin)
	ifeq ($(FIRST), 3)
		PYTHON_INCLUDE = /Users/$(user_name)/opt/anaconda3/envs/py39/include/python3.9/
		LIBPYTHON_PATH = /Users/$(user_name)/opt/anaconda3/envs/py39/lib/python3.9/config-3.9-darwin

#PYTHON_INCLUDE = /usr/local/opt/python@3.9/Frameworks/Python.framework/Versions/3.9/include/python3.9
#$python3.9-config --include
#LIBPYTHON_PATH = /usr/local/opt/python@3.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/config-3.9-darwin
#$python3.9-config --ldflags
	else
		PYTHON_INCLUDE = /Users/$(user_name)/opt/anaconda3/envs/py39/include/python3.9/
		LIBPYTHON_PATH = /Users/$(user_name)/opt/anaconda3/envs/py39/lib/python3.9/config-3.9-darwin
	endif
else
	PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)
	LIBPYTHON_PATH = /usr/lib/python$(PYTHON_VERSION)/config
endif

# boost python lib, on mac, default is lboost_python for python2.x, lboost_python3 for python3.x
# on ubuntu, name ===> python3.5m
# on mac, name ===> python3.6
ifeq ($(FIRST), 3)
	BOOST = lboost_python39
	ifeq ($(osname), Darwin)
		PYTHON_VERSION_FINAL = $(PYTHON_VERSION)
	else
		PYTHON_VERSION_FINAL = $(PYTHON_VERSION)m
	endif
else
	BOOST = lboost_python
	PYTHON_VERSION_FINAL = $(PYTHON_VERSION)
endif

 
$(TARGET).so: $(TARGET).o
	g++ $(CFLAGS) -shared -Wl,-$(EXPORT_DYNAMIC_NAME) $(TARGET).o -L$(BOOST_LIB) -$(BOOST) -L$(LIBPYTHON_PATH) -undefined dynamic_lookup -o $(TARGET).so
#g++ $(CFLAGS) -shared -Wl,-$(EXPORT_DYNAMIC_NAME) $(TARGET).o -L$(BOOST_LIB) -$(BOOST) -L$(LIBPYTHON_PATH) -lpython3.9 -o $(TARGET).so
#pytyhon3.9だけ手打ちで変更
 
$(TARGET).o: $(TARGET).cpp
	g++ $(CFLAGS) -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC -c $(TARGET).cpp

#g++ -I`python -c 'from distutils.sysconfig import *; print get_python_inc()'` -DPIC -bundle -fPIC -o basic.so basic.cpp -lboost_python  -framework Python


#https://github.com/zpoint/Boost-Python-Examples/tree/master/Examples/basic_interface ← 参考にしました

#make しなさい〜〜〜〜〜〜！

#PYTHON_INCLUDE = /Users/"name"/opt/anaconda3/envs/py39/include/python3.9
#LIBPYTHON_PATH = /Users/"name"/opt/anaconda3/envs/py39/lib/python3.9/config-3.9-darwin

#boostは別にビルドしろばか