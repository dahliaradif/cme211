#ifndef SPARSE_HPP
#define SPARSE_HPP

#include <vector>
#include "matvecops.hpp"

class SparseMatrix
{
  friend class HeatEquation2D;
  private:
    int CSR = 0;
    std::vector<int> i_idx;
    std::vector<int> j_idx;
    std::vector<double> a;
    int ncols;
    int nrows;

  public:
    /* Method to modify sparse matrix dimensions */
    void Resize(int nrows, int ncols);
   

    /* Method to add entry to matrix in COO format */
    void AddEntry(int i, int j, double val);

    /* Method to convert COO matrix to CSR format using provided function */
    void ConvertToCSR();

    /* Method to perform sparse matrix vector multiplication using CSR formatted matrix */
    std::vector<double> MulVec(std::vector<double> const &vec);

    /*Method for computing the A norm between two vectors */
    double A_norm(std::vector<double> const &x, std::vector<double> const &y); 

    /* Method for getting the dimensions of a matrix */ 
    int GetSize();
    
};

#endif /* SPARSE_HPP */
