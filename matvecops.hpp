#ifndef MATEVECOPS_HPP
#define MATEVECOPS_HPP

#include <vector>
/*Method for calculating the 2-norm of a vector*/
double twoNorm(std::vector<double> const &x);

/*Method for calculating the dot product of two vectors*/
double dotProduct(std::vector<double> const &x, std::vector<double> const &y);

/*Method for multipling a vector by a constant*/
std::vector<double> constVecMultiply(double a,
                                     std::vector<double> const &x);

/*Method for mulitpling a matrix in CSR format with a vector*/
std::vector<double> matVecMultiply(std::vector<double> const &val,
                                   std::vector<int> const &row_ptr,
                                   std::vector<int> const &col_idx,
                                   std::vector<double> const &x);

/*Method for calculating the A norm of two vectors*/
double A_norm(std::vector<double> const &val,
              std::vector<int> const &row_ptr,
              std::vector<int> const &col_idx,
              std::vector<double> const &x, 
              std::vector<double> const &y);

/*Method for subtracting two vectors*/
std::vector<double> vectorSubtraction(std::vector<double> const &x,
                                      std::vector<double> const &y);

/*Method for adding two vectors*/
std::vector<double> vectorAddition(std::vector<double> const &x,
                                      std::vector<double> const &y);
#endif /* MATVECOPS_HPP */