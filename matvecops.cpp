#include <iostream>
#include <math.h>
#include <vector>
#include "matvecops.hpp"

double twoNorm(std::vector<double> const &x)
{
    double counter = 0; 
    for (unsigned int i = 0; i < x.size(); i++)
    {
        counter += x[i] * x[i];
    }
    double norm = sqrt(counter);
    return norm;
}

double dotProduct(std::vector<double> const &x, std::vector<double> const &y)
{
    if (x.size() == y.size())
    {
        double counter = 0;
        for (unsigned int i = 0; i < x.size(); i++)
        {
            counter += x[i] * y[i];
        }
        return counter;
    }
    else
    {
        std::cerr << "ERROR: Dimensions of vectors do not match" << std::endl;
        exit(1);
        
    }
}

std::vector<double> constVecMultiply(double a,
                                     std::vector<double> const &x)
{
    std::vector<double> result(x.size(), 0);
    for (unsigned int i = 0; i < x.size(); i++)
    {
        result[i] = x[i] * a;
    }
    return result;
}

std::vector<double> matVecMultiply(std::vector<double> const &val,
                                   std::vector<int> const &row_ptr,
                                   std::vector<int> const &col_idx,
                                   std::vector<double> const &x)
{
    if (x.size() == row_ptr.size() - 1)
    {
        std::vector<double> result(x.size(), 0);
        for (unsigned int i = 0; i < x.size(); i++)
        {
            for (unsigned int k = (unsigned int)row_ptr[i]; k < (unsigned int)row_ptr[i + 1]; k++)
            {
                result[i] += val[k] *  x[(unsigned int)col_idx[k]];
            }
        }
        return result;
    }
    else
    {
        std::cerr << "ERROR: Cannot multiply- dimensions do not match" << std::endl;
        exit(1);
    }
}
//returns <x,Ay>
double A_norm(std::vector<double> const &val,
              std::vector<int> const &row_ptr,
              std::vector<int> const &col_idx,
              std::vector<double> const &x,
              std::vector<double> const &y) 
{
        std::vector<double> Ax = matVecMultiply(val, row_ptr, col_idx, x); 
        double result = dotProduct(y, Ax);
        return result;
}

std::vector<double> vectorSubtraction(std::vector<double> const &x,
                                      std::vector<double> const &y)
{
    if (x.size() == y.size())
    {
        std::vector<double> result(x.size(), 0);
        for (unsigned int i = 0; i < x.size(); i++)
        {
            result[i] = x[i] - y[i];
        }
        return result;
    }
    else
    {
        std::cerr << "ERROR: Cannot subtract- dimensions do not match" << std::endl;
        exit(1);
    }
}

std::vector<double> vectorAddition(std::vector<double> const &x,
                                      std::vector<double> const &y)
{
    if (x.size() == y.size())
    {
        std::vector<double> result(x.size(), 0);
        for (unsigned int i = 0; i < x.size(); i++)
        {
            result[i] = x[i] + y[i];
        }
        return result;
    }
    else
    {
        std::cerr << "ERROR: Cannot add- dimensions do not match" << std::endl;
        exit(1);
    }
}