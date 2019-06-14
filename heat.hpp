#ifndef HEAT_HPP
#define HEAT_HPP

#include <string>
#include <vector>

#include "sparse.hpp"

class HeatEquation2D
{
  private:
    SparseMatrix A;
    std::vector<double> b, x;
    std::vector<double> Th_vector;
    std::vector<double> Tc_vector;
    double tol;
    double length;
    double width;
    double h;
    double Tc;
    double Th;
    int ni;
    int nj;


  public:
    /* Method to setup Ax=b system */
    int Setup(std::string inputfile);

    /* Method to solve system using CGsolver */
    int Solve(std::string soln_prefix);

    /* Method for computing the lower isothermal boundary value */
    double lowerIsothermalBoundary(double x);
   

};

#endif /* HEAT_HPP */
