#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "sparse.hpp"
#include "COO2CSR.hpp"
#include "matvecops.hpp"

void SparseMatrix::Resize(int nrows, int ncols)
{
    this->nrows = nrows;
    this->ncols = ncols;
}
void SparseMatrix::AddEntry(int i, int j, double val)
{
    i_idx.push_back(i);
    j_idx.push_back(j);
    a.push_back(val);
}

void SparseMatrix::ConvertToCSR()
{
    COO2CSR(a, i_idx, j_idx);
    CSR = 1;
}

std::vector<double> SparseMatrix::MulVec(std::vector<double> const &vec)
{
    /* Boolean ensures multiplication is only executed if matrix is in CSR format */
    if (CSR == 1)
    {
        /* call multiplication function from matvecops */
        std::vector<double> result = matVecMultiply(a, i_idx, j_idx, vec);
        return result;
    }
    else
    {
        std::cerr << "ERROR: Cannot multiply!" << std::endl;
        exit(1);
    }
}
double SparseMatrix::A_norm(std::vector<double> const &x, std::vector<double> const &y) 
{
    /* call dotProduct from matvecops */
        std::vector<double> z = MulVec(x); 
        double result = dotProduct(y, z);
        return result;
}
int SparseMatrix::GetSize()
{
    return ((int)i_idx.size()) -1;
}