// 16ビット モノラル
#include <bits/stdc++.h>
#include <math.h>
#include <stdio.h>

#include <boost/python.hpp>
#include <boost/python/numpy.hpp>
#include <iomanip>
using namespace std;
namespace py = boost::python;
namespace np = boost::python::numpy;

#include "../synthetic/normal.hpp"

class SyntheticControl
{
private:
public:
    SyntheticControl()
    {
    }
    np::array run(std::string typename, np::array &source, np::array &additions)
    {
    }
}