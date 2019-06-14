#ifndef CGSOLVER_HPP
#define CGSOLVER_HPP

#include <vector>
#include "sparse.hpp"
/* Function that implements the CG algorithm for a linear system
 *
 * Ax = b
 *
 * where A is in CSR format.  The starting guess for the solution
 * is provided in x, and the solver runs a maximum number of iterations
 * equal to the size of the linear system.  Function returns the
 * number of iterations to converge the solution to the specified
 * tolerance, or -1 if the solver did not converge.
 */
int CGSolver(SparseMatrix A,
             std::vector<double> &b,
             std::vector<double> &x,
             double const tol,
             std::vector<double> const &Th_vector,
             std::vector<double> const &Tc_vector,
             std::string soln_prefix);

/*Method for writing the solution vector to a file with isothermal boundaries*/
void WriteToFile(std::string filename,
                 std::vector<double> const &Tc,
                 std::vector<double> const &Th,
                 std::vector<double> const &z);

/*Method for obtaining the suitable file name of the solution file*/
std::string GetFileName(int digit, std::string soln_prefix);

/*Method for formatting the number part of the solution file name*/
std::string FormatNumber(int digit);

#endif /* CGSOLVER_HPP */
