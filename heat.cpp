#include <iostream>
#include <fstream>
#include <math.h>
#include <string>
#include <vector>

#include "CGSolver.hpp"
#include "heat.hpp"
#include "sparse.hpp"

using std::cout;
using std::endl;

int HeatEquation2D::Setup(std::string inputfile)
{

    std::ifstream input(inputfile);
    if (input.is_open())
    {
        input >> length >> width >> h;
        input >> Tc >> Th;
    }
    input.close();
    nj = (int)((length / h) + 1);
    ni = (int)((width / h) + 1);         
    /*size of matrix (excluding isothermal boundaries and repeated
    periodic boundary condition. Also number of grid entries excluding
    the same conditions*/
    int size = (ni - 2) * (nj-1); 
    b.reserve((unsigned int)size);
    x.reserve((unsigned int)size);
    A.Resize(size, size);
    /* omit bottom and top row of grid because of isothermal boundary conditions */
    for (int i = 1; i < (ni - 1); i++)
    {
        for (int j = 0; j < (nj-1); j++)
        {
            x.push_back(1);
            /* row index of matrix corresponding to the grid point*/
            int rowindex = j + ((i - 1) * (nj-1));
            A.AddEntry(rowindex, rowindex, 4);
            b.insert(b.begin() + (unsigned int)rowindex, 0);
            /* Conditions for grid point being directly above or below
            isothermal boundary condition */
            if (i == 1)
            {
                double Tx = lowerIsothermalBoundary((j * h));
                b[(unsigned int)rowindex] = Tx;
                Tc_vector.push_back(Tx);
            }
            else
            {
                A.AddEntry(rowindex, rowindex - (nj-1), -1);
            }
            if (i == ni - 2)
            {
                b[(unsigned int)rowindex] = Th;
                Th_vector.push_back(Th);
            }
            else
            {
                A.AddEntry(rowindex, rowindex + (nj-1), -1);
            }
            /* Conditions for grid point lying on or next to a peridoic boundary */
            if (j == 0)
            {
                A.AddEntry(rowindex, rowindex + (nj - 2), -1);
            }
            else
            {
                A.AddEntry(rowindex, rowindex - 1, -1);
            }
            if (j == nj - 2)
            {

                A.AddEntry(rowindex, rowindex - (nj - 2), -1);
            }
            else
            {
                A.AddEntry(rowindex, rowindex + 1, -1);
            }
        }
    }
    A.ConvertToCSR();
    /* Checking that dimension of matrix is equal to the number of grid elements */
    if (A.GetSize() != size)
    {
        return 1;
    }
    return 0;
}
int HeatEquation2D::Solve(std::string soln_prefix)
{
    
    tol = 1e-5;
    int n = CGSolver(A, b, x, tol, Th_vector, Tc_vector, soln_prefix);
    if (n != -1)
    {
        cout << "SUCCESS: CG solver converged in " << n << " iterations." << endl;
    }
    else
    {
        return 1;
    }
    return 0;
}
double HeatEquation2D::lowerIsothermalBoundary(double x)
{
    double value = -10 * pow((x - (length / 2)), 2);
    double param = exp(value) - 2;
    double Tx = (-Tc) * param;
    return Tx;
}


